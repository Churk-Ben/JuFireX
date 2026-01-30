# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 博客服务层, 包含博客项的创建, 更新, 删除, 查询等业务逻辑
# ------------------------------------------------------------

from typing import Any, Dict, List, Optional, Tuple

from backend.config import ROLE_ADMIN, ROLE_GUEST
from backend.data import BlogRepository


class BlogService:
    def __init__(self, blog_repo: BlogRepository):
        self.blog_repo = blog_repo

    def get_all(
        self, user_uuid: Optional[str] = None, view_all: bool = False
    ) -> List[Dict[str, Any]]:
        return self.blog_repo.get_all(user_uuid=user_uuid, view_all=view_all)

    def get_by_uuid(
        self,
        uuid: str,
        user_uuid: Optional[str] = None,
        user_role: int = ROLE_GUEST,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        blog = self.blog_repo.get_by_uuid(uuid)
        if not blog:
            return False, "文章不存在", None

        # 检查是否公开
        if blog.get("is_public", True):
            return True, "获取成功", blog

        # 如果是私有文章, 检查权限
        # 1. 管理员
        if user_role >= ROLE_ADMIN:
            return True, "获取成功", blog

        # 2. 作者本人
        if user_uuid and user_uuid == blog.get("owner_uuid"):
            return True, "获取成功", blog

        return False, "权限不足", None

    def create(self, data: dict) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        try:
            if "owner_uuid" not in data:
                return False, "无法认证的作者", None

            blog = self.blog_repo.create(data)
            return True, "文章创建成功", blog
        except Exception as e:
            return False, f"创建失败: {str(e)}", None

    def update(
        self,
        uuid: str,
        data: dict,
        user_uuid: Optional[str] = None,
        user_role: int = ROLE_GUEST,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        try:
            # 先获取博客信息 (复用 get_by_uuid 可能会有点绕, 因为这里是写操作, 通常只要存在就可以进一步判断)
            # 为了避免逻辑循环, 直接查 Repo, 然后在这里做写权限判断
            blog = self.blog_repo.get_by_uuid(uuid)
            if not blog:
                return False, "文章不存在", None

            # 验权: 必须是管理员或作者
            is_admin = user_role >= ROLE_ADMIN
            is_owner = user_uuid and user_uuid == blog.get("owner_uuid")

            if not (is_admin or is_owner):
                return False, "权限不足", None

            blog = self.blog_repo.update(uuid, data)
            if not blog:
                return False, "文章不存在", None
            return True, "文章更新成功", blog
        except Exception as e:
            return False, f"更新失败: {str(e)}", None

    def delete(
        self,
        uuid: str,
        user_uuid: Optional[str] = None,
        user_role: int = ROLE_GUEST,
    ) -> Tuple[bool, str]:
        try:
            blog = self.blog_repo.get_by_uuid(uuid)
            if not blog:
                return False, "文章不存在"

            # 验权: 必须是管理员或作者
            is_admin = user_role >= ROLE_ADMIN
            is_owner = user_uuid and user_uuid == blog.get("owner_uuid")

            if not (is_admin or is_owner):
                return False, "权限不足"

            success = self.blog_repo.delete(uuid)
            if success:
                return True, "文章删除成功"
            return False, "文章不存在"
        except Exception as e:
            return False, f"删除失败: {str(e)}"

    def increment_views(self, uuid: str):
        self.blog_repo.increment_views(uuid)
