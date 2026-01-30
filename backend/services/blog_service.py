# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 博客服务层, 包含博客项的创建, 更新, 删除, 查询等业务逻辑
# ------------------------------------------------------------

from typing import Any, Dict, List, Optional, Tuple

from backend.data import BlogRepository


class BlogService:
    def __init__(self, blog_repo: BlogRepository):
        self.blog_repo = blog_repo

    def get_all(
        self, user_uuid: Optional[str] = None, view_all: bool = False
    ) -> List[Dict[str, Any]]:
        return self.blog_repo.get_all(user_uuid=user_uuid, view_all=view_all)

    def get_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        return self.blog_repo.get_by_uuid(uuid)

    def create(self, data: dict) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        try:
            if "owner_uuid" not in data:
                return False, "无法认证的作者", None

            blog = self.blog_repo.create(data)
            return True, "文章创建成功", blog
        except Exception as e:
            return False, f"创建失败: {str(e)}", None

    def update(
        self, uuid: str, data: dict
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        try:
            blog = self.blog_repo.update(uuid, data)
            if not blog:
                return False, "文章不存在", None
            return True, "文章更新成功", blog
        except Exception as e:
            return False, f"更新失败: {str(e)}", None

    def delete(self, uuid: str) -> Tuple[bool, str]:
        try:
            success = self.blog_repo.delete(uuid)
            if success:
                return True, "文章删除成功"
            return False, "文章不存在"
        except Exception as e:
            return False, f"删除失败: {str(e)}"

    def increment_views(self, uuid: str):
        self.blog_repo.increment_views(uuid)
