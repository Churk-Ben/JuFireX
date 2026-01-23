import os
from flask import Flask
from backend.config import Config, ROLE_SUPER_ADMIN
from backend.data.database import db
from backend.data.models.user import User
import random

CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"


def seed_admin():
    """
    如果不存在管理员账户，则创建默认管理员账户。
    """
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@jufirex.com",
            role=ROLE_SUPER_ADMIN,
            is_active=True,
        )
        # 生成随机密码
        init_password = "".join(random.choice(CHARSET) for _ in range(12))
        admin.set_password(init_password)
        db.session.add(admin)
        db.session.commit()

        # Create user folder
        user_folder = Config.PROFILES_DB_PATH.parent / admin.uuid
        os.makedirs(user_folder, exist_ok=True)

        from backend.core.Logger import get_logger

        logger = get_logger(__name__)
        logger.info(f"默认管理员: admin / {init_password} (UUID: {admin.uuid})")


if __name__ == "__main__":
    init_password = "".join(random.choice(CHARSET) for _ in range(12))
    print(f"默认管理员: admin / {init_password}")
