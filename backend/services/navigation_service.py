# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 导航服务层, 包含导航项的创建, 更新, 删除, 查询等业务逻辑
# ------------------------------------------------------------

from typing import Any, Dict, List, Optional, Tuple

from backend.config import ROLE_ADMIN, ROLE_GUEST
from backend.data import NavigationRepository


class NavigationService:
    def __init__(self, nav_repo: NavigationRepository):
        self.nav_repo = nav_repo

    def get_all(
        self, user_uuid: str = None, user_role: int = ROLE_GUEST, view_all: bool = False
    ) -> List[Dict[str, Any]]:
        # 如果请求查看所有，必须是管理员
        if view_all and user_role < ROLE_ADMIN:
            view_all = False

        navs = self.nav_repo.get_all(user_uuid=user_uuid, view_all=view_all)
        return [nav.to_dict() for nav in navs]

    def get_by_uuid(
        self, uuid: str, user_uuid: str = None, user_role: int = ROLE_GUEST
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        nav = self.nav_repo.get_by_uuid(uuid)
        if not nav:
            return False, "导航不存在", None

        # 这里的鉴权逻辑有点微妙。
        # 如果导航是私有的(有owner_uuid)，那么必须是Owner或Admin。
        # 如果是公共的(owner_uuid is None)，谁都可以看吗？假设是的。

        is_public = nav.owner_uuid is None
        is_admin = user_role >= ROLE_ADMIN
        is_owner = user_uuid and nav.owner_uuid == user_uuid

        if is_public or is_admin or is_owner:
            return True, "获取成功", nav.to_dict()

        return False, "权限不足", None

    def create(
        self, data: dict, user_uuid: str = None, user_role: int = ROLE_GUEST
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        try:
            is_admin = user_role >= ROLE_ADMIN

            # 权限控制 & Owner 赋值逻辑
            if not is_admin:
                # 如果是成员用户, 强制设置 owner_uuid 为自己
                data["owner_uuid"] = user_uuid
            else:
                # 管理员可以指定 owner_uuid, 如果未指定则默认为 None (系统/公共)
                if "owner_uuid" not in data:
                    data["owner_uuid"] = None

            nav = self.nav_repo.add(data)
            return True, "导航创建成功", nav.to_dict()
        except Exception as e:
            return False, f"创建失败: {str(e)}", None

    def update(
        self,
        uuid: str,
        data: dict,
        user_uuid: str = None,
        user_role: int = ROLE_GUEST,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        nav = self.nav_repo.get_by_uuid(uuid)
        if not nav:
            return False, "导航不存在", None

        is_admin = user_role >= ROLE_ADMIN
        # 如果不是管理员, 且不是所有者 -> 拒绝
        if not is_admin and nav.owner_uuid != user_uuid:
            return False, "权限不足", None

        nav = self.nav_repo.update(uuid, data)
        if not nav:
            return False, "导航不存在", None
        return True, "导航更新成功", nav.to_dict()

    def delete(
        self, uuid: str, user_uuid: str = None, user_role: int = ROLE_GUEST
    ) -> Tuple[bool, str]:
        nav = self.nav_repo.get_by_uuid(uuid)
        if not nav:
            return False, "导航不存在"

        is_admin = user_role >= ROLE_ADMIN
        # 如果不是管理员, 且不是所有者 -> 拒绝
        if not is_admin and nav.owner_uuid != user_uuid:
            return False, "权限不足"

        success = self.nav_repo.delete(uuid)
        if success:
            return True, "导航删除成功"
        return False, "导航不存在"
