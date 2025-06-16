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
from datetime import datetime
import os
import base64
import re
import uuid
from PIL import Image
import io

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


# 权限检查装饰器
def require_role(min_role):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))

            user = db.session.get(User, session["user_id"])
            if not user or user.role < min_role:
                flash("权限不足", "error")
                return redirect(url_for("index"))

            return f(*args, **kwargs)

        decorated_function.__name__ = f.__name__
        return decorated_function

    return decorator


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
            return redirect(url_for("register"))

        # 检查邮箱是否已存在
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(
                    {"success": False, "message": "邮箱已被注册，请使用其他邮箱"}
                )
            flash("邮箱已被注册，请使用其他邮箱", "error")
            return redirect(url_for("register"))

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
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"注册用户时出错: {str(e)}")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": f"注册失败: {str(e)}"})
            flash(f"注册失败: {str(e)}", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("已退出登录", "info")
    return redirect(url_for("index"))


@app.route("/profile")
@require_role(ROLE_GUEST)
def profile():
    user = db.session.get(User, session["user_id"])
    current_user = user  # 确保current_user变量可用于base.html
    user_projects = Project.query.filter_by(author_id=user.id).all()

    # 定义角色颜色映射
    role_colors = {
        ROLE_GUEST: "bg-secondary",
        ROLE_MEMBER: "bg-primary",
        ROLE_ADMIN: "bg-success",
        ROLE_SUPER_ADMIN: "bg-danger",
    }

    return render_template(
        "profile.html",
        user=user,
        current_user=current_user,
        projects=user_projects,
        role_names=ROLE_NAMES,
        role_colors=role_colors,
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
        user.avatar_path = filename
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "头像上传成功",
                "avatar_url": url_for("user_avatar", filename=filename),
            }
        )

    except Exception as e:
        print(f"头像上传错误: {str(e)}")
        return jsonify({"success": False, "message": f"头像上传失败: {str(e)}"})


@app.route("/navigation")
@require_role(ROLE_MEMBER)
def navigation():
    current_user = db.session.get(User, session["user_id"])
    return render_template("navigation.html", current_user=current_user)


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


@app.route("/api/projects", methods=["POST"])
@require_role(ROLE_ADMIN)
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
    return jsonify({"success": True, "message": "项目创建成功"})


@app.route("/api/users/<int:user_id>/role", methods=["PUT"])
@require_role(ROLE_SUPER_ADMIN)
def update_user_role(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.role = data["role"]
    db.session.commit()
    return jsonify({"success": True, "message": "用户角色更新成功"})


@app.route("/api/users/<int:user_id>/status", methods=["PUT"])
@require_role(ROLE_SUPER_ADMIN)
def update_user_status(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.is_active = data["is_active"]
    db.session.commit()
    return jsonify({"success": True, "message": "用户状态更新成功"})


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
@require_role(ROLE_SUPER_ADMIN)
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # 防止删除当前登录的超级管理员
    if user.id == session["user_id"]:
        return jsonify({"success": False, "message": "不能删除当前登录的用户"})

    # 删除用户的所有项目
    Project.query.filter_by(author_id=user.id).delete()

    # 删除用户
    db.session.delete(user)
    db.session.commit()

    return jsonify({"success": True, "message": "用户删除成功"})


@app.route("/api/projects/<int:project_id>/featured", methods=["PUT"])
@require_role(ROLE_ADMIN)
def toggle_project_featured(project_id):
    data = request.get_json()
    project = Project.query.get_or_404(project_id)
    project.is_featured = data["is_featured"]
    db.session.commit()
    return jsonify({"success": True, "message": "项目状态更新成功"})


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
@require_role(ROLE_ADMIN)
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    # 检查权限：只有项目作者或超级管理员可以删除
    if (
        project.author_id != session["user_id"]
        and session.get("role", 0) < ROLE_SUPER_ADMIN
    ):
        return jsonify({"success": False, "message": "权限不足"})

    db.session.delete(project)
    db.session.commit()

    return jsonify({"success": True, "message": "项目删除成功"})


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
            )
            db.session.add(studio)
            db.session.commit()

    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
