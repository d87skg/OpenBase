"""
OpenBase Registry - Health API
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "OpenBase Registry",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/ready")
async def readiness_check():
    return {
        "status": "ready",
        "service": "OpenBase Registry"
    }
