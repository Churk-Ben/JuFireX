from typing import List, Optional, Tuple
from backend.data import ProjectRepository
from backend.data.models.project import Project

class ProjectService:
    def __init__(self, proj_repo: ProjectRepository):
        self.proj_repo = proj_repo

    def get_all(self, public_only: bool = False) -> List[Project]:
        return self.proj_repo.get_all(public_only)

    def get_by_uuid(self, uuid: str) -> Optional[Project]:
        return self.proj_repo.get_by_uuid(uuid)

    def create(self, data: dict) -> Tuple[bool, str, Optional[Project]]:
        try:
            proj = self.proj_repo.create(data)
            return True, "项目创建成功", proj
        except Exception as e:
            return False, f"创建失败: {str(e)}", None

    def update(self, uuid: str, data: dict) -> Tuple[bool, str, Optional[Project]]:
        proj = self.proj_repo.update(uuid, data)
        if not proj:
            return False, "项目不存在", None
        return True, "项目更新成功", proj

    def delete(self, uuid: str) -> Tuple[bool, str]:
        success = self.proj_repo.delete(uuid)
        if success:
            return True, "项目删除成功"
        return False, "项目不存在"
