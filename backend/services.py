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