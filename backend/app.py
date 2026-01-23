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
    app.logger.info("正在初始化 JuFireX Backend...")

    # Initialize Extensions (Database, etc.)
    app.logger.info("正在初始化数据库...")
    from backend.data.database import init_db
    init_db(app)

    # Initialize SocketIO
    app.logger.info("正在初始化 SocketIO...")
    from backend.extensions import socketio
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register Socket Events
    app.logger.info("正在注册 SocketIO 事件...")
    import backend.sockets

    # Register Blueprints
    app.logger.info("正在注册 API 蓝图...")
    from backend.api import register_blueprints
    register_blueprints(app)
    
    @app.route("/health")
    def health_check():
        return {"status": "healthy", "version": "2.0.0"}

    return app

if __name__ == "__main__":
    app = create_app()
    from backend.extensions import socketio
    app.logger.info("JuFireX Backend 已就绪")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
