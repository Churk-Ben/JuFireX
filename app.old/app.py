import base64
import io
import os
import secrets
import uuid
from datetime import datetime

from PIL import Image
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    send_from_directory,
)
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///studio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["USER_AVATAR_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "user_data"
)

# 确保用户头像目录存在
os.makedirs(app.config["USER_AVATAR_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")


# 为每个请求生成 CSRF token
@app.before_request
def csrf_protect():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(16)


# 添加自定义过滤器
@app.template_filter("format_datetime")
def format_datetime(value):
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d %H:%M")


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


# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, default=ROLE_GUEST)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    avatar_path = db.Column(db.String(200), default=None)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role_name(self):
        return ROLE_NAMES.get(self.role, "未知")


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    github_url = db.Column(db.String(200))
    demo_url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_featured = db.Column(db.Boolean, default=False)
    docs_opened = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    author = db.relationship("User", backref=db.backref("projects", lazy=True))


class StudioInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(200))
    contact_email = db.Column(db.String(120))
    github_url = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.now)


# 导航分类模型
class NavCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), default="fas fa-link")
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))

    creator = db.relationship("User", backref=db.backref("nav_categories", lazy=True))
    nav_items = db.relationship(
        "NavItem", backref="category", lazy=True, cascade="all, delete-orphan"
    )


# 导航项模型
class NavItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50), default="fas fa-link")
    is_public = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey("nav_category.id"))
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))

    creator = db.relationship("User", backref=db.backref("nav_items", lazy=True))


# 用户隐藏的导航项
class HiddenNavItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    nav_item_id = db.Column(db.Integer, db.ForeignKey("nav_item.id"))
    hidden_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", backref=db.backref("hidden_nav_items", lazy=True))
    nav_item = db.relationship("NavItem")


# 权限检查装饰器
def require_role(min_role, owner_check=None):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("请先登录", "warning")
                return redirect(url_for("auth.login"))

            user = db.session.get(User, session["user_id"])
            if not user or not user.is_active:
                flash("用户不存在或已被禁用", "error")
                return redirect(url_for("auth.login"))

            # 基本角色检查
            if user.role < min_role:
                flash("权限不足", "error")
                return redirect(url_for("index"))

            # 可选的所有权或更复杂的检查
            if owner_check:
                if not owner_check(user, **kwargs):
                    flash("权限不足或操作不允许", "error")
                    # 对于API端点，返回JSON错误可能更合适
                    if request.path.startswith("/api/"):
                        return (
                            jsonify(
                                {"success": False, "message": "权限不足或操作不允许"}
                            ),
                            403,
                        )
                    return redirect(url_for("index"))

            return f(*args, **kwargs)

        decorated_function.__name__ = f.__name__
        return decorated_function

    return decorator


# --- 所有权检查函数 ---


