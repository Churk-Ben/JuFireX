import sys
from pathlib import Path
from flask import Flask
from flask_cors import CORS

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.config import Config
from backend.utils import Logger

def create_app(config_class=Config):
    Config.ensure_dirs()
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 启用 CORS
    CORS(app)
    
    # Initialize Logger
    app.logger = Logger.get_logger("JuFireX_Backend")
    app.logger.info("Starting JuFireX Backend...")

    # Initialize Extensions (Database, etc.)
    from backend.data.database import init_db
    init_db(app)

    # Register Blueprints
    from backend.api import register_blueprints
    register_blueprints(app)
    
    @app.route("/health")
    def health_check():
        return {"status": "healthy", "version": "2.0.0"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
