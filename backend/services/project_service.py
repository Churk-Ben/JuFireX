import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from backend.config import Config, ROLE_ADMIN, ROLE_GUEST
from backend.data import ProjectRepository


class ProjectService:
    def __init__(self, proj_repo: ProjectRepository):
        self.proj_repo = proj_repo

    def get_all(
        self, user_role: int = ROLE_GUEST, user_uuid: Optional[str] = None, view_all: bool = False
    ) -> List[Dict[str, Any]]:
        # If view_all is requested, it must be an Admin
        if view_all and user_role < ROLE_ADMIN:
            view_all = False

        # If view_all is True (and user is Admin), public_only is False.
        # Otherwise, public_only is True (unless we want to show private items owned by user).
        public_only = not view_all
        return self.proj_repo.get_all(public_only=public_only, owner_uuid=user_uuid)

    def get_by_uuid(
        self, uuid: str, user_role: int = ROLE_GUEST, user_uuid: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        project = self.proj_repo.get_by_uuid(uuid)
        if not project:
            return False, "Project not found", None

        # Check permissions
        is_public = project.get("is_public", False)
        owner_uuid = project.get("owner_uuid")
        
        if is_public:
            return True, "Success", project
        
        if user_role >= ROLE_ADMIN:
            return True, "Success", project
            
        if user_uuid and owner_uuid == user_uuid:
            return True, "Success", project

        return False, "Permission denied", None

    def create(
        self, data: dict, user_uuid: str, user_role: int = ROLE_GUEST
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        if user_role < ROLE_ADMIN:
            return False, "Permission denied", None

        data["owner_uuid"] = user_uuid
        try:
            proj = self.proj_repo.create(data)
            return True, "Project created successfully", proj
        except Exception as e:
            return False, f"Creation failed: {str(e)}", None

    def update(
        self, uuid: str, data: dict, user_role: int = ROLE_GUEST, user_uuid: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        success, msg, project = self.get_by_uuid(uuid, user_role, user_uuid)
        if not success:
            return False, msg, None
            
        if user_role < ROLE_ADMIN and project.get("owner_uuid") != user_uuid:
             return False, "Permission denied", None

        proj = self.proj_repo.update(uuid, data)
        if not proj:
            return False, "Project not found", None
        return True, "Project updated successfully", proj

    def delete(self, uuid: str, user_role: int = ROLE_GUEST, user_uuid: Optional[str] = None) -> Tuple[bool, str]:
        success, msg, project = self.get_by_uuid(uuid, user_role, user_uuid)
        if not success:
            return False, msg

        if user_role < ROLE_ADMIN and project.get("owner_uuid") != user_uuid:
             return False, "Permission denied"

        if self.proj_repo.delete(uuid):
            return True, "Project deleted successfully"
        return False, "Project not found"

    def get_file_tree(
        self, uuid: str, path: str = "", user_role: int = ROLE_GUEST, user_uuid: Optional[str] = None
    ) -> Tuple[bool, str, Optional[List[Dict[str, Any]]]]:
        success, msg, _ = self.get_by_uuid(uuid, user_role, user_uuid)
        if not success:
            return False, msg, None

        project_root = Config.PROJECTS_DIR / uuid
        path = path.lstrip("/\\")
        target_path = (project_root / path).resolve()
        
        try:
            target_path.relative_to(project_root)
        except ValueError:
             return False, "Invalid path", None
             
        if not target_path.exists():
             return False, "Path not found", None
             
        if not target_path.is_dir():
             return False, "Not a directory", None

        files = []
        try:
            for entry in os.scandir(target_path):
                files.append({
                    "name": entry.name,
                    "type": "directory" if entry.is_dir() else "file",
                    "size": entry.stat().st_size if entry.is_file() else 0,
                })
        except Exception as e:
            return False, f"Error listing files: {str(e)}", None
            
        files.sort(key=lambda x: (x["type"] != "directory", x["name"]))
        
        return True, "Success", files

    def get_file_content(
        self, uuid: str, path: str, user_role: int = ROLE_GUEST, user_uuid: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        success, msg, _ = self.get_by_uuid(uuid, user_role, user_uuid)
        if not success:
            return False, msg, None

        project_root = Config.PROJECTS_DIR / uuid
        path = path.lstrip("/\\")
        target_path = (project_root / path).resolve()
        
        try:
            target_path.relative_to(project_root)
        except ValueError:
             return False, "Invalid path", None

        if not target_path.exists() or not target_path.is_file():
             return False, "File not found", None
             
        try:
            if target_path.stat().st_size > 1024 * 1024:
                return False, "File too large to view", None
                
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            return True, "Success", content
        except UnicodeDecodeError:
             return False, "Binary file cannot be viewed", None
        except Exception as e:
            return False, f"Error reading file: {str(e)}", None
