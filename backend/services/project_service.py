# ------------------------------------------------------------
# @author: Churk
# @status: 待审查
# @description: 项目服务层, 包含项目的创建, 更新, 删除, 查询等业务逻辑
# ------------------------------------------------------------

from typing import Any, Dict, List, Optional, Tuple

from backend.config import ROLE_ADMIN, ROLE_GUEST
from backend.data import ProjectRepository


class ProjectService:
    def __init__(self, proj_repo: ProjectRepository):
        self.proj_repo = proj_repo

    def get_all(
        self, user_role: int = ROLE_GUEST, view_all: bool = False
    ) -> List[Dict[str, Any]]:
        # 如果请求查看所有，必须是管理员
        if view_all and user_role < ROLE_ADMIN:
            # 降级为只看公开
            view_all = False

        # public_only 与 view_all 逻辑相反
        public_only = not view_all
        projects = self.proj_repo.get_all(public_only)
        return [p.to_dict() for p in projects]

    def get_by_uuid(
        self, uuid: str, user_role: int = ROLE_GUEST
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        project = self.proj_repo.get_by_uuid(uuid)
        if not project:
            return False, "项目不存在", None

        # 检查是否公开
        if project.is_public:
            return True, "获取成功", project.to_dict()

        # 如果是私有项目, 检查权限 (必须是管理员)
        if user_role >= ROLE_ADMIN:
            return True, "获取成功", project.to_dict()

        return False, "权限不足", None

    def create(
        self, data: dict, user_role: int = ROLE_GUEST
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        # 必须是管理员
        if user_role < ROLE_ADMIN:
            return False, "权限不足", None

        try:
            proj = self.proj_repo.create(data)
            return True, "项目创建成功", proj.to_dict()
        except Exception as e:
            return False, f"创建失败: {str(e)}", None

    def update(
        self, uuid: str, data: dict, user_role: int = ROLE_GUEST
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        # 必须是管理员
        if user_role < ROLE_ADMIN:
            return False, "权限不足", None

        proj = self.proj_repo.update(uuid, data)
        if not proj:
            return False, "项目不存在", None
        return True, "项目更新成功", proj.to_dict()

    def delete(self, uuid: str, user_role: int = ROLE_GUEST) -> Tuple[bool, str]:
        # 必须是管理员
        if user_role < ROLE_ADMIN:
            return False, "权限不足"

        success = self.proj_repo.delete(uuid)
        if success:
            return True, "项目删除成功"
        return False, "项目不存在"
