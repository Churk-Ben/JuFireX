from flask import current_app
from ..models import db, NavCategory, NavItem, HiddenNavItem, User

class NavigationService:
    """导航服务类，处理导航相关的业务逻辑"""
    
    def __init__(self, db):
        self.db = db
    
    def get_navigation_data(self, user_id=None):
        """获取导航管理页面所需的数据
        
        Args:
            user_id: 当前用户ID
            
        Returns:
            包含分类、导航项和隐藏导航项的字典
        """
        # 获取所有分类
        categories = NavCategory.query.order_by(NavCategory.order).all()
        
        # 获取所有导航项
        nav_items = NavItem.query.order_by(NavItem.order).all()
        
        # 获取当前用户隐藏的导航项
        hidden_nav_items = []
        if user_id:
            hidden_items = (
                self.db.session.query(HiddenNavItem, NavItem)
                .join(NavItem, HiddenNavItem.nav_item_id == NavItem.id)
                .filter(HiddenNavItem.user_id == user_id)
                .all()
            )
            hidden_nav_items = [
                {
                    "id": nav_item.id,
                    "title": nav_item.title,
                    "url": nav_item.url,
                    "description": nav_item.description,
                    "icon": nav_item.icon,
                    "category_id": nav_item.category_id,
                    "category_name": nav_item.category.name,
                }
                for _, nav_item in hidden_items
            ]
        
        return {
            "categories": categories,
            "nav_items": nav_items,
            "hidden_nav_items": hidden_nav_items
        }
    
    def get_user_navigation(self, user_id=None):
        """获取用户导航页面所需的数据
        
        Args:
            user_id: 当前用户ID
            
        Returns:
            包含分类和按分类分组的导航项的字典
        """
        # 获取所有分类
        categories = NavCategory.query.order_by(NavCategory.order).all()
        
        # 获取当前用户隐藏的导航项ID列表
        hidden_nav_item_ids = []
        hidden_nav_items = []
        if user_id:
            hidden_items = (
                self.db.session.query(HiddenNavItem, NavItem)
                .join(NavItem, HiddenNavItem.nav_item_id == NavItem.id)
                .filter(HiddenNavItem.user_id == user_id)
                .all()
            )
            hidden_nav_items = [
                {
                    "id": nav_item.id,
                    "title": nav_item.title,
                    "url": nav_item.url,
                    "description": nav_item.description,
                    "icon": nav_item.icon,
                    "category_id": nav_item.category_id,
                    "category_name": nav_item.category.name,
                }
                for _, nav_item in hidden_items
            ]
            hidden_nav_item_ids = [item["id"] for item in hidden_nav_items]
        
        # 获取所有导航项并按分类分组
        nav_items_by_category = {}
        for category in categories:
            # 获取该分类下的所有导航项（排除隐藏的）
            query = NavItem.query.filter_by(category_id=category.id)
            if hidden_nav_item_ids:
                query = query.filter(~NavItem.id.in_(hidden_nav_item_ids))
            nav_items = query.order_by(NavItem.order).all()

            if nav_items:
                nav_items_by_category[category.id] = nav_items
        
        return {
            "categories": categories,
            "nav_items_by_category": nav_items_by_category,
            "hidden_nav_items": hidden_nav_items
        }
    
    def create_nav_category(self, name, order=0):
        """创建导航分类
        
        Args:
            name: 分类名称
            order: 排序顺序
            
        Returns:
            (success, message, category_data) 元组
        """
        if not name:
            return False, "分类名称不能为空", None
        
        # 检查名称是否已存在
        existing = NavCategory.query.filter_by(name=name).first()
        if existing:
            return False, "分类名称已存在", None
        
        try:
            category = NavCategory(name=name, order=order)
            self.db.session.add(category)
            self.db.session.commit()
            
            return True, "分类创建成功", {
                "id": category.id,
                "name": category.name,
                "order": category.order,
                "created_at": category.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"创建导航分类失败: {str(e)}")
            return False, f"创建失败: {str(e)}", None
    
    def update_nav_category(self, category_id, name=None, order=None):
        """更新导航分类
        
        Args:
            category_id: 分类ID
            name: 新的分类名称
            order: 新的排序顺序
            
        Returns:
            (success, message, category_data) 元组
        """
        category = NavCategory.query.get(category_id)
        if not category:
            return False, "分类不存在", None
        
        try:
            if name is not None:
                # 检查名称是否已存在（排除当前分类）
                existing = NavCategory.query.filter(NavCategory.name == name, NavCategory.id != category_id).first()
                if existing:
                    return False, "分类名称已存在", None
                category.name = name
            
            if order is not None:
                category.order = order
            
            self.db.session.commit()
            
            return True, "分类更新成功", {
                "id": category.id,
                "name": category.name,
                "order": category.order,
                "created_at": category.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"更新导航分类失败: {str(e)}")
            return False, f"更新失败: {str(e)}", None
    
    def delete_nav_category(self, category_id):
        """删除导航分类
        
        Args:
            category_id: 分类ID
            
        Returns:
            (success, message) 元组
        """
        category = NavCategory.query.get(category_id)
        if not category:
            return False, "分类不存在"
        
        # 检查分类下是否有导航项
        nav_items_count = NavItem.query.filter_by(category_id=category_id).count()
        if nav_items_count > 0:
            return False, "该分类下存在导航项，无法删除"
        
        try:
            self.db.session.delete(category)
            self.db.session.commit()
            return True, "分类删除成功"
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"删除导航分类失败: {str(e)}")
            return False, f"删除失败: {str(e)}"
    
    def hide_nav_item(self, user_id, nav_item_id):
        """隐藏导航项
        
        Args:
            user_id: 用户ID
            nav_item_id: 导航项ID
            
        Returns:
            (success, message) 元组
        """
        # 检查导航项是否存在
        nav_item = NavItem.query.get(nav_item_id)
        if not nav_item:
            return False, "导航项不存在"
        
        # 检查是否已经隐藏
        existing = HiddenNavItem.query.filter_by(user_id=user_id, nav_item_id=nav_item_id).first()
        if existing:
            return False, "该导航项已被隐藏"
        
        try:
            hidden_item = HiddenNavItem(user_id=user_id, nav_item_id=nav_item_id)
            self.db.session.add(hidden_item)
            self.db.session.commit()
            return True, "导航项已隐藏"
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"隐藏导航项失败: {str(e)}")
            return False, f"隐藏失败: {str(e)}"
    
    def unhide_nav_item(self, user_id, nav_item_id):
        """显示导航项
        
        Args:
            user_id: 用户ID
            nav_item_id: 导航项ID
            
        Returns:
            (success, message) 元组
        """
        # 查找并删除隐藏记录
        hidden_item = HiddenNavItem.query.filter_by(user_id=user_id, nav_item_id=nav_item_id).first()
        if not hidden_item:
            return False, "该导航项未被隐藏"
        
        try:
            self.db.session.delete(hidden_item)
            self.db.session.commit()
            return True, "导航项已显示"
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"显示导航项失败: {str(e)}")
            return False, f"显示失败: {str(e)}"
    
    def unhide_all_nav_items(self, user_id):
        """显示所有导航项
        
        Args:
            user_id: 用户ID
            
        Returns:
            (success, message) 元组
        """
        try:
            num_deleted = HiddenNavItem.query.filter_by(user_id=user_id).delete()
            self.db.session.commit()
            return True, f"{num_deleted} 个导航项已恢复"
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"恢复所有导航项失败: {str(e)}")
            return False, f"恢复失败: {str(e)}"
    
    def toggle_nav_item_privacy(self, nav_item_id):
        """切换导航项的私有状态
        
        Args:
            nav_item_id: 导航项ID
            
        Returns:
            (success, message, is_private) 元组
        """
        nav_item = NavItem.query.get(nav_item_id)
        if not nav_item:
            return False, "导航项不存在", None
        
        try:
            nav_item.is_public = not nav_item.is_public
            self.db.session.commit()
            
            status = "公开" if nav_item.is_public else "私有"
            return True, f"导航项已设为{status}", not nav_item.is_public
        except Exception as e:
            self.db.session.rollback()
            current_app.logger.error(f"切换导航项私有状态失败: {str(e)}")
            return False, f"设置失败: {str(e)}", None
    
    def get_nav_item(self, nav_item_id, user_id):
        """获取单个导航项
        
        Args:
            nav_item_id: 导航项ID
            user_id: 用户ID
            
        Returns:
            (success, message, item_data) 元组
        """
        nav_item = NavItem.query.get(nav_item_id)
        if not nav_item:
            return False, "导航项不存在", None
        
        # 获取创建者信息
        creator = User.query.get(nav_item.created_by)
        creator_name = creator.username if creator else "未知"
        
        # 检查是否被当前用户隐藏
        is_hidden = HiddenNavItem.query.filter_by(user_id=user_id, nav_item_id=nav_item_id).first() is not None
        
        item_data = {
            "id": nav_item.id,
            "title": nav_item.title,
            "url": nav_item.url,
            "description": nav_item.description,
            "icon": nav_item.icon,
            "is_public": nav_item.is_public,
            "order": nav_item.order,
            "category_id": nav_item.category_id,
            "created_by": nav_item.created_by,
            "creator_name": creator_name,
            "created_at": nav_item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_hidden": is_hidden
        }
        
        return True, "获取成功", item_data