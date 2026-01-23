from typing import Optional, Dict, Any, Tuple
from flask import session
from werkzeug.datastructures import FileStorage

from backend.data import UserRepository
from backend.data.models.user import User
from backend.config import ROLE_GUEST, ROLE_MEMBER


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login(self, identifier: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        用户登录逻辑
        :param identifier: 邮箱或UUID
        :param password: 密码
        :return: (是否成功, 消息, 用户对象)
        """
        user = None
        # 简单判断是否为邮箱
        if "@" in identifier:
            user = self.user_repo.get_by_email(identifier)
        else:
            # 尝试作为UUID查找
            user = self.user_repo.get_by_uuid(identifier)

        if not user:
            return False, "用户不存在或密码错误", None

        if not user.check_password(password):
            return False, "用户不存在或密码错误", None

        if not user.is_active:
            return False, "账户已被禁用", None

        # 登录成功, 设置 Session
        session["user_id"] = user.id
        session["role"] = user.role
        session.permanent = True

        return True, "登录成功", user

    def logout(self) -> None:
        """注销当前用户"""
        session.clear()

    def register(
        self, username: str, email: str, password: str
    ) -> Tuple[bool, str, Optional[User]]:
        """
        用户注册逻辑
        :return: (是否成功, 消息, 新用户对象)
        """
        # 检查邮箱是否已存在
        if self.user_repo.get_by_email(email):
            return False, "该邮箱已被注册", None

        new_user = User(
            username=username,
            email=email,
            role=ROLE_GUEST,
            is_active=True,
        )
        new_user.set_password(password)
        self.user_repo.add(new_user)

        return True, "注册成功", new_user

    def get_current_user(self) -> Optional[User]:
        """获取当前登录用户"""
        user_id = session.get("user_id")
        if not user_id:
            return None
        return self.user_repo.get_by_id(user_id)

    def update_avatar(
        self, user_id: int, avatar_file: FileStorage
    ) -> Tuple[bool, str, str]:
        """
        更新用户头像
        :param user_id: 用户ID
        :param avatar_file: 上传的文件对象 (Werkzeug FileStorage)
        :return: (是否成功, 消息, 头像URL/路径)
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False, "用户不存在", ""

        # 读取文件数据
        file_data = avatar_file.read()

        # 调用 repo 保存头像 (Repo 会自动处理为 Pillow 对象或直接保存)
        # 假设文件名使用默认的 avatar.png, 或者根据上传文件后缀
        filename = "avatar.png"
        if avatar_file.filename and "." in avatar_file.filename:
            ext = avatar_file.filename.rsplit(".", 1)[1].lower()
            if ext in ["jpg", "jpeg", "png", "gif"]:
                filename = f"avatar.{ext}"

        try:
            saved_path = self.user_repo.save_avatar(user, file_data, filename=filename)
            return True, "头像更新成功", filename
        except Exception as e:
            return False, f"头像保存失败: {str(e)}", ""
