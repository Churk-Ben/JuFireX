"""
业务服务层 - 减少代码冗余，提供统一的业务逻辑
"""

import os
import shutil
from typing import Optional, Dict, Any, List, Tuple
from werkzeug.datastructures import FileStorage
from PIL import Image
import requests
from .models import Project, User, db
from .utils import get_project_folder_path, save_file_to_user_data
from .config import Config


class ImageService:
    """图片处理服务"""
    
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    MAX_SIZE = (1920, 1080)
    
    @classmethod
    def validate_image(cls, file_or_url: str) -> bool:
        """验证图片格式和大小"""
        try:
            if file_or_url.startswith('http'):
                # 网络图片验证
                response = requests.head(file_or_url, timeout=5)
                content_type = response.headers.get('content-type', '')
                return content_type.startswith('image/')
            else:
                # 本地文件验证
                ext = os.path.splitext(file_or_url)[1].lower()
                return ext in cls.ALLOWED_EXTENSIONS
        except Exception:
            return False
    
    @classmethod
    def process_project_image(cls, project: Project, image_data: Dict[str, Any]) -> Optional[str]:
        """
        统一处理项目图片
        返回: 新的图片URL或None
        """
        try:
            image_url = image_data.get('image_url')
            if not image_url:
                return None
            
            project_path = get_project_folder_path(project.id, project.created_at)
            if not project_path:
                return None
            
            # index.* 白名单：保持现有文件，不做任何改动
            if image_url.startswith('index.'):
                return image_url
            
            # 删除旧图片
            cls._remove_old_project_images(project_path)
            
            # 处理新图片
            if image_url.startswith('data:image/'):
                return cls._process_data_url_image(image_url, project_path)
            elif image_url.startswith('http'):
                return cls._process_url_image(image_url, project_path)
            elif image_url.startswith('user_data://'):
                return cls._process_user_data_image(image_url, project_path)
            elif image_url.startswith('/user_data/'):
                return cls._process_user_data_legacy(image_url, project_path)
            elif image_url.startswith('file://'):
                return cls._process_file_uri(image_url, project_path)
            
            return None
            
        except Exception as e:
            print(f"Error processing project image: {e}")
            return None

    @classmethod
    def _remove_old_project_images(cls, project_path: str):
        """删除项目文件夹中的旧图片"""
        import glob
        old_images = glob.glob(os.path.join(project_path, "index.*"))
        for old_file in old_images:
            if os.path.isfile(old_file):
                os.remove(old_file)

    # 新增：提供控制器调用的清理接口，避免控制器层自行处理文件
    @classmethod
    def clear_project_image(cls, project: Project) -> None:
        project_path = get_project_folder_path(project.id, project.created_at)
        if not project_path:
            return
        try:
            cls._remove_old_project_images(project_path)
        except Exception:
            # 静默失败，控制器不因清理失败而报错
            pass

    @classmethod
    def _process_data_url_image(cls, data_url: str, project_path: str) -> Optional[str]:
        """处理 data URL 格式的图片"""
        import base64
        import re
        
        match = re.match(r'data:image/(\w+);base64,(.+)', data_url)
        if not match:
            return None
        
        format_name, image_data = match.groups()
        ext = f".{format_name.lower()}"
        
        if ext not in cls.ALLOWED_EXTENSIONS:
            return None
        
        try:
            image_bytes = base64.b64decode(image_data)
            image_path = os.path.join(project_path, f"index{ext}")
            
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            
            # 压缩图片
            cls._compress_image(image_path)
            return f"index{ext}"
            
        except Exception:
            return None

    @classmethod
    def _process_url_image(cls, url: str, project_path: str) -> Optional[str]:
        """处理网络URL图片"""
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            # 从 Content-Type 推断扩展名
            content_type = response.headers.get('content-type', '')
            ext = '.jpg'  # 默认
            if 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            
            image_path = os.path.join(project_path, f"index{ext}")
            
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 压缩图片
            cls._compress_image(image_path)
            return f"index{ext}"
            
        except Exception:
            return None

    @classmethod
    def _process_user_data_image(cls, user_data_url: str, project_path: str) -> Optional[str]:
        """处理用户数据文件图片 (user_data:// 协议)"""
        try:
            user_data_file = user_data_url.replace('user_data://', '')
            user_data_path = os.path.join(
                Config.get_user_avatar_folder(), user_data_file
            )
            
            if not os.path.exists(user_data_path):
                return None
            
            ext = os.path.splitext(user_data_file)[1] or '.jpg'
            image_path = os.path.join(project_path, f"index{ext}")
            
            shutil.copy2(user_data_path, image_path)
            cls._compress_image(image_path)
            return f"index{ext}"
            
        except Exception:
            return None

    @classmethod
    def _process_user_data_legacy(cls, legacy_path: str, project_path: str) -> Optional[str]:
        """处理旧版 '/user_data/...' 形式的图片路径"""
        try:
            user_data_file = legacy_path.replace('/user_data/', '')
            user_data_path = os.path.join(
                Config.get_user_avatar_folder(), user_data_file
            )
            if not os.path.exists(user_data_path):
                return None
            ext = os.path.splitext(user_data_file)[1] or '.jpg'
            image_path = os.path.join(project_path, f"index{ext}")
            shutil.copy2(user_data_path, image_path)
            cls._compress_image(image_path)
            return f"index{ext}"
        except Exception:
            return None

    @classmethod
    def _process_file_uri(cls, file_uri: str, project_path: str) -> Optional[str]:
        """处理本地文件 URI (file://...)"""
        try:
            from urllib.parse import urlparse, unquote
            result = urlparse(file_uri)
            local_path = unquote(result.path)
            # Windows 修正: /C:/... -> C:/...
            if os.name == 'nt' and local_path.startswith('/'):
                local_path = local_path[1:]
            if not os.path.exists(local_path):
                return None
            ext = os.path.splitext(local_path)[1] or '.jpg'
            image_path = os.path.join(project_path, f"index{ext}")
            shutil.copy2(local_path, image_path)
            cls._compress_image(image_path)
            return f"index{ext}"
        except Exception:
            return None

    @classmethod
    def _compress_image(cls, image_path: str):
        """压缩图片"""
        try:
            with Image.open(image_path) as img:
                # 转换RGBA到RGB（如果需要）
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                # 调整大小
                img.thumbnail(cls.MAX_SIZE, Image.Resampling.LANCZOS)
                
                # 保存压缩后的图片
                img.save(image_path, optimize=True, quality=85)
                
        except Exception:
            pass  # 压缩失败不影响主流程


