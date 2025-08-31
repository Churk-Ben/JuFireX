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
    
    def search(self, search_term: str, search_fields: List[str]) -> List[Any]:
        """搜索记录"""
        try:
            query = self.model_class.query
            
            if search_term and search_fields:
                conditions = []
                for field in search_fields:
                    if hasattr(self.model_class, field):
                        attr = getattr(self.model_class, field)
                        conditions.append(attr.ilike(f'%{search_term}%'))
                
                if conditions:
                    from sqlalchemy import or_
                    query = query.filter(or_(*conditions))
            
            return query.all()
        except Exception as e:
            self.logger.error(f"搜索失败: {str(e)}")
            return []
    
    def paginate(self, page: int = 1, per_page: int = 20, 
                 filters: Optional[Dict] = None) -> Dict:
        """分页查询"""
        try:
            query = self.model_class.query
            
            if filters:
                query = self._apply_filters(query, filters)
            
            pagination = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            return {
                'items': pagination.items,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page,
                'per_page': per_page,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next
            }
        except Exception as e:
            self.logger.error(f"分页查询失败: {str(e)}")
            return {
                'items': [],
                'total': 0,
                'pages': 0,
                'current_page': page,
                'per_page': per_page,
                'has_prev': False,
                'has_next': False
            }
    
    # ========== 创建操作 ==========
    
    def create(self, data: Dict) -> tuple[bool, Union[Any, str]]:
        """创建新记录"""
        try:
            # 验证数据
            validation_result = self.validate_create_data(data)
            if not validation_result[0]:
                return False, validation_result[1]
            
            # 预处理数据
            processed_data = self.preprocess_create_data(data)
            
            # 创建实例
            instance = self.model_class(**processed_data)
            
            # 保存到数据库
            self.db.session.add(instance)
            self.db.session.commit()
            
            # 后处理
            self.postprocess_create(instance, data)
            
            self.logger.info(f"创建记录成功 (ID: {instance.id})")
            return True, instance
            
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"创建记录失败: {str(e)}")
            return False, str(e)
    
    # ========== 更新操作 ==========
    
    def update(self, item_id: int, data: Dict) -> tuple[bool, Union[Any, str]]:
        """更新记录"""
        try:
            # 获取记录
            instance = self.get_by_id(item_id)
            if not instance:
                return False, "记录不存在"
            
            # 验证数据
            validation_result = self.validate_update_data(data, instance)
            if not validation_result[0]:
                return False, validation_result[1]
            
            # 预处理数据
            processed_data = self.preprocess_update_data(data, instance)
            
            # 更新属性
            for key, value in processed_data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            # 更新时间戳
            if hasattr(instance, 'updated_at'):
                instance.updated_at = datetime.utcnow()
            
            self.db.session.commit()
            
            # 后处理
            self.postprocess_update(instance, data)
            
            self.logger.info(f"更新记录成功 (ID: {item_id})")
            return True, instance
            
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"更新记录失败 (ID: {item_id}): {str(e)}")
            return False, str(e)
    
    # ========== 删除操作 ==========
    
    def delete(self, item_id: int) -> tuple[bool, str]:
        """删除记录"""
        try:
            # 获取记录
            instance = self.get_by_id(item_id)
            if not instance:
                return False, "记录不存在"
            
            # 检查是否可以删除
            can_delete, message = self.can_delete(instance)
            if not can_delete:
                return False, message
            
            # 预处理删除
            self.preprocess_delete(instance)
            
            # 删除记录
            self.db.session.delete(instance)
            self.db.session.commit()
            
            # 后处理删除
            self.postprocess_delete(instance)
            
            self.logger.info(f"删除记录成功 (ID: {item_id})")
            return True, "删除成功"
            
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"删除记录失败 (ID: {item_id}): {str(e)}")
            return False, str(e)
    
    # ========== 批量操作 ==========
    
    def bulk_update(self, updates: List[Dict]) -> tuple[bool, str]:
        """批量更新"""
        try:
            for update_data in updates:
                item_id = update_data.get('id')
                if not item_id:
                    continue
                
                success, result = self.update(item_id, update_data)
                if not success:
                    self.db.session.rollback()
                    return False, f"批量更新失败: {result}"
            
            return True, "批量更新成功"
            
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"批量更新失败: {str(e)}")
            return False, str(e)
    
    def bulk_delete(self, item_ids: List[int]) -> tuple[bool, str]:
        """批量删除"""
        try:
            for item_id in item_ids:
                success, message = self.delete(item_id)
                if not success:
                    self.db.session.rollback()
                    return False, f"批量删除失败: {message}"
            
            return True, "批量删除成功"
            
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"批量删除失败: {str(e)}")
            return False, str(e)
    
    # ========== 工具方法 ==========
    
    def _apply_filters(self, query, filters: Dict):
        """应用过滤条件"""
        for field, value in filters.items():
            if hasattr(self.model_class, field) and value is not None:
                attr = getattr(self.model_class, field)
                if isinstance(value, list):
                    query = query.filter(attr.in_(value))
                else:
                    query = query.filter(attr == value)
        return query
    
    def _apply_ordering(self, query, order_by: str):
        """应用排序"""
        if order_by.startswith('-'):
            field = order_by[1:]
            if hasattr(self.model_class, field):
                attr = getattr(self.model_class, field)
                query = query.order_by(attr.desc())
        else:
            if hasattr(self.model_class, order_by):
                attr = getattr(self.model_class, order_by)
                query = query.order_by(attr)
        return query
    
    # ========== 需要子类实现的抽象方法 ==========
    
    @abstractmethod
    def validate_create_data(self, data: Dict) -> tuple[bool, str]:
        """验证创建数据"""
        pass
    
    @abstractmethod
    def validate_update_data(self, data: Dict, instance: Any) -> tuple[bool, str]:
        """验证更新数据"""
        pass
    
    # ========== 可选的钩子方法 ==========
    
    def preprocess_create_data(self, data: Dict) -> Dict:
        """预处理创建数据"""
        return data
    
    def postprocess_create(self, instance: Any, original_data: Dict):
        """创建后处理"""
        pass
    
    def preprocess_update_data(self, data: Dict, instance: Any) -> Dict:
        """预处理更新数据"""
        return data
    
    def postprocess_update(self, instance: Any, original_data: Dict):
        """更新后处理"""
        pass
    
    def can_delete(self, instance: Any) -> tuple[bool, str]:
        """检查是否可以删除"""
        return True, ""
    
    def preprocess_delete(self, instance: Any):
        """删除前处理"""
        pass
    
    def postprocess_delete(self, instance: Any):
        """删除后处理"""
        pass