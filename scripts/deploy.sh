#!/bin/bash

# 获取脚本所在目录的上一级目录 (项目根目录)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 切换到项目根目录
cd "$PROJECT_ROOT"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}开始执行 JuFireX Docker 部署流程...${NC}"

# 1. 检查环境依赖
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: 未找到 Docker，请先安装 Docker 和 Docker Compose${NC}"
    exit 1
fi

if ! docker compose version &> /dev/null && ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: 未找到 Docker Compose 插件或命令${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}错误: 未找到 npm，请先安装 Node.js 和 npm${NC}"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}错误: 未找到 git，请先安装 git${NC}"
    exit 1
fi

# 2. 创建 .env 配置文件 (如果不存在)
if [ ! -f .env ]; then
    echo -e "${GREEN}正在创建默认 .env 配置文件...${NC}"
    echo "SECRET_KEY=$(openssl rand -hex 32)" > .env
    echo "LOG_LEVEL=INFO" >> .env
    echo "DEBUG=false" >> .env
    echo "SEED=true" >> .env
    echo ".env 文件已创建，请根据需要修改。"
fi

# 3. 创建必要的目录
echo -e "${GREEN}正在创建数据目录...${NC}"
mkdir -p logs \
    database/defaults \
    database/backups \
    database/profiles \
    database/projects \
    database/navigations \
    database/blogs

# 4. 构建前端
echo -e "${GREEN}正在构建前端项目...${NC}"
if [ -d "frontend" ]; then
    cd frontend
    echo "安装依赖..."
    npm install
    echo "构建项目..."
    npm run build
    cd ..
    
    # 将构建产物复制到 static 目录
    if [ -d "frontend/static" ]; then
        echo "前端构建成功，正在同步静态文件..."
        mkdir -p static
        cp -r frontend/static/* static/
    else
        echo -e "${RED}前端构建失败: 未找到 frontend/static 目录${NC}"
        # 不强制退出，因为可能只运行后端
    fi
else
    echo -e "${YELLOW}警告: 未找到 frontend 目录，跳过前端构建${NC}"
fi

# 5. 启动服务
echo -e "${GREEN}正在启动 Docker 容器...${NC}"

# 获取 git 信息并导出为环境变量，供 docker-compose 使用
export GIT_COMMIT_HASH=$(git rev-parse --short HEAD)
export GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
export GIT_COMMIT_DATE=$(git log -1 --format=%cd --date=iso)

# 优先尝试 docker compose (V2), 失败则尝试 docker-compose (V1)
if docker compose version &> /dev/null; then
    docker compose up -d --build
else
    docker-compose up -d --build
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}部署成功!${NC}"
    echo -e "后端服务已在端口 8000 上运行。"
    echo -e "请配置 Nginx 反向代理指向 http://127.0.0.1:8000"
else
    echo -e "${RED}部署失败，请检查 Docker 日志${NC}"
    exit 1
fi
