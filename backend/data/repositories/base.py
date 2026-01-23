from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any, Dict

T = TypeVar("T")
ID = TypeVar("ID")


class BaseRepository(ABC, Generic[T, ID]):
    """
    统一的数据访问接口基类
    定义了通用的 CRUD 操作契约
    """

    @abstractmethod
    def get(self, id: ID) -> Optional[T]:
        """根据 ID 获取单个实体"""
        pass

    @abstractmethod
    def list(self, **kwargs) -> List[T]:
        """获取实体列表，支持可选的过滤参数"""
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        """创建新实体"""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """更新实体"""
        pass

    @abstractmethod
    def delete(self, id: ID) -> bool:
        """根据 ID 删除实体"""
        pass

    @abstractmethod
    def count(self, **kwargs) -> int:
        """获取数量"""
        pass
