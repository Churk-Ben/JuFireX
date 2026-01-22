"""管理员服务类 - 处理管理员相关的业务逻辑"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from flask import current_app
from .base_service import BaseService
from ..models import User, StudioInfo, Project, NavCategory, NavItem, HiddenNavItem
from ..config import ROLE_GUEST, ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN, ROLE_NAMES
from ..utils import delete_user_data_file, save_file_to_user_data

class AdminService(BaseService):
    """管理员服务类，处理用户管理、工作室信息管理等功能"""
    
    def __init__(self, db):
        super().__init__(db, User)  # 默认使用User模型
    
    # ========== 用户管理 ==========
    
    def get_all_users(self) -> List[User]:
        """获取所有用户"""
        return self.get_all(order_by="-created_at")
    
    def get_user_details(self, user_id: int) -> Optional[Dict]:
        """获取用户详细信息"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        # 构建用户数据
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "role_name": ROLE_NAMES.get(user.role, "未知"),
            "is_active": user.is_active,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "avatar_path": user.avatar_path,
        }
    
    def update_user_role(self, user_id: int, new_role: int) -> Tuple[bool, str]:
        """更新用户角色"""
        if new_role not in [ROLE_GUEST, ROLE_MEMBER, ROLE_ADMIN, ROLE_SUPER_ADMIN]:
            return False, "无效的角色"
        
        result = self.update(user_id, {"role": new_role})
        if result:
            return True, "用户角色更新成功"
        return False, "用户不存在或更新失败"
    
    def update_user_status(self, user_id: int, is_active: bool) -> Tuple[bool, str]:
        """更新用户状态（激活/禁用）"""
        result = self.update(user_id, {"is_active": is_active})
        if result:
            status_text = "激活" if is_active else "禁用"
            return True, f"用户已{status_text}"
        return False, "用户不存在或更新失败"
    
    def delete_user(self, user_id: int, current_user_id: int) -> Tuple[bool, str]:
        """删除用户"""
        # 不能删除自己
        if user_id == current_user_id:
            return False, "不能删除自己的账户"
        
        # 检查权限（不能删除其他超级管理员）
        user = self.get_by_id(user_id)
        current_user = self.get_by_id(current_user_id)
        
        if not user or not current_user:
            return False, "用户不存在"
        
        if user.role == ROLE_SUPER_ADMIN and current_user.role != ROLE_SUPER_ADMIN:
            return False, "权限不足"
        
        # 执行删除
        if self.delete(user_id):
            return True, "用户已删除"
        return False, "删除失败"
    
    # ========== 工作室信息管理 ==========
    
    def get_studio_info(self) -> Optional[StudioInfo]:
        """获取工作室信息"""
        return StudioInfo.query.first()
    
    def update_studio_info(self, data: Dict) -> Tuple[bool, str]:
        """更新工作室信息"""
        try:
            studio_info = self.get_studio_info()
            
            if not studio_info:
                # 如果不存在，创建新的
                studio_info = StudioInfo(
                    name=data.get("name", ""),
                    description=data.get("description", ""),
                    logo_url=data.get("logo_url", ""),
                    contact_email=data.get("contact_email", ""),
                    github_url=data.get("github_url", ""),
                )
                self.db.session.add(studio_info)
            else:
                # 更新现有信息
                studio_info.name = data.get("name", studio_info.name)
                studio_info.description = data.get("description", studio_info.description)
                
                # 处理logo
                if "logo_url" in data:
                    new_logo_url = data["logo_url"]
                    old_logo_url = studio_info.logo_url
                    
                    # 如果新的URL与旧的URL不同，或者新的URL为空，则处理旧图片
                    if new_logo_url != old_logo_url:
                        if old_logo_url:
                            delete_user_data_file(old_logo_url)
                        
                        if new_logo_url:
                            # 保存新的logo图片到用户数据目录
                            saved_url = save_file_to_user_data(
                                new_logo_url, storage_folder="user_data"
                            )
                            if saved_url:
                                studio_info.logo_url = saved_url
                            else:
                                current_app.logger.warning(
                                    f"Failed to save logo from {new_logo_url}"
                                )
                        else:
                            # 如果新的URL为空，则清空数据库中的值
                            studio_info.logo_url = None
                
                studio_info.contact_email = data.get("contact_email", studio_info.contact_email)
                studio_info.github_url = data.get("github_url", studio_info.github_url)
                studio_info.updated_at = datetime.now()
            
            self.db.session.commit()
            return True, "工作室信息更新成功"
        except Exception as e:
            self.db.session.rollback()
            self.logger.error(f"更新工作室信息失败: {str(e)}")
            return False, f"更新失败: {str(e)}"
    
    # ========== 项目管理 ==========
    
    def get_all_projects(self) -> List[Project]:
        """获取所有项目"""
        return Project.query.order_by(Project.created_at.desc()).all()
    
    # ========== 导航管理 ==========
    
    def get_navigation_data(self, user_id: int) -> Dict:
        """获取导航管理数据"""
        # 获取所有分类和导航项
        categories = NavCategory.query.order_by(NavCategory.order).all()
        nav_items = NavItem.query.order_by(NavItem.order).all()
        
        # 获取当前用户隐藏的导航项
        hidden_items = (
            self.db.session.query(HiddenNavItem, NavItem)
            .join(NavItem, HiddenNavItem.nav_item_id == NavItem.id)
            .filter(HiddenNavItem.user_id == user_id)
            .all()
        )
        
        hidden_nav_items = []
        for hidden_item, nav_item in hidden_items:
            hidden_nav_items.append({
                "id": nav_item.id,
                "title": nav_item.title,
                "url": nav_item.url,
                "description": nav_item.description,
                "icon": nav_item.icon,
                "category_id": nav_item.category_id,
                "category_name": nav_item.category.name,
                "hidden_at": hidden_item.hidden_at.strftime("%Y-%m-%d %H:%M:%S"),
            })
        
        return {
            "categories": categories,
            "nav_items": nav_items,
            "hidden_nav_items": hidden_nav_items
        }