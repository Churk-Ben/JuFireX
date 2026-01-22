import os
from datetime import datetime
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
dotenv_path = os.path.join(
    PROJECT_ROOT,
    ".env",
)
load_dotenv(dotenv_path)


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
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "Q2h1cmtCZW4",
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///studio.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_user_avatar_folder():
        return os.path.join(
            PROJECT_ROOT,
            "user_data",
        )

    @staticmethod
    def get_projects_folder():
        return os.path.join(
            PROJECT_ROOT,
            "projects",
        )
