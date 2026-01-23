from typing import List, Optional, Type, TypeVar, Any
from backend.data.database import db
from .base import BaseRepository

T = TypeVar("T")


class DBRepository(BaseRepository[T, int]):
    """
    基于 SQLAlchemy 的数据库仓储通用实现
    """

    def __init__(self, model_cls: Type[T]):
        self.model_cls = model_cls

    def get(self, id: int) -> Optional[T]:
        return db.session.get(self.model_cls, id)

    def list(self, **kwargs) -> List[T]:
        query = self.model_cls.query
        for key, value in kwargs.items():
            if hasattr(self.model_cls, key):
                query = query.filter(getattr(self.model_cls, key) == value)
        return query.all()

    def create(self, entity: T) -> T:
        db.session.add(entity)
        db.session.commit()
        return entity

    def update(self, entity: T) -> T:
        db.session.commit()
        return entity

    def delete(self, id: int) -> bool:
        entity = self.get(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()
            return True
        return False

    def count(self, **kwargs) -> int:
        query = self.model_cls.query
        for key, value in kwargs.items():
            if hasattr(self.model_cls, key):
                query = query.filter(getattr(self.model_cls, key) == value)
        return query.count()
