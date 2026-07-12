"""
OpenBase Registry - Base Storage Interface
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class BaseStore(ABC):
    """存储层抽象接口"""

    @abstractmethod
    def create(self, collection: str, data: Dict[str, Any]) -> str:
        """创建记录"""
        pass

    @abstractmethod
    def get(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        """获取记录"""
        pass

    @abstractmethod
    def list(self, collection: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """列出记录"""
        pass

    @abstractmethod
    def update(self, collection: str, id: str, data: Dict[str, Any]) -> bool:
        """更新记录"""
        pass

    @abstractmethod
    def delete(self, collection: str, id: str) -> bool:
        """删除记录"""
        pass

    @abstractmethod
    def query(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """自定义查询"""
        pass
