# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 用户数据仓库, 封装 User 模型的所有数据库操作
# ------------------------------------------------------------

import io
import os
from pathlib import Path
import shutil
from typing import List, Optional, Union

from PIL import Image
from sqlalchemy import select

from backend.config import Config
from backend.data.database import db
from backend.data.models.user import User


class UserRepository:
    """
    用户数据仓库, 封装 User 模型的所有数据库操作
    """

    def __init__(self):
        self.model = User

    def get_by_id(self, user_id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        return db.session.get(self.model, user_id)

    def get_by_username(self, username: str) -> List[User]:
        """
        根据用户名获取用户列表.
        注意: 由于用户名在模型定义中不是唯一的,
        可能有多个用户拥有相同的用户名, 因此返回列表.
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
        """添加新用户, 并初始化用户目录"""
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
        """删除用户, 并清理用户目录"""
        db.session.delete(user)
        if commit:
            db.session.commit()
            self._remove_user_directory(user)

    def rebuild(self, user: User) -> None:
        """重建用户文件夹, 用于用户数据意外删除或损坏"""
        if user:
            self._remove_user_directory(user)
            self._ensure_user_directory(user)

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

    # --- 头像管理方法 ---

    def save_avatar(
        self, user: User, image: bytes, filename: str = "avatar.png"
    ) -> int:
        """
        保存用户头像到用户目录.
        :param user: 用户对象
        :param image: 二进制数据
        :param filename: 文件名 (默认为 avatar.png)
        :return: 头像文件的大小 (千字节)
        """
        self._ensure_user_directory(user)
        user_dir = self._get_user_dir(user)
        file_path = user_dir / filename

        with open(file_path, "wb") as f:
            f.write(image)

        return file_path.stat().st_size / 1024