def is_project_owner_or_admin(user, project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return False
    # 超级管理员或管理员可以管理
    if user.role >= ROLE_ADMIN:
        return True
    # 作者可以管理自己的项目
    return project.author_id == user.id


def can_manage_project(user, project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return False
    # 超级管理员可以管理所有项目
    if user.role == ROLE_SUPER_ADMIN:
        return True
    # 管理员可以管理非超级管理员和非管理员创建的项目
    if user.role == ROLE_ADMIN:
        return project.author.role < ROLE_ADMIN
    # 成员只能管理自己的项目
    if user.role == ROLE_MEMBER:
        return project.author_id == user.id
    return False


def can_manage_nav_item(user, item_id):
    item = db.session.get(NavItem, item_id)
    if not item:
        return False
    if user.role == ROLE_SUPER_ADMIN:
        return True
    if user.role == ROLE_ADMIN:
        return item.creator.role < ROLE_ADMIN
    return item.created_by == user.id


def can_manage_user(user, user_id):
    # 只有超级管理员可以管理用户
    return user.role == ROLE_SUPER_ADMIN


# --- API 路由 ---


# 路由
@app.route("/")
def index():
    studio_info = StudioInfo.query.first()
    projects = (
        Project.query.filter_by(is_featured=True)
        .order_by(Project.created_at.desc())
        .limit(6)
        .all()
    )

    current_user = None
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])

    return render_template(
        "index.html",
        studio_info=studio_info,
        projects=projects,
        current_user=current_user,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            flash("登录成功", "success")
            return redirect(url_for("profile"))
        else:
            flash("用户名或密码错误", "error")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        # 检查用户是否存在，如果不存在则清除session
        user = db.session.get(User, session["user_id"])
        if not user:
            session.clear()
        else:
            return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(
                    {"success": False, "message": "用户名已存在，请选择其他用户名"}
                )
            flash("用户名已存在，请选择其他用户名", "error")
            return redirect(url_for("auth.register"))

        # 检查邮箱是否已存在
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(
                    {"success": False, "message": "邮箱已被注册，请使用其他邮箱"}
                )
            flash("邮箱已被注册，请使用其他邮箱", "error")
            return redirect(url_for("auth.register"))

        # 创建新用户
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # 如果是第一个用户，设置为超级管理员
        if User.query.count() == 0:
            new_user.role = ROLE_SUPER_ADMIN

        # 处理头像上传
        avatar_file = request.files.get("avatar")
        if avatar_file and avatar_file.filename:
            try:
                # 读取图片数据
                img_data = avatar_file.read()
                img = Image.open(io.BytesIO(img_data))

                # 裁剪为正方形（取中心部分）
                width, height = img.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                right = left + size
                bottom = top + size
                img = img.crop((left, top, right, bottom))

                # 调整大小为标准尺寸
                img = img.resize((200, 200), Image.LANCZOS)

                # 生成唯一文件名
                filename = f"{uuid.uuid4().hex}.png"
                filepath = os.path.join(app.config["USER_AVATAR_FOLDER"], filename)

                # 保存图片
                img.save(filepath, "PNG")

                # 更新用户头像路径
                new_user.avatar_path = filename
            except Exception as e:
                app.logger.error(f"处理头像时出错: {str(e)}")
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(
                        {"success": False, "message": f"处理头像时出错: {str(e)}"}
                    )

        try:
            db.session.add(new_user)
            db.session.commit()

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True, "message": "注册成功，请登录"})

            flash("注册成功，请登录", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"注册用户时出错: {str(e)}")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": f"注册失败: {str(e)}"})
            flash(f"注册失败: {str(e)}", "error")
            return redirect(url_for("auth.register"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("已退出登录", "info")
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
@require_role(ROLE_GUEST)
def profile():
    user = db.session.get(User, session["user_id"])
    current_user = user  # 确保current_user变量可用于base.html
    user_projects = Project.query.filter_by(author_id=user.id).all()

    # 定义角色颜色映射
    role_colors = {
        ROLE_GUEST: "bg-info",
        ROLE_MEMBER: "bg-primary",
        ROLE_ADMIN: "bg-warning",
        ROLE_SUPER_ADMIN: "bg-danger",
    }

    # 检查每个项目的文档空间是否已开通
    for project in user_projects:
        # 根据项目创建日期和ID生成文档文件夹路径
        folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
        project_docs_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "projects", folder_name
        )
        project.docs_opened = os.path.exists(project_docs_path)

    return render_template(
        "profile.html",
        user=user,
        current_user=current_user,
        projects=user_projects,
        role_names=ROLE_NAMES,
        role_colors=role_colors,
        now=datetime.now(),
    )


@app.route("/user_data/<path:filename>")
def user_avatar(filename):
    return send_from_directory(app.config["USER_AVATAR_FOLDER"], filename)


@app.route("/api/users/avatar", methods=["POST"])
@require_role(ROLE_GUEST)
def upload_avatar():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "未登录"})

    user = db.session.get(User, session["user_id"])
    if not user:
        return jsonify({"success": False, "message": "用户不存在"})

    # 获取Base64编码的图像数据
    data = request.get_json()
    if not data or "avatar" not in data:
        return jsonify({"success": False, "message": "未提供头像数据"})

    try:
        # 解析Base64图像数据
        image_data = data["avatar"]
        # 移除Base64前缀
        if "," in image_data:
            image_data = image_data.split(",")[1]

        # 解码Base64数据
        image_bytes = base64.b64decode(image_data)

        # 使用PIL打开图像
        img = Image.open(io.BytesIO(image_bytes))

        # 确保图像是正方形
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        img = img.crop((left, top, right, bottom))

        # 调整大小为200x200像素
        img = img.resize((200, 200), Image.LANCZOS)

        # 生成唯一文件名
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(app.config["USER_AVATAR_FOLDER"], filename)

        # 保存图像
        img.save(filepath, "JPEG", quality=95)

        # 更新用户头像路径
        if user.avatar_path:
            # 删除旧头像文件
            old_avatar_path = os.path.join(
                app.config["USER_AVATAR_FOLDER"], user.avatar_path
            )
            try:
                os.remove(old_avatar_path)
            except FileNotFoundError:
                pass
            except Exception as e:
                return jsonify(
                    {"success": False, "message": f"删除旧头像出错: {str(e)}"}
                )
        user.avatar_path = filename
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "头像上传成功",
                "avatar_url": url_for("auth.user_avatar", filename=filename),
            }
        )

    except Exception as e:
        print(f"头像上传错误: {str(e)}")
        return jsonify({"success": False, "message": f"头像上传失败: {str(e)}"})


@app.route("/navigation")
def navigation():
    categories = NavCategory.query.order_by(NavCategory.order).all()

    current_user = None
    hidden_nav_item_ids = set()
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])
        if current_user:
            hidden_nav_items = HiddenNavItem.query.filter_by(
                user_id=current_user.id
            ).all()
            hidden_nav_item_ids = {item.nav_item_id for item in hidden_nav_items}

    # 获取所有公开的或由当前用户创建的导航项
    query = NavItem.query
    if current_user:
        query = query.filter(
            db.or_(NavItem.is_public == True, NavItem.created_by == current_user.id)
        )
    else:
        query = query.filter(NavItem.is_public == True)

    nav_items = query.order_by(NavItem.order).all()

    nav_items_by_category = {}
    for item in nav_items:
        if item.id not in hidden_nav_item_ids:
            if item.category_id not in nav_items_by_category:
                nav_items_by_category[item.category_id] = []
            nav_items_by_category[item.category_id].append(item)

    return render_template(
        "navigation.html",
        categories=categories,
        nav_items_by_category=nav_items_by_category,
        current_user=current_user,
        hidden_nav_item_ids=hidden_nav_item_ids,
    )


