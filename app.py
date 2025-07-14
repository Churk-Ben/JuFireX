import os
from datetime import datetime
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash

# 导入配置和模块
from backend.config import Config, ROLE_SUPER_ADMIN, ROLE_GUEST
from backend.models import db, User, Project, StudioInfo, NavCategory
from backend.utils import require_role, generate_csrf_token
from backend.auth import auth_bp
from backend.projects import projects_bp
from backend.navigation import navigation_bp
from backend.admin import admin_bp

# 创建Flask应用
app = Flask(__name__)
app.config.from_object(Config)

# 添加用户头像文件夹配置
app.config["USER_AVATAR_FOLDER"] = Config.get_user_avatar_folder()

# 初始化扩展
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(navigation_bp)
app.register_blueprint(admin_bp)


# 添加CSRF token到模板上下文
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token())


# 添加日期格式化过滤器
@app.template_filter("dateformat")
def dateformat(value, format="%Y-%m-%d %H:%M:%S"):
    if format == "date":
        format = "%Y-%m-%d"
    elif format == "datetime":
        format = "%Y-%m-%d %H:%M:%S"
    return value.strftime(format)


@app.template_filter("format_datetime")
def format_datetime(value, format="%Y-%m-%d %H:%M:%S"):
    """格式化日期时间"""
    if isinstance(value, str):
        return value
    return value.strftime(format)


# 根路由
@app.route("/")
def index():
    # 获取工作室信息
    studio_info = StudioInfo.query.first()

    # 获取特色项目（最多6个）
    featured_projects = Project.query.filter_by(is_featured=True).limit(6).all()

    # 获取当前用户信息
    current_user = None
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])

    return render_template(
        "index.html",
        studio_info=studio_info,
        featured_projects=featured_projects,
        current_user=current_user,
    )


# SocketIO事件处理
@socketio.on("connect")
def handle_connect():
    print(f"用户连接: {session.get('username', '匿名用户')}")
    emit("status", {"msg": f"{session.get('username', '匿名用户')} 已连接"})


@socketio.on("disconnect")
def handle_disconnect():
    print(f"用户断开连接: {session.get('username', '匿名用户')}")


def init_database():
    """初始化数据库和默认数据"""
    with app.app_context():
        # 创建所有表
        db.create_all()

        # 创建默认超级管理员（如果不存在）
        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@jufirestudio.com",
                password_hash=generate_password_hash("admin123"),
                role=ROLE_SUPER_ADMIN,
                is_active=True,
            )
            db.session.add(admin_user)
            print("创建默认超级管理员: admin / admin123")

        # 创建默认工作室信息（如果不存在）
        studio_info = StudioInfo.query.first()
        if not studio_info:
            studio_info = StudioInfo(
                name="JuFire Studio",
                description="一个专注于创新和技术的工作室",
                logo_url="/static/images/logo.png",
                contact_email="contact@jufirestudio.com",
                github_url="https://github.com/jufirestudio",
                website_url="https://jufirestudio.com",
            )
            db.session.add(studio_info)
            print("创建默认工作室信息")

        # 创建默认导航分类（如果不存在）
        default_categories = [
            {"name": "开发工具", "order": 1},
            {"name": "学习资源", "order": 2},
            {"name": "设计工具", "order": 3},
            {"name": "其他资源", "order": 4},
        ]

        for cat_data in default_categories:
            existing_cat = NavCategory.query.filter_by(name=cat_data["name"]).first()
            if not existing_cat:
                category = NavCategory(name=cat_data["name"], order=cat_data["order"])
                db.session.add(category)
                print(f"创建默认导航分类: {cat_data['name']}")

        # 提交所有更改
        db.session.commit()
        print("数据库初始化完成")


if __name__ == "__main__":
    # 初始化数据库
    init_database()

    # 启动应用
    print("启动 JuFire Studio 应用...")
    print("访问地址: http://localhost:5000")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
