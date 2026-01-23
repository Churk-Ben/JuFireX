from typing import List, Dict
from ...config import Config
from .file_repo import FileRepository


class ProjectRepository(FileRepository):
    def __init__(self):
        super().__init__(Config.PROJECTS_DIR)

    def get_featured_projects(self) -> List[Dict]:
        all_projects = self.list_items()
        return [p for p in all_projects if p.get("is_featured", False)]

    def get_by_author(self, author_id: int) -> List[Dict]:
        all_projects = self.list_items()
        return [p for p in all_projects if p.get("author_id") == author_id]
