import json
from pathlib import Path


class Registry:
    def __init__(self, path: str = ".openbase/registry"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def register_runtime(self, data: dict):
        file = self.path / "runtime.json"
        file.write_text(json.dumps(data, indent=2))

    def get_runtime(self):
        file = self.path / "runtime.json"
        if file.exists():
            return json.loads(file.read_text())
        return None
