#!/bin/bash

# 1. 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请先安装 Python 3 (建议 >= 3.11)"
    exit 1
fi

# 2. 创建虚拟环境
echo "正在创建虚拟环境..."
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
echo "正在安装依赖..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "错误: 未找到 requirements.txt"
    exit 1
fi

# 4. 创建 .env 配置文件 (如果不存在)
if [ ! -f .env ]; then
    echo "正在创建默认 .env 配置文件..."
    echo "SECRET_KEY=$(openssl rand -hex 32)" > .env
    echo "LOG_LEVEL=INFO" >> .env
    echo "DEBUG=false" >> .env
    echo "SEED=true" >> .env
    echo ".env 文件已创建，请根据需要修改。"
fi

# 5. 创建必要的目录
mkdir -p logs database/defaults database/backups database/profiles database/projects database/navigations database/blogs

echo "部署环境准备完成！"
echo "请在 1Panel 的 Supervisor 中配置启动命令:"
echo "命令: $(pwd)/.venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 'backend.app:create_app()'"
echo "运行目录: $(pwd)"
