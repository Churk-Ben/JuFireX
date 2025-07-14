import base64
import io
import os
import uuid
from datetime import datetime
from PIL import Image
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    send_from_directory,
    current_app,
)
from .models import db, User
from .config import ROLE_SUPER_ADMIN, ROLE_GUEST, ROLE_NAMES
from .utils import require_role

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("auth.profile"))
        else:
            flash("用户名或密码错误", "error")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
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
                filepath = os.path.join(
                    current_app.config["USER_AVATAR_FOLDER"], filename
                )

                # 保存图片
                img.save(filepath, "PNG")

                # 更新用户头像路径
                new_user.avatar_path = filename
            except Exception as e:
                current_app.logger.error(f"处理头像时出错: {str(e)}")
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
            current_app.logger.error(f"注册用户时出错: {str(e)}")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": f"注册失败: {str(e)}"})
            flash(f"注册失败: {str(e)}", "error")
            return redirect(url_for("auth.register"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("已退出登录", "info")
    return redirect(url_for("index"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@require_role(ROLE_GUEST)
def profile():
    from .models import Project

    user = db.session.get(User, session["user_id"])
    current_user = user  # 确保current_user变量可用于base.html
    user_projects = Project.query.filter_by(author_id=user.id).all()

    # 定义角色颜色映射
    role_colors = {
        ROLE_GUEST: "bg-info",
        1: "bg-primary",  # ROLE_MEMBER
        2: "bg-warning",  # ROLE_ADMIN
        ROLE_SUPER_ADMIN: "bg-danger",
    }

    # 检查每个项目的文档空间是否已开通
    for project in user_projects:
        # 根据项目创建日期和ID生成文档文件夹路径
        folder_name = f"{project.created_at.strftime('%Y%m%d')}-{project.id}"
        project_docs_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "projects",
            folder_name,
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


@auth_bp.route("/user_data/<path:filename>")
def user_avatar(filename):
    return send_from_directory(current_app.config["USER_AVATAR_FOLDER"], filename)


@auth_bp.route("/api/users/avatar", methods=["POST"])
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
        filepath = os.path.join(current_app.config["USER_AVATAR_FOLDER"], filename)

        # 保存图像
        img.save(filepath, "JPEG", quality=95)

        # 更新用户头像路径
        if user.avatar_path:
            # 删除旧头像文件
            old_avatar_path = os.path.join(
                current_app.config["USER_AVATAR_FOLDER"], user.avatar_path
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
