from typing import List, Dict, Any
from backend.config import Config
from .file_repo import FileRepository


class ProjectRepository(FileRepository[Dict[str, Any]]):
    def __init__(self):
        super().__init__(Config.PROJECTS_DIR)
