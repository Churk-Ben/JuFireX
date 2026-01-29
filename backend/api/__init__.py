from flask import Flask


def register_blueprints(app: Flask):
    """注册所有 API 蓝图"""
    from .auth import auth_bp
    from .user import user_bp
    from .navigation import nav_bp
    from .project import project_bp
    from .blog import blog_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(nav_bp, url_prefix="/api/navigation")
    app.register_blueprint(project_bp, url_prefix="/api/project")
    app.register_blueprint(blog_bp, url_prefix="/api/blog")
