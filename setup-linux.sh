#!/usr/bin/env bash
# 双系统共用磁盘时，从 Windows 切到 Linux 后执行此脚本：
# - 创建/更新 .venv-linux 并安装 Python 依赖
# - 删除 Windows 下安装的 node_modules，按 Linux 平台重装前端依赖
set -e
cd "$(dirname "$0")"

echo ">>> 配置 Python 环境 (.venv-linux)..."
UV_PROJECT_ENVIRONMENT=.venv-linux uv sync --link-mode=copy

echo ""
echo ">>> 重装前端依赖 (Linux 平台)..."
rm -rf frontend/node_modules
(cd frontend && npm i)

echo ""
echo ">>> 完成。之后直接运行 ./start.sh 即可。"
