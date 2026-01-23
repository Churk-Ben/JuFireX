import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from backend.config import Config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app: Flask):
    db.init_app(app)
    with app.app_context():
        # 导入模型确保它们被注册到 SQLAlchemy
        from backend.data.models.user import User
        from backend.config import ROLE_SUPER_ADMIN

        db.create_all()

        # Create default admin user if not exists
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                email="admin@jufirex.com",
                role=ROLE_SUPER_ADMIN,
                is_active=True,
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

            # Create user folder
            user_folder = Config.PROFILES_DB_PATH.parent / admin.uuid
            os.makedirs(user_folder, exist_ok=True)

            print(f"Default admin user created: admin / admin123 (UUID: {admin.uuid})")
