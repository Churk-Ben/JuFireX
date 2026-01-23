from flask import Flask

def register_blueprints(app: Flask):
    from .auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
