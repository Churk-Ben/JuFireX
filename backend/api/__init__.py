from flask import Flask

def register_blueprints(app: Flask):
    """注册所有 API 蓝图"""
    from .auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
