# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 博客数据仓库, 封装 Blog 模型的所有数据库操作
# ------------------------------------------------------------

import json
from pathlib import Path
import shutil
from typing import Any, Dict, List, Optional

from sqlalchemy import or_, select

from backend.config import Config
from backend.core.Logger import get_logger
from backend.data.database import db
from backend.data.models.blog import Blog

logger = get_logger("Repo_Blog")


class BlogRepository:
    """
    博客数据仓库, 封装 Blog 模型的所有数据库操作
    """

    def __init__(self):
        self.model = Blog

    def _get_blog_dir(self, uuid: str) -> Path:
        return Config.BLOGS_DIR / uuid

    def _ensure_blog_dir(self, uuid: str):
        path = self._get_blog_dir(uuid)
        path.mkdir(parents=True, exist_ok=True)

    def _save_files(self, uuid: str, data: Dict[str, Any]):
        self._ensure_blog_dir(uuid)
        blog_dir = self._get_blog_dir(uuid)

        # 元数据
        metadata = {
            "title": data.get("title", ""),
            "summary": data.get("summary", ""),
            "tags": data.get("tags", []),
            "cover_image": data.get("cover_image", ""),
            "author_name": data.get("author_name", ""),
        }

        if isinstance(metadata["tags"], str):
            metadata["tags"] = [
                t.strip() for t in metadata["tags"].split(",") if t.strip()
            ]

        with (blog_dir / "metadata.json").open("w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # 内容
        content = data.get("content", "")

        with (blog_dir / "article.md").open("w", encoding="utf-8") as f:
            f.write(content)

    def _read_files(self, uuid: str) -> Dict[str, Any]:
        blog_dir = self._get_blog_dir(uuid)
        metadata_path = blog_dir / "metadata.json"
        content_path = blog_dir / "article.md"

        result = {}

        if metadata_path.exists():
            try:
                with metadata_path.open("r", encoding="utf-8") as f:
                    result.update(json.load(f))
            except Exception:
                pass

        if content_path.exists():
            try:
                with content_path.open("r", encoding="utf-8") as f:
                    result["content"] = f.read()
            except Exception:
                pass

        return result

    def _merge_blog_data(self, blog: Blog, show_content: bool = True) -> Dict[str, Any]:
        base_data = blog.to_dict()
        file_data = self._read_files(blog.uuid)
        if not show_content:
            # 过滤掉 content 字段, 这是为了防止渲染全部文章时获取过多内容, 拖慢响应时间
            file_data.pop("content", None)

        return {**base_data, **file_data}

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

        stmt = stmt.order_by(self.model.created_at.desc())
        blogs = db.session.scalars(stmt).all()

        return [self._merge_blog_data(b, show_content=False) for b in blogs]

    def get_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        stmt = select(self.model).filter_by(uuid=uuid)
        blog = db.session.scalars(stmt).first()
        if not blog:
            return None
        return self._merge_blog_data(blog)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # 数据库字段
        db_data = {
            "owner_uuid": data.get("owner_uuid"),
            "is_public": data.get("is_public", True),
        }

        blog = self.model(**db_data)
        db.session.add(blog)
        db.session.commit()

        # 保存文件
        self._save_files(blog.uuid, data)

        return self._merge_blog_data(blog)

    def update(self, uuid: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        stmt = select(self.model).filter_by(uuid=uuid)
        blog = db.session.scalars(stmt).first()
        if not blog:
            return None

        # 更新数据库字段
        if "is_public" in data:
            blog.is_public = data["is_public"]

        db.session.commit()

        # 更新文件 (合并现有内容)
        current_data = self._read_files(uuid)

        # 更新元数据/内容字段
        for key in [
            "title",
            "summary",
            "tags",
            "cover_image",
            "author_name",
            "content",
        ]:
            if key in data:
                current_data[key] = data[key]

        self._save_files(uuid, current_data)

        return self._merge_blog_data(blog)

    def delete(self, uuid: str) -> bool:
        stmt = select(self.model).filter_by(uuid=uuid)
        blog = db.session.scalars(stmt).first()
        if not blog:
            return False

        db.session.delete(blog)
        db.session.commit()

        # 删除文件
        blog_dir = self._get_blog_dir(uuid)
        if blog_dir.exists():
            shutil.rmtree(blog_dir)

        return True

    def increment_views(self, uuid: str):
        stmt = select(self.model).filter_by(uuid=uuid)
        blog = db.session.scalars(stmt).first()
        if blog:
            blog.views += 1
            db.session.commit()
