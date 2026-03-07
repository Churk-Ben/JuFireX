from pathlib import Path
import sys
import json

from flask import Flask
from flask_cors import CORS

# 确保项目根目录在 sys.path 中
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import Config
from backend.core import Logger
from backend.data.database import init_db
from backend.api import register_blueprints


def create_app(config_class=Config):
    # 确保目录存在
    Config.ensure_dirs()

    # 检查环境变量配置文件
    if not (Config.PROJECT_ROOT / ".env").exists():
        print(
            f"警告: 环境变量配置文件 {Config.PROJECT_ROOT / '.env'} 不存在. 将使用系统环境变量."
        )

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

    # 打印版本信息
    try:
        v_json = Config.VERSION_JSON
        if v_json.exists():
            with open(v_json, "r", encoding="utf-8") as f:
                v_info = json.load(f)
                version = v_info.get("version")
                commit_hash = v_info.get("commit_hash")
                build_time = v_info.get("build_time")
                logger.info(f"版本: {version} ({commit_hash})")
                logger.info(f"构建时间: {build_time}")
    except Exception as e:
        logger.warning(f"无法读取版本信息: {e}")

    logger.info("JuFireX Backend 已就绪")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000)
