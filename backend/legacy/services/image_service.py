"""图片处理服务 - 提供图片处理相关功能"""

import os
import shutil
import base64
import io
import uuid
from typing import Optional, Dict, Any, List, Tuple, Union
from PIL import Image
import requests
from ..models import Project, User, db
from ..utils import get_project_folder_path, save_file_to_user_data
from ..config import Config


class ImageService:
    """图片处理服务"""

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    MAX_SIZE = (1920, 1080)
    AVATAR_SIZE = (200, 200)

    @classmethod
    def validate_image(
        cls,
        file_or_url: str,
    ) -> bool:
        """验证图片格式和大小"""
        try:
            if file_or_url.startswith("http"):
                # 网络图片验证
                response = requests.head(file_or_url, timeout=5)
                content_type = response.headers.get("content-type", "")
                return content_type.startswith("image/")
            else:
                # 本地文件验证
                ext = os.path.splitext(file_or_url)[1].lower()
                return ext in cls.ALLOWED_EXTENSIONS
        except Exception:
            return False

    @classmethod
    def process_user_avatar(
        cls,
        image_data: Union[bytes, str],
        user_id: int,
        old_avatar_path: Optional[str] = None,
    ) -> Optional[str]:
        """
        处理用户头像
        Args:
            image_data: 图片数据, 可以是bytes或base64字符串
            user_id: 用户ID
            old_avatar_path: 旧头像路径（如果有）
        Returns:
            Optional[str]: 新头像的相对路径, 如果处理失败则返回None
        """
        try:
            user_folder = os.path.join(Config.get_user_avatar_folder(), str(user_id))
            os.makedirs(user_folder, exist_ok=True)

            # 处理输入数据
            if isinstance(image_data, str):
                if "," in image_data:  # base64数据
                    image_data = image_data.split(",")[1]
                img = Image.open(io.BytesIO(base64.b64decode(image_data)))
            else:  # bytes数据
                img = Image.open(io.BytesIO(image_data))

            # 裁剪为正方形
            width, height = img.size
            size = min(width, height)
            left = (width - size) // 2
            top = (height - size) // 2
            img = img.crop((left, top, left + size, top + size))

            # 调整大小
            img = img.resize(cls.AVATAR_SIZE, Image.LANCZOS)

            # 生成文件名和保存
            filename = f"{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(user_folder, filename)

            # 如果是RGBA模式, 转换为RGB
            if img.mode == "RGBA":
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background

            img.save(filepath, "JPEG", quality=95)

            # 清理旧头像
            if old_avatar_path:
                try:
                    old_path = os.path.join(
                        Config.get_user_avatar_folder(), old_avatar_path
                    )
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass

            return os.path.join(str(user_id), filename)

        except Exception as e:
            print(f"用户 {user_id} 头像处理失败: {e}")
            return None

    @classmethod
    def process_project_image(
        cls,
        project: Project,
        image_data: Dict[str, Any],
    ) -> Optional[str]:
        """
        统一处理项目图片
        返回: 新的图片URL或None
        """
        try:
            image_url = image_data.get("image_url")
            if not image_url:
                return None

            project_path = get_project_folder_path(project.id, project.created_at)
            if not project_path:
                return None

            # index.* 白名单：保持现有文件, 不做任何改动
            if image_url.startswith("index."):
                return image_url

            # 删除旧图片
            cls._remove_old_project_images(project_path)

            # 处理新图片
            if image_url.startswith("data:image/"):
                return cls._process_data_url_image(image_url, project_path)
            elif image_url.startswith("http"):
                return cls._process_url_image(image_url, project_path)
            elif image_url.startswith("user_data://"):
                return cls._process_user_data_image(image_url, project_path)
            elif image_url.startswith("/user_data/"):
                return cls._process_user_data_legacy(image_url, project_path)
            elif image_url.startswith("file://"):
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

    # 新增：提供控制器调用的清理接口, 避免控制器层自行处理文件
    @classmethod
    def clear_project_image(cls, project: Project) -> None:
        project_path = get_project_folder_path(project.id, project.created_at)
        if not project_path:
            return
        try:
            cls._remove_old_project_images(project_path)
        except Exception:
            # 静默失败, 控制器不因清理失败而报错
            pass

    @classmethod
    def _process_data_url_image(cls, data_url: str, project_path: str) -> Optional[str]:
        """处理 data URL 格式的图片"""
        import base64
        import re

        match = re.match(r"data:image/(\w+);base64,(.+)", data_url)
        if not match:
            return None

        format_name, image_data = match.groups()
        ext = f".{format_name.lower()}"

        if ext not in cls.ALLOWED_EXTENSIONS:
            return None

        try:
            image_bytes = base64.b64decode(image_data)
            image_path = os.path.join(project_path, f"index{ext}")

            with open(image_path, "wb") as f:
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
            content_type = response.headers.get("content-type", "")
            ext = ".jpg"  # 默认
            if "png" in content_type:
                ext = ".png"
            elif "gif" in content_type:
                ext = ".gif"
            elif "webp" in content_type:
                ext = ".webp"

            image_path = os.path.join(project_path, f"index{ext}")

            with open(image_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # 压缩图片
            cls._compress_image(image_path)
            return f"index{ext}"

        except Exception:
            return None

    @classmethod
    def _process_user_data_image(
        cls, user_data_url: str, project_path: str
    ) -> Optional[str]:
        """处理用户数据文件图片 (user_data:// 协议)"""
        try:
            user_data_file = user_data_url.replace("user_data://", "")
            user_data_path = os.path.join(
                Config.get_user_avatar_folder(), user_data_file
            )

            if not os.path.exists(user_data_path):
                return None

            ext = os.path.splitext(user_data_file)[1] or ".jpg"
            image_path = os.path.join(project_path, f"index{ext}")

            shutil.copy2(user_data_path, image_path)
            cls._compress_image(image_path)
            return f"index{ext}"

        except Exception:
            return None

    @classmethod
    def _process_user_data_legacy(
        cls, legacy_path: str, project_path: str
    ) -> Optional[str]:
        """处理旧版 '/user_data/...' 形式的图片路径"""
        try:
            user_data_file = legacy_path.replace("/user_data/", "")
            user_data_path = os.path.join(
                Config.get_user_avatar_folder(), user_data_file
            )
            if not os.path.exists(user_data_path):
                return None
            ext = os.path.splitext(user_data_file)[1] or ".jpg"
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
            if os.name == "nt" and local_path.startswith("/"):
                local_path = local_path[1:]
            if not os.path.exists(local_path):
                return None
            ext = os.path.splitext(local_path)[1] or ".jpg"
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
                if img.mode == "RGBA":
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background

                # 调整大小
                img.thumbnail(cls.MAX_SIZE, Image.Resampling.LANCZOS)

                # 保存压缩后的图片
                img.save(image_path, optimize=True, quality=85)

        except Exception:
            pass  # 压缩失败不影响主流程