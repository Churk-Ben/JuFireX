from typing import Generic, TypeVar, List, Optional, Type, Any
from sqlalchemy import select
from backend.data.database import db

T = TypeVar('T', bound=db.Model)

class BaseRepository(Generic[T]):
    """
    通用 Repository 基类，提供基本的 CRUD 操作。
    """
    def __init__(self, model: Type[T]):
        self.model = model

    def get_by_id(self, id: Any) -> Optional[T]:
        """根据 ID 获取实体"""
        return db.session.get(self.model, id)

    def get_all(self) -> List[T]:
        """获取所有实体"""
        stmt = select(self.model)
        return db.session.scalars(stmt).all()

    def add(self, entity: T, commit: bool = True) -> T:
        """添加新实体"""
        db.session.add(entity)
        if commit:
            db.session.commit()
        return entity

    def update(self, entity: T, commit: bool = True) -> T:
        """更新实体（主要是提交事务）"""
        if commit:
            db.session.commit()
        return entity

    def delete(self, entity: T, commit: bool = True) -> None:
        """删除实体"""
        db.session.delete(entity)
        if commit:
            db.session.commit()
            
    def save(self, commit: bool = True) -> None:
        """手动提交更改"""
        if commit:
            db.session.commit()
