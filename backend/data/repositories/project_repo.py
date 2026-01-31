# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 导航数据仓库, 封装 Navigation 模型的所有数据库操作
# ------------------------------------------------------------

import json
from pathlib import Path
import shutil
from typing import Any, Dict, List, Optional

from sqlalchemy import select

from backend.config import Config
from backend.data.database import db
from backend.data.models.project import Project


class ProjectRepository:
    def __init__(self):
        self.model = Project

    def _get_project_dir(self, uuid: str) -> Path:
        return Config.PROJECTS_DIR / uuid

    def _read_files(self, uuid: str) -> Dict[str, Any]:
        """Read metadata and readme content from file system"""
        project_dir = self._get_project_dir(uuid)
        metadata_path = project_dir / "metadata.json"
        readme_path = project_dir / "README.md"

        result = {
            "title": "Untitled Project",
            "description": "",
            "tags": [],
            "url": "",
            "icon": "",
            "readme": "",
        }

        if metadata_path.exists():
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    result.update(metadata)
            except Exception:
                pass

        if readme_path.exists():
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    result["readme"] = f.read()
            except Exception:
                pass

        return result

    def _save_files(self, uuid: str, data: dict):
        """Save metadata and readme to file system"""
        project_dir = self._get_project_dir(uuid)
        project_dir.mkdir(parents=True, exist_ok=True)

        # Extract metadata fields
        metadata = {
            "title": data.get("title", "Untitled Project"),
            "description": data.get("description", ""),
            "tags": data.get("tags", []),
            "url": data.get("url", ""),
            "icon": data.get("icon", ""),
        }

        # Handle tags if they are string (legacy compatibility)
        if isinstance(metadata["tags"], str):
            metadata["tags"] = [
                t.strip() for t in metadata["tags"].split(",") if t.strip()
            ]

        with open(project_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # Save README if provided
        if "readme" in data:
            with open(project_dir / "README.md", "w", encoding="utf-8") as f:
                f.write(data["readme"])
        elif "content" in data:  # Compatible with old "content" field
            with open(project_dir / "README.md", "w", encoding="utf-8") as f:
                f.write(data["content"])

    def get_all(
        self, public_only: bool = False, owner_uuid: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        stmt = select(self.model)

        if public_only:
            # If public_only is requested, we strictly return public items
            # If owner_uuid is provided, we ALSO include private items owned by them
            if owner_uuid:
                stmt = stmt.filter(
                    (self.model.is_public == True)
                    | (self.model.owner_uuid == owner_uuid)
                )
            else:
                stmt = stmt.filter_by(is_public=True)

        stmt = stmt.order_by(self.model.order.desc(), self.model.created_at.desc())
        projects = db.session.scalars(stmt).all()

        results = []
        for p in projects:
            p_dict = p.to_dict()
            file_data = self._read_files(p.uuid)
            p_dict.update(file_data)
            results.append(p_dict)

        return results

    def get_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        stmt = select(self.model).filter_by(uuid=uuid)
        proj = db.session.scalars(stmt).first()
        if not proj:
            return None

        # Increment views
        proj.views += 1
        db.session.commit()

        p_dict = proj.to_dict()
        file_data = self._read_files(uuid)
        p_dict.update(file_data)
        return p_dict

    def create(self, data: dict) -> Dict[str, Any]:
        # Extract DB fields
        db_data = {
            "owner_uuid": data.get("owner_uuid"),
            "is_public": data.get("is_public", True),
            "order": data.get("order", 0),
            "stars": data.get("stars", 0),
        }

        proj = self.model(**db_data)
        db.session.add(proj)
        db.session.commit()

        # Save files
        self._save_files(proj.uuid, data)

        return self.get_by_uuid(proj.uuid)

    def update(self, uuid: str, data: dict) -> Optional[Dict[str, Any]]:
        proj = db.session.scalars(select(self.model).filter_by(uuid=uuid)).first()
        if not proj:
            return None

        # Update DB fields
        if "is_public" in data:
            proj.is_public = data["is_public"]
        if "order" in data:
            proj.order = data["order"]
        if "stars" in data:
            proj.stars = data["stars"]

        db.session.commit()

        # Update files
        current_file_data = self._read_files(uuid)

        for k, v in data.items():
            if k in [
                "title",
                "description",
                "tags",
                "url",
                "icon",
                "readme",
                "content",
            ]:
                current_file_data[k] = v

        if "content" in data:
            current_file_data["readme"] = data["content"]

        self._save_files(uuid, current_file_data)

        return self.get_by_uuid(uuid)

    def delete(self, uuid: str) -> bool:
        proj = db.session.scalars(select(self.model).filter_by(uuid=uuid)).first()
        if not proj:
            return False

        db.session.delete(proj)
        db.session.commit()

        # Delete directory
        project_dir = self._get_project_dir(uuid)
        if project_dir.exists():
            shutil.rmtree(project_dir)

        return True
