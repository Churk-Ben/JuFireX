import os
from datetime import datetime

# 用户角色常量
ROLE_GUEST = 0
ROLE_MEMBER = 1
ROLE_ADMIN = 2
ROLE_SUPER_ADMIN = 3

ROLE_NAMES = {
    ROLE_GUEST: "游客",
    ROLE_MEMBER: "成员",
    ROLE_ADMIN: "管理员",
    ROLE_SUPER_ADMIN: "超级管理员",
}


# Flask配置
class Config:
    SECRET_KEY = "your-secret-key-here"
    SQLALCHEMY_DATABASE_URI = "sqlite:///studio.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_user_avatar_folder():
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "user_data"
        )
