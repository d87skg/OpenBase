"""
OpenBase 全局状态（文件持久化）
"""

import json
from pathlib import Path

STATE_FILE = Path.home() / ".openbase" / "mesh_state.json"


def _ensure_dir():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


def _load_state():
    _ensure_dir()
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def _save_state(data):
    _ensure_dir()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_nodes():
    return _load_state()


def get_node(node_id):
    data = _load_state()
    return data.get(node_id)


def add_node(node_data):
    data = _load_state()
    data[node_data["node_id"]] = node_data
    _save_state(data)


def remove_node(node_id):
    data = _load_state()
    if node_id in data:
        del data[node_id]
        _save_state(data)


def update_node(node_id, updates):
    data = _load_state()
    if node_id in data:
        data[node_id].update(updates)
        _save_state(data)


def clear():
    _save_state({})
