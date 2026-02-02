# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 导航数据仓库, 封装 Navigation 模型的所有数据库操作
# ------------------------------------------------------------

import json
import os
from pathlib import Path
import shutil
from typing import Any, Dict, List, Optional

from sqlalchemy import or_, select

from backend.config import Config
from backend.core.Logger import get_logger
from backend.data.database import db
from backend.data.models.project import Project

logger = get_logger("Repo_Project")


class ProjectRepository:
    def __init__(self):
        self.model = Project

    def _get_project_dir(self, uuid: str) -> Path:
        return Config.PROJECTS_DIR / uuid

    def _save_files(self, uuid: str, data: dict):
        """将项目元数据和README内容保存到项目目录"""
        project_dir = self._get_project_dir(uuid)
        project_dir.mkdir(parents=True, exist_ok=True)

        # 元数据
        metadata = {
            "title": data.get("title", "Untitled Project"),
            "description": data.get("description", ""),
            "tags": data.get("tags", []),
            "url": data.get("url", ""),
            "icon": data.get("icon", ""),
        }

        if isinstance(metadata["tags"], str):
            metadata["tags"] = [
                t.strip() for t in metadata["tags"].split(",") if t.strip()
            ]

        with (project_dir / "metadata.json").open("w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # README
        if "readme" in data:
            with (project_dir / "README.md").open("w", encoding="utf-8") as f:
                f.write(data["readme"])

    def _read_files(self, uuid: str) -> Dict[str, Any]:
        """从项目目录读取元数据和README文件内容"""
        possible_readme_files = [
            "README.md",
            "readme.md",
            "Readme.md",
            "README.markdown",
            "readme.markdown",
            "Readme.markdown",
        ]
        project_dir = self._get_project_dir(uuid)
        metadata_path = project_dir / "metadata.json"
        readme_path = None
        for readme_file in possible_readme_files:
            if (project_dir / readme_file).exists():
                readme_path = project_dir / readme_file
                break

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
                with metadata_path.open("r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    result.update(metadata)
            except Exception:
                logger.warning(f"项目 {uuid} 元数据文件损坏")
                pass

        if readme_path.exists():
            try:
                with readme_path.open("r", encoding="utf-8") as f:
                    result["readme"] = f.read()
            except Exception:
                logger.warning(f"项目 {uuid} README 文件损坏")
                pass

        return result

    def _merge_project_data(self, proj: Project, show_content: bool = True) -> dict:
        proj_dict = proj.to_dict()
        file_data = self._read_files(proj.uuid)
        proj_dict.update(file_data)
        if not show_content:
            proj_dict.pop("readme", None)
        return proj_dict

    def get_all(
        self, user_uuid: Optional[str] = None, view_all: bool = False
    ) -> List[Dict[str, Any]]:
        stmt = select(self.model)

        if not view_all:
            # Public + Own
            if user_uuid:
                stmt = stmt.where(
                    or_(
                        self.model.is_public == True, self.model.owner_uuid == user_uuid
                    )
                )
            else:
                stmt = stmt.filter_by(is_public=True)

        stmt = stmt.order_by(self.model.order.desc(), self.model.created_at.desc())
        projects = db.session.scalars(stmt).all()

        return [self._merge_project_data(p, show_content=False) for p in projects]

    def get_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        stmt = select(self.model).filter_by(uuid=uuid)
        proj = db.session.scalars(stmt).first()
        if not proj:
            return None
        return self._merge_project_data(proj)

    def create(self, data: dict) -> Dict[str, Any]:
        # 提取数据库字段
        db_data = {
            "owner_uuid": data.get("owner_uuid"),
            "is_public": data.get("is_public", True),
            "order": data.get("order", 0),
            "stars": data.get("stars", 0),
        }

        proj = self.model(**db_data)
        db.session.add(proj)
        db.session.commit()

        # 保存文件
        self._save_files(proj.uuid, data)

        return self._merge_project_data(proj)

    def update(self, uuid: str, data: dict) -> Optional[Dict[str, Any]]:
        stmt = select(self.model).filter_by(uuid=uuid)
        proj = db.session.scalars(stmt).first()
        if not proj:
            return None

        # 更新数据库字段
        if "is_public" in data:
            proj.is_public = data["is_public"]
        if "order" in data:
            proj.order = data["order"]
        if "stars" in data:
            proj.stars = data["stars"]

        db.session.commit()

        # 更新文件
        current_file_data = self._read_files(uuid)

        for key in [
            "title",
            "description",
            "tags",
            "url",
            "icon",
            "readme",
            "content",
        ]:
            if key in data:
                current_file_data[key] = data[key]

        self._save_files(uuid, current_file_data)

        return self._merge_project_data(proj)

    def delete(self, uuid: str) -> bool:
        stmt = select(self.model).filter_by(uuid=uuid)
        proj = db.session.scalars(stmt).first()
        if not proj:
            return False

        db.session.delete(proj)
        db.session.commit()

        # 删除项目目录
        project_dir = self._get_project_dir(uuid)
        if project_dir.exists():
            shutil.rmtree(project_dir)

        return True

    def increment_views(self, uuid: str):
        stmt = select(self.model).filter_by(uuid=uuid)
        proj = db.session.scalars(stmt).first()
        if proj:
            proj.views += 1
            db.session.commit()

    def update_stars(self, uuid: str, increment: bool = True):
        stmt = select(self.model).filter_by(uuid=uuid)
        proj = db.session.scalars(stmt).first()
        if proj:
            proj.stars += 1 if increment else -1
            db.session.commit()

    def get_file_tree(self, uuid: str, path: str = "") -> List[Dict[str, Any]]:
        project_root = self._get_project_dir(uuid)
        path = path.lstrip("/\\")
        target_path = (project_root / path).resolve()

        try:
            target_path.relative_to(project_root)
        except ValueError:
            logger.warning(f"获取项目 {uuid} 路径越界: {path}")
            raise FileNotFoundError("Path not found")

        if not target_path.exists():
            logger.warning(f"获取项目 {uuid} 路径不存在: {path}")
            raise FileNotFoundError("Path not found")

        if not target_path.is_dir():
            logger.warning(f"获取项目 {uuid} 路径不是目录: {path}")
            raise NotADirectoryError("Not a directory")

        files = []
        try:
            for entry in os.scandir(target_path):
                files.append(
                    {
                        "name": entry.name,
                        "type": "directory" if entry.is_dir() else "file",
                        "size": entry.stat().st_size if entry.is_file() else 0,
                    }
                )
        except Exception as e:
            logger.error(f"获取项目 {uuid} 路径 {path} 文件列表时出错: {e}")
            raise e

        files.sort(key=lambda x: (x["type"] != "directory", x["name"]))
        return files

    def get_file_content(self, uuid: str, path: str) -> str:
        project_root = self._get_project_dir(uuid)
        path = path.lstrip("/\\")
        target_path = (project_root / path).resolve()

        try:
            target_path.relative_to(project_root)
        except ValueError:
            logger.warning(f"获取项目 {uuid} 路径越界: {path}")
            raise FileNotFoundError("File not found")

        if not target_path.exists() or not target_path.is_file():
            logger.warning(f"获取项目 {uuid} 路径不存在或不是文件: {path}")
            raise FileNotFoundError("File not found")

        if target_path.stat().st_size > 1024 * 1024 * 2:
            size = target_path.stat().st_size / (1024 * 1024)
            logger.warning(f"获取项目 {uuid} 路径 {path} 文件大小超限: {size:.2f}MB")
            raise ValueError("File too large to view")

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except UnicodeDecodeError:
            logger.warning(f"获取项目 {uuid} 路径 {path} 文件: 不支持的编码")
            raise ValueError("Binary file cannot be viewed")
