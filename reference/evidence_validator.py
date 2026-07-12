"""Reference implementation: evidence package structure validation."""
import zipfile
REQUIRED_FILES = ["manifest.json", "session.json", "events.jsonl", "signature.sig"]
def validate_package_structure(path: str) -> dict:
    try:
        with zipfile.ZipFile(path, 'r') as zf:
            missing = [f for f in REQUIRED_FILES if f not in zf.namelist()]
            if missing:
                return {"valid": False, "errors": [f"Missing required files: {missing}"]}
            return {"valid": True, "errors": []}
    except zipfile.BadZipFile:
        return {"valid": False, "errors": ["Not a valid ZIP file"]}
