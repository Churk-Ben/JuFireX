"""基础服务类 - 消除后端重复的CRUD操作代码"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from flask import current_app
import logging
from datetime import datetime

class BaseService(ABC):
    """基础服务类，提供通用的CRUD操作"""
    
    def __init__(self, db, model_class):
        self.db = db
        self.model_class = model_class
        self.logger = logging.getLogger(self.__class__.__name__)
    
    # ========== 查询操作 ==========
    
    def get_by_id(self, item_id: int) -> Optional[Any]:
        """根据ID获取单个记录"""
        try:
            return self.model_class.query.get(item_id)
        except Exception as e:
            self.logger.error(f"获取记录失败 (ID: {item_id}): {str(e)}")
            return None
    
    def get_all(self, filters: Optional[Dict] = None, 
                order_by: Optional[str] = None, 
                limit: Optional[int] = None) -> List[Any]:
        """获取所有记录"""
        try:
            query = self.model_class.query
            
            # 应用过滤条件
            if filters:
                query = self._apply_filters(query, filters)
            
            # 应用排序
            if order_by:
                query = self._apply_ordering(query, order_by)
            
            # 应用限制
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except Exception as e:
            self.logger.error(f"获取记录列表失败: {str(e)}")
            return []
    
    def _apply_filters(self, query, filters: Dict) -> Any:
        """应用过滤条件"""
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                query = query.filter(getattr(self.model_class, key) == value)
        return query
    
    def _apply_ordering(self, query, order_by: str) -> Any:
        """应用排序"""
        if order_by.startswith('-'):
            # 降序
            attr = order_by[1:]
            if hasattr(self.model_class, attr):
                query = query.order_by(getattr(self.model_class, attr).desc())
        else:
            # 升序
            if hasattr(self.model_class, order_by):
                query = query.order_by(getattr(self.model_class, order_by))
        return query
    
    # ========== 创建操作 ==========
    
    def create(self, data: Dict) -> Optional[Any]:
        """创建新记录"""
        try:
            item = self.model_class(**data)
            self.db.session.add(item)
            self.db.session.commit()
            return item
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"创建记录失败: {str(e)}")
            return None
    
    # ========== 更新操作 ==========
    
    def update(self, item_id: int, data: Dict) -> Optional[Any]:
        """更新记录"""
        try:
            item = self.get_by_id(item_id)
            if not item:
                return None
            
            for key, value in data.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            
            self.db.session.commit()
            return item
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"更新记录失败 (ID: {item_id}): {str(e)}")
            return None
    
    # ========== 删除操作 ==========
    
    def delete(self, item_id: int) -> bool:
        """删除记录"""
        try:
            item = self.get_by_id(item_id)
            if not item:
                return False
            
            self.db.session.delete(item)
            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"删除记录失败 (ID: {item_id}): {str(e)}")
            return False