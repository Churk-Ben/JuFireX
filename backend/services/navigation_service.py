# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 导航服务层, 包含导航项的创建, 更新, 删除, 查询等业务逻辑
# ------------------------------------------------------------

from typing import List, Optional, Tuple

from backend.data import NavigationRepository
from backend.data.models.navigation import Navigation


class NavigationService:
    def __init__(self, nav_repo: NavigationRepository):
        self.nav_repo = nav_repo

    def get_all(
        self, user_uuid: str = None, view_all: bool = False
    ) -> List[Navigation]:
        return self.nav_repo.get_all(user_uuid=user_uuid, view_all=view_all)

    def get_by_uuid(self, uuid: str) -> Optional[Navigation]:
        return self.nav_repo.get_by_uuid(uuid)

    def create(self, data: dict) -> Tuple[bool, str, Optional[Navigation]]:
        try:
            nav = self.nav_repo.add(data)
            return True, "导航创建成功", nav
        except Exception as e:
            return False, f"创建失败: {str(e)}", None

    def update(self, uuid: str, data: dict) -> Tuple[bool, str, Optional[Navigation]]:
        nav = self.nav_repo.update(uuid, data)
        if not nav:
            return False, "导航不存在", None
        return True, "导航更新成功", nav

    def delete(self, uuid: str) -> Tuple[bool, str]:
        success = self.nav_repo.delete(uuid)
        if success:
            return True, "导航删除成功"
        return False, "导航不存在"
