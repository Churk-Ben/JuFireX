from pathlib import Path
import sys

from flask import Flask
from flask_cors import CORS

# 确保项目根目录在 sys.path 中
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import Config
from backend.core import Logger
from backend.data.database import init_db
from backend.api import register_blueprints


def create_app(config_class=Config):
    # 检查环境变量配置文件
    if not (Config.PROJECT_ROOT / ".env").exists():
        print(f"错误: 环境变量配置文件 {Config.PROJECT_ROOT / '.env'} 不存在.")
        sys.exit(1)

    # 确保目录存在
    Config.ensure_dirs()

    # 初始化日志记录器
    logger = Logger.get_logger("JuFireX_Backend")

    # 创建 Flask 应用实例
    logger.info("正在创建后端实例...")
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger = Logger.get_logger("Clash_Error")
    CORS(app)

    # 初始化数据库
    logger.info("正在初始化数据库...")
    init_db(app)

    # 注册 API 蓝图
    logger.info("正在注册 API 蓝图...")
    register_blueprints(app)

    logger.info("JuFireX Backend 已就绪")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000)
