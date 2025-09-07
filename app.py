import os
from datetime import datetime
from flask import Flask, render_template, session, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash

# 导入配置和模块
from backend.config import Config, ROLE_SUPER_ADMIN, ROLE_GUEST, ROLE_MEMBER, ROLE_ADMIN
from backend.models import (
    db,
    User,
    Project,
    StudioInfo,
    NavCategory,
    NavItem,
    HiddenNavItem,
)
from backend.utils import require_role, generate_csrf_token
from backend.auth import auth_bp
from backend.projects import projects_bp
from backend.navigation import navigation_bp
from backend.admin import admin_bp
from backend.errors import errors_bp

# 创建Flask应用
app = Flask(__name__)
app.config.from_object(Config)

# 添加用户头像文件夹配置
app.config["USER_AVATAR_FOLDER"] = Config.get_user_avatar_folder()
# 添加项目文件夹配置
app.config["PROJECTS_FOLDER"] = Config.get_projects_folder()

# 添加用户数据文件夹配置
app.config["USER_DATA_FOLDER"] = os.path.join(app.root_path, "user_data")

# 确保 USER_DATA_FOLDER 存在
if not os.path.exists(app.config["USER_DATA_FOLDER"]):
    os.makedirs(app.config["USER_DATA_FOLDER"])

# 初始化扩展
db.init_app(app)
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(navigation_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(errors_bp)


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
        "pages/index.html",
        studio_info=studio_info,
        featured_projects=featured_projects,
        current_user=current_user,
    )


# 注册错误处理器
from backend.errors import register_error_handlers
register_error_handlers(app)


# SocketIO事件处理
@socketio.on("connect")
def handle_connect():
    username = session.get('username', 'Anonymous')
    print(f"用户连接: {username} (Session ID: {request.sid})")
    emit("status", {"msg": f"{username} 已连接", "type": "success"})


@socketio.on("disconnect")
def handle_disconnect():
    username = session.get('username', 'Anonymous')
    print(f"用户断开连接: {username} (Session ID: {request.sid})")


@socketio.on_error_default
def default_error_handler(e):
    print(f"Socket.IO错误: {e}")
    emit("error", {"msg": "连接出现错误", "type": "error"})


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
                logo_url="",
                contact_email="contact@jufirestudio.com",
                github_url="https://github.com/jufirestudio",
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

        created_categories = {}
        for cat_data in default_categories:
            existing_cat = NavCategory.query.filter_by(name=cat_data["name"]).first()
            if not existing_cat:
                category = NavCategory(
                    name=cat_data["name"],
                    order=cat_data["order"],
                    created_by=admin_user.id,
                )
                db.session.add(category)
                db.session.flush()  # 获取ID
                created_categories[cat_data["name"]] = category
                print(f"创建默认导航分类: {cat_data['name']}")
            else:
                created_categories[cat_data["name"]] = existing_cat

        # 创建默认导航项（如果不存在）
        default_nav_items = [
            {
                "title": "GitHub",
                "url": "https://github.com",
                "description": "全球最大的代码托管平台",
                "icon": "fab fa-github",
                "category": "开发工具",
                "order": 1,
            },
            {
                "title": "Stack Overflow",
                "url": "https://stackoverflow.com",
                "description": "程序员问答社区",
                "icon": "fab fa-stack-overflow",
                "category": "学习资源",
                "order": 1,
            },
            {
                "title": "MDN Web Docs",
                "url": "https://developer.mozilla.org",
                "description": "Web开发权威文档",
                "icon": "fas fa-book",
                "category": "学习资源",
                "order": 2,
            },
            {
                "title": "Figma",
                "url": "https://figma.com",
                "description": "在线UI设计工具",
                "icon": "fab fa-figma",
                "category": "设计工具",
                "order": 1,
            },
        ]

        for item_data in default_nav_items:
            category = created_categories.get(item_data["category"])
            if category:
                existing_item = NavItem.query.filter_by(
                    title=item_data["title"]
                ).first()
                if not existing_item:
                    nav_item = NavItem(
                        title=item_data["title"],
                        url=item_data["url"],
                        description=item_data["description"],
                        icon=item_data["icon"],
                        category_id=category.id,
                        order=item_data["order"],
                        is_public=True,
                        created_by=admin_user.id,
                    )
                    db.session.add(nav_item)
                    print(f"创建默认导航项: {item_data['title']}")

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