@app.route("/api/navigation/hide/<int:nav_item_id>", methods=["POST"])
@require_role(ROLE_MEMBER)
def hide_nav_item(nav_item_id):
    user_id = session["user_id"]

    # 验证 CSRF token
    csrf_token = request.headers.get("X-CSRFToken")
    if not csrf_token or csrf_token != session.get("_csrf_token"):
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 检查是否已经隐藏
    existing = HiddenNavItem.query.filter_by(
        user_id=user_id, nav_item_id=nav_item_id
    ).first()
    if not existing:
        hidden_item = HiddenNavItem(user_id=user_id, nav_item_id=nav_item_id)
        db.session.add(hidden_item)
        db.session.commit()

    return jsonify({"success": True})


@app.route("/api/navigation/unhide/<int:nav_item_id>", methods=["POST"])
@require_role(ROLE_MEMBER)
def unhide_nav_item(nav_item_id):
    user_id = session["user_id"]

    # 验证 CSRF token
    csrf_token = request.headers.get("X-CSRFToken")
    if not csrf_token or csrf_token != session.get("_csrf_token"):
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    hidden_item = HiddenNavItem.query.filter_by(
        user_id=user_id, nav_item_id=nav_item_id
    ).first()
    if hidden_item:
        db.session.delete(hidden_item)
        db.session.commit()

    return jsonify({"success": True})


@app.route("/api/navigation/toggle_privacy/<int:nav_item_id>", methods=["POST"])
@require_role(ROLE_MEMBER)
def toggle_nav_item_privacy(nav_item_id):
    user_id = session["user_id"]

    # 验证 CSRF token
    csrf_token = request.headers.get("X-CSRFToken")
    if not csrf_token or csrf_token != session.get("_csrf_token"):
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    data = request.json

    nav_item = NavItem.query.get_or_404(nav_item_id)

    # 只有创建者可以修改隐私状态
    if nav_item.created_by != user_id:
        return jsonify({"success": False, "message": "您没有权限修改此导航项"}), 403

    nav_item.is_public = data.get("is_public", not nav_item.is_public)
    db.session.commit()

    return jsonify({"success": True, "is_public": nav_item.is_public})


@app.route("/api/navigation/hidden_items")
@require_role(ROLE_MEMBER)
def get_hidden_nav_items():
    user_id = session["user_id"]

    hidden_items_query = (
        db.session.query(NavItem)
        .join(HiddenNavItem, NavItem.id == HiddenNavItem.nav_item_id)
        .filter(HiddenNavItem.user_id == user_id)
    )

    hidden_items = [
        {"id": item.id, "title": item.title, "category_id": item.category_id}
        for item in hidden_items_query.all()
    ]

    return jsonify({"success": True, "hidden_items": hidden_items})


# (TODO) 申请加入工作室
@app.route("/api/users/pending", methods=["GET"])
@require_role(ROLE_SUPER_ADMIN)
def get_pending_users():
    pending_users = User.query.filter_by(role=ROLE_GUEST).all()
    return jsonify(
        [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "created_at": u.created_at.isoformat(),
            }
            for u in pending_users
        ]
    )


# --- 管理员面板路由 ---


@app.route("/admin/projects")
@require_role(ROLE_ADMIN)
def admin_projects():
    current_user = db.session.get(User, session["user_id"])
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template(
        "admin/projects.html", projects=projects, current_user=current_user
    )


@app.route("/admin/users")
@require_role(ROLE_SUPER_ADMIN)
def admin_users():
    current_user = db.session.get(User, session["user_id"])
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users, current_user=current_user)


@app.route("/admin/studio-info")
@require_role(ROLE_ADMIN)
def admin_studio_info():
    current_user = db.session.get(User, session["user_id"])
    studio_info = StudioInfo.query.first()
    return render_template(
        "admin/studio_info.html", studio_info=studio_info, current_user=current_user
    )


@app.route("/admin/navigation")
@require_role(ROLE_ADMIN)
def admin_navigation():
    current_user = db.session.get(User, session["user_id"])
    categories = NavCategory.query.order_by(NavCategory.order).all()
    nav_items = NavItem.query.order_by(NavItem.category_id, NavItem.order).all()

    return render_template(
        "admin/navigation.html",
        categories=categories,
        nav_items=nav_items,
        current_user=current_user,
    )


