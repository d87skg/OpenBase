from typing import Optional
import uuid

class LamportClock:
    def __init__(self, node_id: str, initial_time: int = 0):
        self.node_id = node_id
        self._time = initial_time

    def tick(self) -> int:
        self._time += 1
        return self._time

    def update(self, received_time: int) -> int:
        self._time = max(self._time, received_time) + 1
        return self._time

    def get_time(self) -> int:
        return self._time

    def get_node_id(self) -> str:
        return self.node_id