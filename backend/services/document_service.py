"""项目文档处理服务 - 提供文档处理相关功能"""

import os
from typing import Optional, Dict, Any, Tuple
from ..models import Project
from ..utils import get_project_folder_path


class DocumentService:
    """项目文档处理服务"""

    @staticmethod
    def _get_project_docs_path(project: Project) -> Optional[str]:
        try:
            project_docs_path = get_project_folder_path(project.id, project.created_at)
            if not project_docs_path or not os.path.exists(project_docs_path):
                return None
            return project_docs_path
        except Exception:
            return None

    @staticmethod
    def _sanitize_md_name(name: str) -> Optional[str]:
        from werkzeug.utils import secure_filename

        if not name:
            return None
        safe = secure_filename(name)
        if not safe:
            return None
        if not safe.lower().endswith((".md", ".markdown")):
            safe += ".md"
        return safe

    @staticmethod
    def _is_basename(name: str) -> bool:
        # 防止路径遍历：仅允许纯文件名, 不允许包含路径分隔符
        return os.path.basename(name) == name

    @classmethod
    def create_markdown(
        cls, project: Project, title: str, content: str
    ) -> Tuple[bool, Any]:
        project_docs_path = cls._get_project_docs_path(project)
        if not project_docs_path:
            return False, "该项目文档空间不存在"

        safe_name = cls._sanitize_md_name(title)
        if not safe_name:
            return False, "无效的文档标题"

        file_path = os.path.join(project_docs_path, safe_name)
        if os.path.exists(file_path):
            return False, "同名文档已存在"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True, {"filename": safe_name}
        except Exception as e:
            return False, f"创建文档失败: {e}"

    @classmethod
    def upload_markdown(
        cls, project: Project, filename: str, content: str
    ) -> Tuple[bool, Any]:
        # 与 create_markdown 一致, 但参数为 filename（表单传入）
        return cls.create_markdown(project, filename, content)

    @classmethod
    def read_markdown(cls, project: Project, filename: str) -> Tuple[bool, Any]:
        project_docs_path = cls._get_project_docs_path(project)
        if not project_docs_path:
            return False, "该项目文档空间不存在"
        if not filename or not cls._is_basename(filename):
            return False, "无效的文件名"

        file_path = os.path.join(project_docs_path, filename)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return False, "文档不存在"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return True, content
        except Exception as e:
            return False, f"读取文件时出错: {e}"

    @classmethod
    def update_markdown(
        cls, project: Project, filename: str, new_title: Optional[str], content: str
    ) -> Tuple[bool, Any]:
        project_docs_path = cls._get_project_docs_path(project)
        if not project_docs_path:
            return False, "该项目文档空间不存在"
        if not filename or not cls._is_basename(filename):
            return False, "无效的文件名"

        file_path = os.path.join(project_docs_path, filename)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return False, f"文件 {filename} 不存在"

        # 保存内容
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            return False, f"更新文档失败: {e}"

        # 重命名（如需要）
        if new_title and new_title.strip():
            safe_new_name = cls._sanitize_md_name(new_title)
            if not safe_new_name:
                return False, "无效的文档标题"
            rename_needed = filename != safe_new_name
            new_file_path = os.path.join(project_docs_path, safe_new_name)
            if rename_needed:
                if os.path.exists(new_file_path):
                    return False, "同名文档已存在"
                try:
                    os.rename(file_path, new_file_path)
                    return True, {"filename": safe_new_name, "renamed": True}
                except Exception as e:
                    return False, f"重命名失败: {e}"
        # 未重命名
        return True, {"filename": filename, "renamed": False}

    @classmethod
    def delete_markdown(cls, project: Project, filename: str) -> Tuple[bool, Any]:
        project_docs_path = cls._get_project_docs_path(project)
        if not project_docs_path:
            return False, "该项目文档空间不存在"
        if not filename or not cls._is_basename(filename):
            return False, "无效的文件名"

        file_path = os.path.join(project_docs_path, filename)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return False, f"文件 {filename} 不存在"

        try:
            os.remove(file_path)
            return True, None
        except Exception as e:
            return False, f"删除文档失败: {e}"