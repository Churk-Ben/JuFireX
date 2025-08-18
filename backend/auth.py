import base64
import io
import os
import uuid
from datetime import datetime
from PIL import Image
import json
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
from .config import ROLE_SUPER_ADMIN, ROLE_GUEST, ROLE_MEMBER, ROLE_ADMIN, ROLE_NAMES
from .utils import require_role
from .services import ImageService

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
            return redirect(url_for("auth.profile", user_id=user.id))
        else:
            flash("用户名或密码错误", "error")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        user = db.session.get(User, session.get("user_id"))
        if user:
            return redirect(url_for("index"))
        session.clear()

    if request.method == "POST":
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not password:
            return send_response(False, "密码不能为空", url_for("auth.register"), is_ajax)

        if User.query.filter_by(username=username).first():
            return send_response(False, "用户名已存在，请选择其他用户名", url_for("auth.register"), is_ajax)

        if User.query.filter_by(email=email).first():
            return send_response(False, "邮箱已被注册，请使用其他邮箱", url_for("auth.register"), is_ajax)

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)

            if User.query.count() == 0:
                new_user.role = ROLE_SUPER_ADMIN

            db.session.add(new_user)
            db.session.commit()

            avatar_file = request.files.get("avatar")
            if avatar_file and avatar_file.filename:
                try:
                    avatar_path = ImageService.process_user_avatar(
                        image_data=avatar_file.read(), user_id=new_user.id
                    )
                    new_user.avatar_path = avatar_path
                    db.session.commit()
                except Exception as e:
                    current_app.logger.error(f"处理头像时出错: {str(e)}")
                    return send_response(False, f"处理头像时出错: {str(e)}", is_ajax=is_ajax)

            return send_response(True, "注册成功，请登录", url_for("auth.login"), is_ajax)

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"注册用户时出错: {str(e)}")
            return send_response(False, f"注册失败: {str(e)}", url_for("auth.register"), is_ajax)

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("已退出登录", "info")
    return redirect(url_for("index"))


@auth_bp.route("/profile/<int:user_id>", methods=["GET", "POST"])
@require_role(ROLE_GUEST)
def profile(user_id):
    from .models import Project, NavItem

    user = User.query.get_or_404(user_id)

    current_user = db.session.get(User, session.get("user_id"))
    user_projects = Project.query.filter_by(author_id=user.id).all()
    public_nav_count = NavItem.query.filter_by(is_public=True, created_by=user.id).count()

    # 定义角色颜色映射
    role_colors = {
        ROLE_GUEST: "bg-info",
        ROLE_MEMBER: "bg-primary",
        ROLE_ADMIN: "bg-warning",
        ROLE_SUPER_ADMIN: "bg-danger",
    }

    return render_template(
        "profile.html",
        user=user,
        current_user=current_user,
        projects=user_projects,
        public_nav_count=public_nav_count,
        role_names=ROLE_NAMES,
        role_colors=role_colors,
        now=datetime.now(),
    )


@auth_bp.route("/user_data/<path:filename>")
def user_avatar(filename):
    directory = os.path.join(current_app.config["USER_AVATAR_FOLDER"], os.path.dirname(filename))
    return send_from_directory(directory, os.path.basename(filename))


@auth_bp.route("/api/users/avatar", methods=["POST"])
@require_role(ROLE_GUEST)
def upload_avatar():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "未登录"})

    user = db.session.get(User, session["user_id"])
    if not user:
        return jsonify({"success": False, "message": "用户不存在"})

    data = request.get_json()
    if not data or "avatar" not in data:
        return jsonify({"success": False, "message": "未提供头像数据"})

    try:
        avatar_path = ImageService.process_user_avatar(
            image_data=data["avatar"], user_id=user.id, old_avatar_path=user.avatar_path
        )
        user.avatar_path = avatar_path
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "头像上传成功",
            "avatar_url": url_for("auth.user_avatar", filename=user.avatar_path),
        })

    except Exception as e:
        current_app.logger.error(f"头像上传错误: {str(e)}")
        return jsonify({"success": False, "message": f"头像上传失败: {str(e)}"})


def send_response(success, message, redirect_url=None, is_ajax=False):
    if is_ajax:
        return jsonify({"success": success, "message": message})
    
    flash(message, "success" if success else "error")
    if redirect_url:
        return redirect(redirect_url)
    return None


@auth_bp.route("/profile/<int:user_id>/settings", methods=["GET", "POST"])
@require_role(ROLE_GUEST)
def settings(user_id):
    user = User.query.get_or_404(user_id)
    current_user = db.session.get(User, session.get("user_id"))

    settings_dir = os.path.join(current_app.config["USER_DATA_FOLDER"], str(user.id))
    settings_file = os.path.join(settings_dir, "settings.json")

    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)

    if request.method == "POST":
        if current_user.id != user.id:
            flash("您没有权限执行此操作", "error")
            return redirect(url_for("auth.profile", user_id=user.id))

        settings = {
            "theme": request.form.get("theme"),
            "notifications": request.form.get("notifications") == "on",
        }
        with open(settings_file, "w") as f:
            json.dump(settings, f, indent=4)

        flash("设置已保存", "success")
        return redirect(url_for("auth.settings", user_id=user.id))

    settings = {}
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            settings = json.load(f)
    else:
        # Default settings
        settings = {"theme": "light", "notifications": True}
        with open(settings_file, "w") as f:
            json.dump(settings, f, indent=4)

    return render_template(
        "profile/settings.html",
        user=user,
        current_user=current_user,
        settings=settings,
    )