@app.route("/api/projects", methods=["POST"])
@require_role(ROLE_MEMBER)
def create_project():
    data = request.get_json()
    project = Project(
        title=data["title"],
        description=data["description"],
        github_url=data.get("github_url"),
        demo_url=data.get("demo_url"),
        image_url=data.get("image_url"),
        is_featured=data.get("is_featured", False),
        author_id=session["user_id"],
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(
        {"success": True, "message": "项目创建成功", "project_id": project.id}
    )


# 项目文档相关路由和API


# 开通项目文档空间API
@app.route("/api/projects/<int:project_id>/open-docs", methods=["POST"])
@require_role(ROLE_MEMBER)
def open_project_docs(project_id):
    # 验证 CSRF token
    csrf_token = request.headers.get("X-CSRFToken")
    if not csrf_token or csrf_token != session.get("_csrf_token"):
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return (
            jsonify({"success": False, "message": "只有项目创建者可以开通文档空间"}),
            403,
        )

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    projects_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "projects")
    project_docs_path = os.path.join(projects_dir, folder_name)

    # 检查文件夹是否已存在
    if os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目的文档空间已存在"}), 400

    try:
        # 确保projects目录存在
        os.makedirs(projects_dir, exist_ok=True)
        # 创建项目文档目录
        os.makedirs(project_docs_path)

        # 创建默认的readme.md文件
        readme_content = f"# {project.title} 文档\n\n欢迎使用 {project.title} 项目文档！\n\n## 项目简介\n\n{project.description}\n\n## 文档说明\n\n这是项目的文档空间，您可以在这里添加和管理项目相关的文档。"
        readme_path = os.path.join(project_docs_path, "readme.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        # 更新项目的docs_opened字段
        project.docs_opened = True
        db.session.commit()

        return jsonify({"success": True, "message": "文档空间开通成功"})
    except Exception as e:
        return (
            jsonify({"success": False, "message": f"创建文档空间失败: {str(e)}"}),
            500,
        )


# 项目文档列表页面
@app.route("/projects/<int:project_id>/docs")
@require_role(ROLE_GUEST)
def project_docs(project_id):
    # 获取项目信息
    project = Project.query.get_or_404(project_id)
    current_user = db.session.get(User, session["user_id"])

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "projects", folder_name
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        flash("该项目尚未开通文档空间", "error")
        return redirect(url_for("auth.profile"))

    # 获取所有.md文件
    md_files = []
    for file in os.listdir(project_docs_path):
        if file.endswith(".md"):
            file_path = os.path.join(project_docs_path, file)
            # 获取文件修改时间
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            md_files.append({"name": file, "path": file, "modified": mod_time})

    # 按修改时间排序，最新的在前
    md_files.sort(key=lambda x: x["modified"], reverse=True)

    return render_template(
        "project_docs_list.html",
        project=project,
        md_files=md_files,
        current_user=current_user,
    )


# 查看单个文档
@app.route("/projects/<int:project_id>/docs/<path:filename>")
@require_role(ROLE_GUEST)
def project_doc_view(project_id, filename):
    # 获取项目信息
    project = Project.query.get_or_404(project_id)
    current_user = db.session.get(User, session["user_id"])

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "projects", folder_name
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        flash("该项目尚未开通文档空间", "error")
        return redirect(url_for("auth.profile"))

    # 构建文件完整路径
    file_path = os.path.join(project_docs_path, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        flash(f"文件 {filename} 不存在", "error")
        return redirect(url_for("project_docs", project_id=project_id))

    try:
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 使用mistune解析Markdown
        import mistune

        html_content = mistune.html(content)

        return render_template(
            "project_doc_view.html",
            project=project,
            filename=filename,
            content=content,
            html_content=html_content,
            current_user=current_user,
        )
    except Exception as e:
        flash(f"读取文件失败: {str(e)}", "error")
        return redirect(url_for("project_docs", project_id=project_id))


# 上传文档API
@app.route("/api/projects/<int:project_id>/docs/upload", methods=["POST"])
@require_role(ROLE_MEMBER)
def upload_project_doc(project_id):
    # 验证 CSRF token
    csrf_token = request.headers.get("X-CSRFToken")
    if not csrf_token or csrf_token != session.get("_csrf_token"):
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return jsonify({"success": False, "message": "只有项目创建者可以上传文档"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "projects", folder_name
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目尚未开通文档空间"}), 400

    try:
        # 获取上传的文件和文档名称
        doc_file = request.files.get("docFile")
        doc_name = request.form.get("docName")

        if not doc_file or not doc_name:
            return jsonify({"success": False, "message": "缺少必要参数"}), 400

        # 验证文件类型
        if not doc_file.filename.lower().endswith((".md", ".markdown")):
            return (
                jsonify({"success": False, "message": "只支持Markdown格式的文档"}),
                400,
            )

        # 清理文件名，确保安全
        safe_doc_name = secure_filename(doc_name)
        if not safe_doc_name:
            return jsonify({"success": False, "message": "无效的文档名称"}), 400

        # 添加.md扩展名
        if not safe_doc_name.lower().endswith(".md"):
            safe_doc_name += ".md"

        # 检查文件是否已存在
        file_path = os.path.join(project_docs_path, safe_doc_name)
        if os.path.exists(file_path):
            return jsonify({"success": False, "message": "同名文档已存在"}), 400

        # 读取文件内容并保存
        content = doc_file.read().decode("utf-8")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return jsonify(
            {"success": True, "message": "文档上传成功", "filename": safe_doc_name}
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"上传文档失败: {str(e)}"}), 500


# 创建新文档API
@app.route("/api/projects/<int:project_id>/docs/create", methods=["POST"])
@require_role(ROLE_MEMBER)
def create_project_doc(project_id):
    # 验证 CSRF token
    csrf_token = request.headers.get("X-CSRFToken")
    if not csrf_token or csrf_token != session.get("_csrf_token"):
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return jsonify({"success": False, "message": "只有项目创建者可以创建文档"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "projects", folder_name
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目尚未开通文档空间"}), 400

    try:
        # 获取文档标题和内容
        data = request.json
        doc_title = data.get("docTitle")
        doc_content = data.get("docContent")

        if not doc_title or not doc_content:
            return jsonify({"success": False, "message": "缺少必要参数"}), 400

        # 清理文件名，确保安全
        safe_doc_name = secure_filename(doc_title)
        if not safe_doc_name:
            return jsonify({"success": False, "message": "无效的文档标题"}), 400

        # 添加.md扩展名
        if not safe_doc_name.lower().endswith(".md"):
            safe_doc_name += ".md"

        # 检查文件是否已存在
        file_path = os.path.join(project_docs_path, safe_doc_name)
        if os.path.exists(file_path):
            return jsonify({"success": False, "message": "同名文档已存在"}), 400

        # 保存文档内容
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        return jsonify(
            {"success": True, "message": "文档创建成功", "filename": safe_doc_name}
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"创建文档失败: {str(e)}"}), 500


# 获取原始文档内容API
@app.route("/api/projects/<int:project_id>/docs/<path:filename>/raw", methods=["GET"])
@require_role(ROLE_MEMBER)
def get_project_doc_raw(project_id, filename):
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({"success": False, "message": "项目不存在"}), 404

    # 权限检查：只有项目作者或管理员可以获取
    user = db.session.get(User, session.get("user_id"))
    if not user or (user.id != project.author_id and user.role < ROLE_ADMIN):
        return jsonify({"success": False, "message": "权限不足"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "projects", folder_name
    )
    doc_path = os.path.join(project_docs_path, filename)

    if not os.path.exists(doc_path) or not os.path.isfile(doc_path):
        return jsonify({"success": False, "message": "文档不存在"}), 404

    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({"success": True, "content": content})
    except Exception as e:
        return jsonify({"success": False, "message": f"读取文件时出错: {e}"}), 500


# 更新文档API
@app.route("/api/projects/<int:project_id>/docs/<path:filename>", methods=["PUT"])
@require_role(ROLE_MEMBER)
def update_project_doc(project_id, filename):
    # 验证 CSRF token
    csrf_token = request.headers.get("X-CSRFToken")
    if not csrf_token or csrf_token != session.get("_csrf_token"):
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return jsonify({"success": False, "message": "只有项目创建者可以编辑文档"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "projects", folder_name
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目尚未开通文档空间"}), 400

    # 构建文件完整路径
    file_path = os.path.join(project_docs_path, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return jsonify({"success": False, "message": f"文件 {filename} 不存在"}), 404

    try:
        # 获取更新的文档标题和内容
        data = request.json
        new_doc_title = data.get("docTitle")
        doc_content = data.get("docContent")

        if not new_doc_title or not doc_content:
            return jsonify({"success": False, "message": "缺少必要参数"}), 400

        # 清理文件名，确保安全
        safe_doc_name = secure_filename(new_doc_title)
        if not safe_doc_name:
            return jsonify({"success": False, "message": "无效的文档标题"}), 400

        # 添加.md扩展名
        if not safe_doc_name.lower().endswith(".md"):
            safe_doc_name += ".md"

        # 检查是否需要重命名文件
        new_file_path = os.path.join(project_docs_path, safe_doc_name)
        rename_needed = filename != safe_doc_name

        # 如果需要重命名，检查新文件名是否已存在
        if rename_needed and os.path.exists(new_file_path):
            return jsonify({"success": False, "message": "同名文档已存在"}), 400

        # 保存文档内容
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc_content)

        # 如果需要重命名，执行重命名操作
        if rename_needed:
            os.rename(file_path, new_file_path)
            return jsonify(
                {
                    "success": True,
                    "message": "文档更新并重命名成功",
                    "filename": safe_doc_name,
                }
            )

        return jsonify(
            {"success": True, "message": "文档更新成功", "filename": filename}
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"更新文档失败: {str(e)}"}), 500


# 删除文档API
@app.route("/api/projects/<int:project_id>/docs/<path:filename>", methods=["DELETE"])
@require_role(ROLE_MEMBER)
def delete_project_doc(project_id, filename):
    # 验证 CSRF token
    csrf_token = request.headers.get("X-CSRFToken")
    if not csrf_token or csrf_token != session.get("_csrf_token"):
        return jsonify({"success": False, "message": "CSRF 验证失败"}), 403

    # 获取项目信息
    project = Project.query.get_or_404(project_id)

    # 验证当前用户是否为项目所有者
    if project.author_id != session["user_id"]:
        return jsonify({"success": False, "message": "只有项目创建者可以删除文档"}), 403

    # 生成文档文件夹路径
    folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
    project_docs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "projects", folder_name
    )

    # 检查文档空间是否存在
    if not os.path.exists(project_docs_path):
        return jsonify({"success": False, "message": "该项目尚未开通文档空间"}), 400

    # 构建文件完整路径
    file_path = os.path.join(project_docs_path, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return jsonify({"success": False, "message": f"文件 {filename} 不存在"}), 404

    try:
        # 删除文件
        os.remove(file_path)
        return jsonify({"success": True, "message": "文档删除成功"})
    except Exception as e:
        return jsonify({"success": False, "message": f"删除文档失败: {str(e)}"}), 500


@app.route("/api/users/<int:user_id>/role", methods=["PUT"])
@require_role(ROLE_SUPER_ADMIN, owner_check=can_manage_user)
def update_user_role(user_id):
    user_to_update = db.session.get(User, user_id)
    if not user_to_update:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    data = request.json
    new_role = data.get("role")

    if new_role not in ROLE_NAMES:
        return jsonify({"success": False, "message": "无效的角色"}), 400

    # 防止将自己降级
    if user_to_update.id == session.get("user_id") and new_role < ROLE_SUPER_ADMIN:
        return (
            jsonify({"success": False, "message": "不能降低自己的超级管理员权限"}),
            403,
        )

    user_to_update.role = new_role
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "用户角色已更新",
            "new_role_name": ROLE_NAMES[new_role],
        }
    )


@app.route("/api/users/<int:user_id>/status", methods=["PUT"])
@require_role(ROLE_SUPER_ADMIN, owner_check=can_manage_user)
def update_user_status(user_id):
    user_to_update = db.session.get(User, user_id)
    if not user_to_update:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    data = request.json
    is_active = data.get("is_active")

    if is_active is None:
        return jsonify({"success": False, "message": "缺少 is_active 参数"}), 400

    # 防止禁用自己
    if user_to_update.id == session.get("user_id") and not is_active:
        return jsonify({"success": False, "message": "不能禁用自己的账户"}), 403

    user_to_update.is_active = is_active
    db.session.commit()

    return jsonify(
        {"success": True, "message": "用户状态已更新", "is_active": is_active}
    )


@app.route("/api/users/<int:user_id>", methods=["GET"])
@require_role(ROLE_SUPER_ADMIN)
def get_user_details(user_id):
    user = User.query.get_or_404(user_id)
    user_projects = Project.query.filter_by(author_id=user.id).all()
    featured_projects = [p for p in user_projects if p.is_featured]

    from datetime import datetime

    active_days = (datetime.now() - user.created_at).days

    return jsonify(
        {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role_name": user.get_role_name(),
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "project_count": len(user_projects),
                "featured_project_count": len(featured_projects),
                "active_days": active_days,
                "avatar_path": user.avatar_path,
            },
        }
    )


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
@require_role(ROLE_SUPER_ADMIN, owner_check=can_manage_user)
def delete_user(user_id):
    user_to_delete = db.session.get(User, user_id)
    if not user_to_delete:
        return jsonify({"success": False, "message": "用户不存在"}), 404

    # 不能删除自己
    if user_to_delete.id == session.get("user_id"):
        return jsonify({"success": False, "message": "不能删除自己"}), 403

    try:
        # 在删除用户前，处理该用户创建的内容
        # 将项目作者设置为null
        Project.query.filter_by(author_id=user_id).update({"author_id": None})
        # 删除导航项和分类
        NavItem.query.filter_by(created_by=user_id).delete()
        NavCategory.query.filter_by(created_by=user_id).delete()

        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"success": True, "message": "用户已删除"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500


@app.route("/api/projects/<int:project_id>/featured", methods=["PUT"])
@require_role(ROLE_ADMIN)
def toggle_project_featured(project_id):
    data = request.get_json()
    project = Project.query.get_or_404(project_id)
    project.is_featured = data["is_featured"]
    db.session.commit()
    return jsonify({"success": True, "message": "项目状态更新成功"})


@app.route("/api/projects/<int:project_id>", methods=["GET"])
@require_role(ROLE_ADMIN)
def get_project(project_id):
    project = Project.query.get_or_404(project_id)

    # 构建项目数据
    project_data = {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "github_url": project.github_url,
        "demo_url": project.demo_url,
        "image_url": project.image_url,
        "is_featured": project.is_featured,
        "created_at": project.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "author_id": project.author_id,
        "author": project.author.username if project.author else None,
    }

    return jsonify({"success": True, "project": project_data})


@app.route("/api/projects/<int:project_id>", methods=["PUT"])
@require_role(ROLE_ADMIN)
def update_project(project_id):
    project = Project.query.get_or_404(project_id)

    # 检查权限：只有项目作者或超级管理员可以更新
    if (
        project.author_id != session["user_id"]
        and session.get("role", 0) < ROLE_SUPER_ADMIN
    ):
        return jsonify({"success": False, "message": "权限不足"})

    data = request.get_json()

    # 更新项目信息
    project.title = data.get("title", project.title)
    project.description = data.get("description", project.description)
    project.github_url = data.get("github_url", project.github_url)
    project.demo_url = data.get("demo_url", project.demo_url)
    project.image_url = data.get("image_url", project.image_url)
    project.is_featured = data.get("is_featured", project.is_featured)

    db.session.commit()

    return jsonify({"success": True, "message": "项目更新成功"})


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
@require_role(ROLE_MEMBER, owner_check=can_manage_project)
def delete_project(project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({"success": False, "message": "项目不存在"}), 404

    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({"success": True, "message": "项目已删除"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500


@app.route("/api/studio-info", methods=["PUT"])
@require_role(ROLE_ADMIN)
def update_studio_info():
    data = request.json
    studio_info = StudioInfo.query.first()
    if not studio_info:
        studio_info = StudioInfo(name="默认工作室名称")  # 提供一个默认名称
        db.session.add(studio_info)

    studio_info.name = data.get("name", studio_info.name)
    studio_info.description = data.get("description", studio_info.description)
    studio_info.contact_email = data.get("contact_email", studio_info.contact_email)
    studio_info.github_url = data.get("github_url", studio_info.github_url)
    studio_info.updated_at = datetime.now()

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "工作室信息更新成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"更新失败: {str(e)}"}), 500


# 导航分类API
@app.route("/api/nav-categories", methods=["GET"])
@require_role(ROLE_MEMBER)
def get_nav_categories():
    categories = NavCategory.query.order_by(NavCategory.order).all()
    categories_data = [
        {
            "id": cat.id,
            "name": cat.name,
            "icon": cat.icon,
            "order": cat.order,
            "created_by": cat.created_by,
            "creator_name": cat.creator.username if cat.creator else None,
        }
        for cat in categories
    ]

    return jsonify({"success": True, "categories": categories_data})


@app.route("/api/nav-categories", methods=["POST"])
@require_role(ROLE_ADMIN)
def create_nav_category():
    data = request.get_json()

    # 验证数据
    if not data.get("name"):
        return jsonify({"success": False, "message": "分类名称不能为空"})

    # 创建新分类
    category = NavCategory(
        name=data["name"],
        icon=data.get("icon", "fas fa-link"),
        order=data.get("order", 0),
        created_by=session["user_id"],
    )

    db.session.add(category)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "导航分类创建成功",
            "category": {
                "id": category.id,
                "name": category.name,
                "icon": category.icon,
                "order": category.order,
            },
        }
    )


@app.route("/api/nav-categories/<int:category_id>", methods=["PUT"])
@require_role(ROLE_ADMIN)
def update_nav_category(category_id):
    category = NavCategory.query.get_or_404(category_id)
    data = request.get_json()

    # 更新分类信息
    if "name" in data:
        category.name = data["name"]
    if "icon" in data:
        category.icon = data["icon"]
    if "order" in data:
        category.order = data["order"]

    db.session.commit()

    return jsonify({"success": True, "message": "导航分类更新成功"})


@app.route("/api/nav-categories/<int:category_id>", methods=["DELETE"])
@require_role(ROLE_SUPER_ADMIN)  # 只有超级管理员可以删除分类
def delete_nav_category(category_id):
    category = db.session.get(NavCategory, category_id)
    if not category:
        return jsonify({"success": False, "message": "分类不存在"}), 404

    # 检查是否有导航项属于此分类
    if category.nav_items:
        return jsonify({"success": False, "message": "分类下有导航项，无法删除"}), 400

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"success": True, "message": "分类已删除"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500


# 导航项API
@app.route("/api/nav-items", methods=["GET"])
@require_role(ROLE_MEMBER)
def get_nav_items():
    current_user = db.session.get(User, session["user_id"])

    # 获取所有公开的导航项和当前用户创建的私有导航项
    nav_items = (
        NavItem.query.filter(
            db.or_(NavItem.is_public == True, NavItem.created_by == current_user.id)
        )
        .order_by(NavItem.category_id, NavItem.order)
        .all()
    )

    # 获取当前用户隐藏的导航项ID列表
    hidden_items = HiddenNavItem.query.filter_by(user_id=current_user.id).all()
    hidden_item_ids = [item.nav_item_id for item in hidden_items]

    items_data = [
        {
            "id": item.id,
            "title": item.title,
            "url": item.url,
            "description": item.description,
            "icon": item.icon,
            "is_public": item.is_public,
            "order": item.order,
            "category_id": item.category_id,
            "created_by": item.created_by,
            "creator_name": item.creator.username if item.creator else None,
            "is_hidden": item.id in hidden_item_ids,
            "is_owner": item.created_by == current_user.id,
        }
        for item in nav_items
    ]

    return jsonify({"success": True, "nav_items": items_data})


@app.route("/api/nav-items", methods=["POST"])
@require_role(ROLE_MEMBER)
def create_nav_item():
    data = request.get_json()

    # 验证数据
    if not data.get("title"):
        return jsonify({"success": False, "message": "导航标题不能为空"})
    if not data.get("url"):
        return jsonify({"success": False, "message": "导航URL不能为空"})
    if not data.get("category_id"):
        return jsonify({"success": False, "message": "必须选择一个分类"})

    # 检查分类是否存在
    category = NavCategory.query.get(data["category_id"])
    if not category:
        return jsonify({"success": False, "message": "所选分类不存在"})

    # 创建新导航项
    nav_item = NavItem(
        title=data["title"],
        url=data["url"],
        description=data.get("description", ""),
        icon=data.get("icon", "fas fa-link"),
        is_public=data.get("is_public", True),
        order=data.get("order", 0),
        category_id=data["category_id"],
        created_by=session["user_id"],
    )

    db.session.add(nav_item)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": "导航项创建成功",
            "nav_item": {
                "id": nav_item.id,
                "title": nav_item.title,
                "url": nav_item.url,
                "description": nav_item.description,
                "icon": nav_item.icon,
                "is_public": nav_item.is_public,
                "category_id": nav_item.category_id,
            },
        }
    )


@app.route("/api/nav-items/<int:item_id>", methods=["PUT"])
@require_role(ROLE_MEMBER)
def update_nav_item(item_id):
    nav_item = NavItem.query.get_or_404(item_id)
    current_user = db.session.get(User, session["user_id"])

    # 检查权限：只有创建者或超级管理员可以更新
    if nav_item.created_by != current_user.id and current_user.role < ROLE_SUPER_ADMIN:
        return jsonify({"success": False, "message": "权限不足"})

    data = request.get_json()

    # 更新导航项信息
    if "title" in data:
        nav_item.title = data["title"]
    if "url" in data:
        nav_item.url = data["url"]
    if "description" in data:
        nav_item.description = data["description"]
    if "icon" in data:
        nav_item.icon = data["icon"]
    if "is_public" in data:
        nav_item.is_public = data["is_public"]
    if "order" in data:
        nav_item.order = data["order"]
    if "category_id" in data:
        # 检查分类是否存在
        category = NavCategory.query.get(data["category_id"])
        if not category:
            return jsonify({"success": False, "message": "所选分类不存在"})
        nav_item.category_id = data["category_id"]

    db.session.commit()

    return jsonify({"success": True, "message": "导航项更新成功"})


@app.route("/api/nav-items/<int:item_id>", methods=["DELETE"])
@require_role(ROLE_MEMBER, owner_check=can_manage_nav_item)
def delete_nav_item(item_id):
    nav_item = db.session.get(NavItem, item_id)
    if not nav_item:
        return jsonify({"success": False, "message": "导航项不存在"}), 404

    try:
        # 删除相关的隐藏记录
        HiddenNavItem.query.filter_by(nav_item_id=item_id).delete()

        # 删除导航项
        db.session.delete(nav_item)
        db.session.commit()
        return jsonify({"success": True, "message": "导航项删除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500


# 隐藏/显示导航项API
@app.route("/api/nav-items/<int:item_id>/visibility", methods=["PUT"])
@require_role(ROLE_MEMBER)
def toggle_nav_item_visibility(item_id):
    nav_item = NavItem.query.get_or_404(item_id)
    current_user = db.session.get(User, session["user_id"])
    data = request.get_json()

    # 检查是否是自己创建的导航项
    if nav_item.created_by == current_user.id:
        # 如果是自己的导航项，可以设置公开/私有
        if "is_public" in data:
            nav_item.is_public = data["is_public"]
            db.session.commit()
            return jsonify({"success": True, "message": "导航项可见性更新成功"})

    # 对于其他用户的公开导航项，可以选择隐藏/显示
    if "is_hidden" in data:
        # 检查是否已经存在隐藏记录
        hidden_record = HiddenNavItem.query.filter_by(
            user_id=current_user.id, nav_item_id=item_id
        ).first()

        if data["is_hidden"]:
            # 隐藏导航项
            if not hidden_record:
                hidden_record = HiddenNavItem(
                    user_id=current_user.id, nav_item_id=item_id
                )
                db.session.add(hidden_record)
                db.session.commit()
            return jsonify({"success": True, "message": "导航项已隐藏"})
        else:
            # 显示导航项
            if hidden_record:
                db.session.delete(hidden_record)
                db.session.commit()
            return jsonify({"success": True, "message": "导航项已显示"})

    return jsonify({"success": False, "message": "无效的请求"})


# SocketIO 事件
@socketio.on("connect")
def handle_connect(auth=None):
    if "user_id" in session:
        user = db.session.get(User, session["user_id"])
        if user:
            emit("user_connected", {"username": user.username})


@socketio.on("disconnect")
def handle_disconnect(auth=None):
    if "user_id" in session:
        user = db.session.get(User, session["user_id"])
        if user:
            emit("user_disconnected", {"username": user.username})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # 创建默认超级管理员
        if not User.query.filter_by(role=ROLE_SUPER_ADMIN).first():
            admin = User(
                username="admin", email="admin@studio.com", role=ROLE_SUPER_ADMIN
            )
            admin.set_password("admin123")
            db.session.add(admin)

            # 创建默认工作室信息
            studio = StudioInfo(
                name="JuFire Studio",
                description="一个专注于创新技术开发的游戏创意工作室",
                contact_email="contact@jufire.studio",
                github_url="https://github.com/JuFireX",
            )
            db.session.add(studio)

            # 创建默认导航分类
            categories = [
                NavCategory(name="快速访问", icon="fas fa-bolt", order=1, created_by=1),
                NavCategory(
                    name="开发工具", icon="fas fa-tools", order=2, created_by=1
                ),
                NavCategory(
                    name="学习资源", icon="fas fa-graduation-cap", order=3, created_by=1
                ),
                NavCategory(name="常用链接", icon="fas fa-link", order=4, created_by=1),
            ]
            db.session.add_all(categories)

            db.session.commit()

    socketio.run(app, debug=True, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
