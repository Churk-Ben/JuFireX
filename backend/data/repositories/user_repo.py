from typing import Optional, List, Union
from pathlib import Path
import os
import shutil
import io
from PIL import Image
from sqlalchemy import select
from backend.data.database import db
from backend.data.models.user import User
from backend.config import Config


class UserRepository:
    """
    用户数据仓库，封装 User 模型的所有数据库操作以及用户相关的文件存储操作（如头像）。
    """

    def __init__(self):
        self.model = User

    def get_by_id(self, user_id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        return db.session.get(self.model, user_id)

    def get_by_username(self, username: str) -> List[User]:
        """
        根据用户名获取用户列表。
        注意：由于用户名在模型定义中不是唯一的 (unique=False)，
        可能有多个用户拥有相同的用户名，因此返回列表。
        """
        stmt = select(self.model).filter_by(username=username)
        return list(db.session.scalars(stmt).all())

    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        stmt = select(self.model).filter_by(email=email)
        return db.session.scalars(stmt).first()

    def get_by_uuid(self, uuid: str) -> Optional[User]:
        """根据 UUID 获取用户"""
        stmt = select(self.model).filter_by(uuid=uuid)
        return db.session.scalars(stmt).first()

    def get_all(self) -> List[User]:
        """获取所有用户"""
        stmt = select(self.model)
        return list(db.session.scalars(stmt).all())

    def get_count(self) -> int:
        """获取用户总数"""
        return self.model.query.count()

    def add(self, user: User, commit: bool = True) -> User:
        """添加新用户，并初始化用户目录"""
        db.session.add(user)
        if commit:
            db.session.commit()
            self._ensure_user_directory(user)
        return user

    def save(self, user: User = None, commit: bool = True) -> None:
        """保存更改"""
        if user:
            db.session.add(user)
        if commit:
            db.session.commit()

    def delete(self, user: User, commit: bool = True) -> None:
        """删除用户，并清理用户目录"""
        db.session.delete(user)
        if commit:
            db.session.commit()
            self._remove_user_directory(user)

    # --- 文件管理方法 ---

    def _get_user_dir(self, user: User) -> Path:
        """获取用户专属数据目录"""
        # 假设所有用户数据都在 profiles/UUID/ 下
        return Config.PROFILES_DB_PATH.parent / user.uuid

    def _ensure_user_directory(self, user: User) -> None:
        """确保用户目录存在"""
        user_dir = self._get_user_dir(user)
        os.makedirs(user_dir, exist_ok=True)

    def _remove_user_directory(self, user: User) -> None:
        """删除用户目录及其内容"""
        user_dir = self._get_user_dir(user)
        if user_dir.exists():
            shutil.rmtree(user_dir)

    def save_avatar(
        self, user: User, image: Union[Image.Image, bytes], filename: str = "avatar.png"
    ) -> Path:
        """
        保存用户头像到用户目录。
        :param user: 用户对象
        :param image: Pillow Image 对象或二进制数据
        :param filename: 文件名（默认为 avatar.png）
        :return: 头像文件的绝对路径
        """
        self._ensure_user_directory(user)
        user_dir = self._get_user_dir(user)
        file_path = user_dir / filename

        # 处理图像数据
        if isinstance(image, bytes):
            img_obj = Image.open(io.BytesIO(image))
        else:
            img_obj = image

        # 保存图像
        # 如果 filename 是 .png 结尾，Pillow 会自动保存为 PNG 格式
        # 这里我们不强制转换格式，而是信任 Pillow 根据文件扩展名处理
        # 但通常建议标准化头像格式（如 PNG）
        img_obj.save(file_path)

        return file_path

    def get_avatar_path(
        self, user: User, filename: str = "avatar.png"
    ) -> Optional[Path]:
        """
        获取用户头像文件路径。
        :return: 如果文件存在返回 Path，否则返回 None
        """
        user_dir = self._get_user_dir(user)
        file_path = user_dir / filename
        if file_path.exists():
            return file_path
        return None

    def get_avatar_image(
        self, user: User, filename: str = "avatar.png"
    ) -> Optional[Image.Image]:
        """
        获取用户头像的 Pillow Image 对象。
        :return: 如果文件存在返回 Image 对象，否则返回 None
        """
        path = self.get_avatar_path(user, filename)
        if path:
            return Image.open(path)
        return None
