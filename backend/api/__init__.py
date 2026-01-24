from flask import Flask


def register_blueprints(app: Flask):
    """注册所有 API 蓝图"""
    from .auth import auth_bp
    from .user import user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/user")
