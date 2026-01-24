from pathlib import Path
import sys

from flask import Flask
from flask_cors import CORS

# 确保项目根目录在 sys.path 中
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import Config
from backend.core import Logger


def create_app(config_class=Config):
    Config.ensure_dirs()

    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    # 初始化 Logger
    app.logger = Logger.get_logger("JuFireX_Backend")
    app.logger.info("正在初始化 JuFireX Backend...")

    # 初始化数据库
    app.logger.info("正在初始化数据库...")
    from backend.data.database import init_db

    init_db(app)

    # 注册 API 蓝图
    app.logger.info("正在注册 API 蓝图...")
    from backend.api import register_blueprints

    register_blueprints(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.logger.info("JuFireX Backend 已就绪")
    app.run(debug=True, host="0.0.0.0", port=5000)
