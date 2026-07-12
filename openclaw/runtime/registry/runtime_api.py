"""
OpenBase Registry - Runtime API
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..service import RuntimeService
from ..models import Runtime, RuntimeStatus, RuntimeClass

router = APIRouter(prefix="/runtimes", tags=["runtimes"])


class RuntimeRegisterRequest(BaseModel):
    name: str
    version: str
    vendor: str
    runtime_class: str = "STANDARD"
    capabilities: List[str] = []
    description: Optional[str] = None
    metadata: dict = {}


class RuntimeUpdateRequest(BaseModel):
    status: Optional[str] = None
    version: Optional[str] = None
    capabilities: Optional[List[str]] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None


class RuntimeResponse(BaseModel):
    runtime_id: str
    name: str
    version: str
    vendor: str
    status: str
    runtime_class: str
    capabilities: List[str]
    description: Optional[str]
    registered_at: str
    updated_at: str


def setup_runtime_routes(service: RuntimeService):
    @router.post("/register", response_model=RuntimeResponse)
    async def register_runtime(request: RuntimeRegisterRequest):
        try:
            runtime_class = RuntimeClass(request.runtime_class.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid runtime_class: {request.runtime_class}")

        runtime = service.register(
            name=request.name,
            version=request.version,
            vendor=request.vendor,
            runtime_class=runtime_class,
            capabilities=request.capabilities,
            description=request.description,
            metadata=request.metadata
        )
        return RuntimeResponse(**runtime.to_dict())

    @router.get("/{runtime_id}", response_model=RuntimeResponse)
    async def get_runtime(runtime_id: str):
        runtime = service.get(runtime_id)
        if not runtime:
            raise HTTPException(status_code=404, detail=f"Runtime {runtime_id} not found")
        return RuntimeResponse(**runtime.to_dict())

    @router.get("/", response_model=List[RuntimeResponse])
    async def list_runtimes(status: Optional[str] = None):
        if status:
            try:
                status_enum = RuntimeStatus(status.upper())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
            runtimes = service.list_all(status_enum)
        else:
            runtimes = service.list_all()
        return [RuntimeResponse(**r.to_dict()) for r in runtimes]

    @router.put("/{runtime_id}", response_model=RuntimeResponse)
    async def update_runtime(runtime_id: str, request: RuntimeUpdateRequest):
        update_data = {}
        if request.status:
            try:
                RuntimeStatus(request.status.upper())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {request.status}")
            update_data["status"] = request.status.upper()
        if request.version:
            update_data["version"] = request.version
        if request.capabilities is not None:
            update_data["capabilities"] = request.capabilities
        if request.description is not None:
            update_data["description"] = request.description
        if request.metadata is not None:
            update_data["metadata"] = request.metadata

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        success = service.update(runtime_id, **update_data)
        if not success:
            raise HTTPException(status_code=404, detail=f"Runtime {runtime_id} not found")

        runtime = service.get(runtime_id)
        return RuntimeResponse(**runtime.to_dict())

    @router.delete("/{runtime_id}")
    async def delete_runtime(runtime_id: str):
        success = service.delete(runtime_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Runtime {runtime_id} not found")
        return {"message": f"Runtime {runtime_id} deleted"}

    return router
