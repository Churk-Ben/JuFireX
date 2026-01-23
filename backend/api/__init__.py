from flask import Flask

def register_blueprints(app: Flask):
    from .auth import auth_bp
    from .project import project_bp
    from .nav import nav_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(project_bp, url_prefix="/api/projects")
    app.register_blueprint(nav_bp, url_prefix="/api/nav")
