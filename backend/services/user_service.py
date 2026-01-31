# ------------------------------------------------------------
# @author: Churk
# @status: 阶段性完工
# @description: 用户服务层, 包含用户登录, 注册, 注销等业务逻辑
# ------------------------------------------------------------

from typing import Optional, Tuple

from werkzeug.datastructures import FileStorage

from backend.config import Config, ROLE_GUEST
from backend.data import UserRepository
from backend.data.models.user import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login(self, identifier: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        用户登录逻辑
        :param identifier: 邮箱 或 ID
        :param password: 密码
        :return: (是否成功, 消息, 用户对象)
        """
        user = None
        if "@" in identifier:
            user = self.user_repo.get_by_email(identifier)
        elif identifier.isalnum():
            user = self.user_repo.get_by_id(identifier)
        elif "-" in identifier:
            user = self.user_repo.get_by_uuid(identifier)
        else:
            return False, "无效的用户凭证", None

        if not user or not user.check_password(password):
            return False, "用户不存在或密码错误", None

        if not user.is_active:
            return False, "账户已被禁用", None

        return True, f"欢迎回来, {user.username}", user

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

    def rebuild(self, user_uuid: str) -> Tuple[bool, str]:
        """
        重建用户目录
        :param user_uuid: 用户UUID
        :return: (是否成功, 消息)
        """
        user = self.user_repo.get_by_uuid(user_uuid)
        if not user:
            return False, "用户不存在"

        try:
            self.user_repo.rebuild(user)
            return True, "用户目录重建成功"
        except Exception as e:
            return False, f"用户目录重建失败: {str(e)}"

    def get_profile(self, user_uuid: str) -> Optional[User]:
        """获取用户个人信息"""
        if not user_uuid:
            return None
        return self.user_repo.get_by_uuid(user_uuid)

    def get_all_users(self) -> list[User]:
        """获取所有用户"""
        return self.user_repo.get_all()

    def update_avatar(
        self, user_uuid: str, avatar_file: FileStorage
    ) -> Tuple[bool, str, str]:
        """
        更新用户头像
        :param user_uuid: 用户UUID
        :param avatar_file: 上传的文件对象 (Werkzeug FileStorage)
        :return: (是否成功, 消息, 头像文件名)
        """
        user = self.user_repo.get_by_uuid(user_uuid)
        if not user:
            return False, "用户不存在", ""

        # 读取文件数据
        file_data = avatar_file.read()
        filename = "avatar.png"
        if avatar_file.filename and "." in avatar_file.filename:
            ext = avatar_file.filename.rsplit(".", 1)[1].lower()
            if ext in ["jpg", "jpeg", "png", "gif"]:
                filename = f"avatar.{ext}"

        try:
            size_kb = self.user_repo.save_avatar(user, file_data, filename=filename)
            if size_kb > 1024:
                # 从默认文件夹还原为默认头像
                default_avatar_path = Config.DEFAULTS_DIR / "avatar.png"
                with default_avatar_path.open("rb") as f:
                    default_avatar_data = f.read()
                self.user_repo.save_avatar(user, default_avatar_data, filename=filename)
                return False, "?你给我喂了什么?", ""
            return True, "头像更新成功", filename
        except Exception as e:
            return False, f"头像保存失败: {str(e)}", ""
