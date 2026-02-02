# ------------------------------------------------------------
# @author: Churk
# @status: 审查中
# @description: 项目服务层, 包含项目项的创建, 更新, 删除, 查询等业务逻辑
# ------------------------------------------------------------

from typing import Any, Dict, List, Optional, Tuple

from backend.config import ROLE_ADMIN, ROLE_GUEST
from backend.data import ProjectRepository


class ProjectService:
    def __init__(self, proj_repo: ProjectRepository):
        self.proj_repo = proj_repo

    def get_all(
        self, user_uuid: Optional[str] = None, view_all: bool = False
    ) -> List[Dict[str, Any]]:
        return self.proj_repo.get_all(user_uuid=user_uuid, view_all=view_all)

    def get_by_uuid(
        self,
        uuid: str,
        user_uuid: Optional[str] = None,
        user_role: int = ROLE_GUEST,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        project = self.proj_repo.get_by_uuid(uuid)
        if not project:
            return False, "项目不存在", None

        # 鉴权
        is_public = project.get("is_public", False)
        owner_uuid = project.get("owner_uuid")

        if is_public:
            return True, "获取成功", project

        if user_role >= ROLE_ADMIN:
            return True, "获取成功", project

        if user_uuid and owner_uuid == user_uuid:
            return True, "获取成功", project

        return False, "权限不足", None

    def create(
        self, data: dict, user_uuid: str, user_role: int = ROLE_GUEST
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        if user_role < ROLE_ADMIN:
            return False, "权限不足", None

        data["owner_uuid"] = user_uuid
        try:
            proj = self.proj_repo.create(data)
            return True, "项目创建成功", proj
        except Exception as e:
            return False, f"创建失败: {str(e)}", None

    def update(
        self,
        uuid: str,
        data: dict,
        user_role: int = ROLE_GUEST,
        user_uuid: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        success, msg, project = self.get_by_uuid(
            uuid, user_uuid=user_uuid, user_role=user_role
        )
        if not success:
            return False, msg, None

        if user_role < ROLE_ADMIN and project.get("owner_uuid") != user_uuid:
            return False, "权限不足", None

        proj = self.proj_repo.update(uuid, data)
        if not proj:
            return False, "项目不存在", None
        return True, "项目更新成功", proj

    def delete(
        self, uuid: str, user_role: int = ROLE_GUEST, user_uuid: Optional[str] = None
    ) -> Tuple[bool, str]:
        success, msg, project = self.get_by_uuid(
            uuid, user_uuid=user_uuid, user_role=user_role
        )
        if not success:
            return False, msg

        if user_role < ROLE_ADMIN and project.get("owner_uuid") != user_uuid:
            return False, "权限不足"

        if self.proj_repo.delete(uuid):
            return True, "项目删除成功"
        return False, "项目不存在"

    def get_file_tree(
        self,
        uuid: str,
        path: str = "",
        user_role: int = ROLE_GUEST,
        user_uuid: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
        success, msg, _ = self.get_by_uuid(
            uuid, user_uuid=user_uuid, user_role=user_role
        )
        if not success:
            return False, msg, None

        try:
            files = self.proj_repo.get_file_tree(uuid, path)
            return True, "文件树获取成功", files
        except FileNotFoundError:
            return False, "路径不存在", None
        except Exception as e:
            return False, f"获取文件树失败: {str(e)}", None

    def get_file_content(
        self,
        uuid: str,
        path: str,
        user_role: int = ROLE_GUEST,
        user_uuid: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[str]]:
        success, msg, _ = self.get_by_uuid(
            uuid, user_uuid=user_uuid, user_role=user_role
        )
        if not success:
            return False, msg, None

        try:
            content = self.proj_repo.get_file_content(uuid, path)
            return True, "文件内容获取成功", content
        except FileNotFoundError:
            return False, "文件不存在", None
        except Exception as e:
            return False, f"读取文件内容失败: {str(e)}", None
