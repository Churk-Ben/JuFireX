from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app: Flask):
    """
    初始化数据库连接并创建表结构.
    """
    db.init_app(app)

    with app.app_context():
        # 导入模型确保它们被注册到 SQLAlchemy
        from backend.data.models.user import User
        from backend.data.seed import seed_admin

        db.create_all()
        seed_admin()