class ValidationService:
    """数据验证服务"""
    
    @staticmethod
    def validate_project_data(data: Dict[str, Any]) -> Tuple[bool, str]:
        """验证项目数据"""
        required_fields = ['title', 'description']
        
        for field in required_fields:
            if not data.get(field, '').strip():
                return False, f"字段 '{field}' 不能为空"
        
        # 标题长度检查
        if len(data['title']) > 100:
            return False, "项目标题不能超过100个字符"
        
        # 描述长度检查
        if len(data['description']) > 500:
            return False, "项目描述不能超过500个字符"
        
        # URL格式检查
        for url_field in ['github_url', 'demo_url']:
            url = data.get(url_field, '').strip()
            if url and not ValidationService._is_valid_url(url):
                return False, f"无效的URL格式: {url_field}"
        
        return True, ""
    
    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """验证URL格式"""
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None


class AuditService:
    """审计日志服务"""
    
    @staticmethod
    def log_user_action(user_id: int, action: str, resource: str = "", details: str = ""):
        """记录用户操作日志"""
        # TODO: 实现到数据库或日志文件
        import logging
        
        logger = logging.getLogger('audit')
        logger.info(f"User {user_id} performed {action} on {resource}. Details: {details}")
    
    @staticmethod
    def log_security_event(event_type: str, user_id: Optional[int] = None, details: str = ""):
        """记录安全事件"""
        import logging
        
        logger = logging.getLogger('security')
        logger.warning(f"Security event: {event_type}. User: {user_id}. Details: {details}")


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
        if not safe.lower().endswith(('.md', '.markdown')):
            safe += '.md'
        return safe

    @staticmethod
    def _is_basename(name: str) -> bool:
        # 防止路径遍历：仅允许纯文件名，不允许包含路径分隔符
        return os.path.basename(name) == name

    @classmethod
    def create_markdown(cls, project: Project, title: str, content: str) -> Tuple[bool, Any]:
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
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, {"filename": safe_name}
        except Exception as e:
            return False, f"创建文档失败: {e}"

    @classmethod
    def upload_markdown(cls, project: Project, filename: str, content: str) -> Tuple[bool, Any]:
        # 与 create_markdown 一致，但参数为 filename（表单传入）
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
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return True, content
        except Exception as e:
            return False, f"读取文件时出错: {e}"

    @classmethod
    def update_markdown(cls, project: Project, filename: str, new_title: Optional[str], content: str) -> Tuple[bool, Any]:
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
            with open(file_path, 'w', encoding='utf-8') as f:
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