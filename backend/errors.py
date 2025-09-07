from flask import Blueprint, render_template, session, current_app
from backend.models import User, db

errors_bp = Blueprint("errors", __name__)

# 路由处理
@errors_bp.route("/403")
def forbidden():
    # 获取当前用户信息
    current_user = None
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])

    return render_template(
        "pages/errors/403.html",
        current_user=current_user,
    )

@errors_bp.route("/404")
def not_found():
    # 获取当前用户信息
    current_user = None
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])

    return render_template(
        "pages/errors/404.html",
        current_user=current_user,
    )

@errors_bp.route("/502")
def bad_gateway():
    # 获取当前用户信息
    current_user = None
    if "user_id" in session:
        current_user = db.session.get(User, session["user_id"])

    return render_template(
        "pages/errors/502.html",
        current_user=current_user,
    )

# 错误处理器
def register_error_handlers(app):
    @app.errorhandler(403)
    def handle_forbidden(e):
        # 获取当前用户信息
        current_user = None
        if "user_id" in session:
            current_user = db.session.get(User, session["user_id"])

        return (
            render_template(
                "pages/errors/403.html",
                current_user=current_user,
            ),
            403,
        )

    @app.errorhandler(404)
    def handle_not_found(e):
        # 获取当前用户信息
        current_user = None
        if "user_id" in session:
            current_user = db.session.get(User, session["user_id"])

        return (
            render_template(
                "pages/errors/404.html",
                current_user=current_user,
            ),
            404,
        )
        
    @app.errorhandler(502)
    def handle_bad_gateway(e):
        # 获取当前用户信息
        current_user = None
        if "user_id" in session:
            current_user = db.session.get(User, session["user_id"])

        return (
            render_template(
                "pages/errors/502.html",
                current_user=current_user,
            ),
            502,
        )