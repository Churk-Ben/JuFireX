#!/bin/bash

# JuFireX 安全更新脚本
# 使用方法: chmod +x ./update.sh && ./update.sh

# 获取脚本所在目录的上一级目录 (项目根目录)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 切换到项目根目录
cd "$PROJECT_ROOT"

APP_DIR="$PROJECT_ROOT"
BACKUP_DIR="${APP_DIR}/backups/$(date +%Y%m%d_%H%M%S)"
OPENRESTY_INDEX_DIR="/opt/1panel/www/sites/jufirex/index"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}开始执行 JuFireX 自动更新流程...${NC}"

# 1. 检查环境依赖
if ! command -v git &> /dev/null; then
    echo -e "${RED}错误: 未找到 git, 请先安装 git${NC}"
    exit 1
fi


# 2. 创建备份
echo -e "${GREEN}[1/5] 正在备份当前版本...${NC}"
mkdir -p "$BACKUP_DIR"

# 备份后端代码 (虽然有 git，但保留备份以防万一)
if [ -d "${APP_DIR}/backend" ]; then
    cp -r "${APP_DIR}/backend" "${BACKUP_DIR}/"
fi

# 备份前端静态文件
if [ -d "${APP_DIR}/frontend/static" ]; then
    cp -r "${APP_DIR}/frontend/static" "${BACKUP_DIR}/static_backup"
fi

# 备份配置文件
if [ -f "${APP_DIR}/requirements.txt" ]; then
    cp "${APP_DIR}/requirements.txt" "${BACKUP_DIR}/"
fi
if [ -f "${APP_DIR}/docker-compose.yml" ]; then
    cp "${APP_DIR}/docker-compose.yml" "${BACKUP_DIR}/"
fi
if [ -f "${APP_DIR}/Dockerfile" ]; then
    cp "${APP_DIR}/Dockerfile" "${BACKUP_DIR}/"
fi

echo -e "备份已保存至: ${BACKUP_DIR}"

# 3. 拉取最新代码
echo -e "${GREEN}[2/5] 正在拉取最新代码...${NC}"

# 固定使用 Gitee，幂等设置（执行多次结果一样）
GITEE_URL="https://gitee.com/church-zhang/JuFireX.git"
GITHUB_URL="https://github.com/Churk-Ben/JuFireX.git"

# 检查并设置 origin 为 Gitee（如果已经是则不操作）
CURRENT_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ "$CURRENT_URL" != "$GITEE_URL" ]; then
    echo "配置远程仓库为 Gitee..."
    if [ -z "$CURRENT_URL" ]; then
        git remote add origin "$GITEE_URL"
    else
        git remote set-url origin "$GITEE_URL"
    fi
fi

# 保留 GitHub 作为备用 remote（如果不存在则添加）
if ! git remote get-url github &>/dev/null; then
    git remote add github "$GITHUB_URL" 2>/dev/null || true
fi

# 获取最新分支信息
git fetch origin main
if [ $? -ne 0 ]; then
    echo -e "${RED}获取远程分支失败，请检查网络连接${NC}"
    exit 1
fi

# 强制重置到远程 main（丢弃所有本地修改，以远程为准）
git reset --hard origin/main
if [ $? -ne 0 ]; then
    echo -e "${RED}重置本地仓库失败${NC}"
    exit 1
fi

echo -e "${GREEN}代码已更新至最新版本${NC}"

# 4. 同步前端静态文件 (不再服务器构建)
echo -e "${GREEN}[3/5] 正在同步前端静态文件...${NC}"

# 检查仓库中是否存在预构建的静态文件
if [ -d "${APP_DIR}/frontend/static" ]; then
    echo "找到预构建的静态文件，正在同步..."
    
    # 同步到 OpenResty 目录
    if [ -d "${OPENRESTY_INDEX_DIR}" ]; then
        # 清空旧文件
        rm -rf "${OPENRESTY_INDEX_DIR:?}/"*
        # 复制新文件
        cp -r "${APP_DIR}/frontend/static/"* "${OPENRESTY_INDEX_DIR}/"
        echo "前端静态文件已同步至 OpenResty index 目录"
    else
        echo -e "${YELLOW}警告: 未找到 OpenResty 目录 ${OPENRESTY_INDEX_DIR}，跳过同步${NC}"
    fi

    # 同步到项目根目录 static (以备不时之需，如 Docker 挂载)
    # if [ -d "${APP_DIR}/static" ]; then
    #     rm -rf "${APP_DIR}/static"/*
    # else
    #     mkdir -p "${APP_DIR}/static"
    # fi
    # cp -r "${APP_DIR}/frontend/static/"* "${APP_DIR}/static/"
    # echo "前端静态文件已同步至项目根目录 static"
else
    echo -e "${RED}错误: 未找到预构建的 static 目录 (${APP_DIR}/frontend/static)${NC}"
    echo -e "${YELLOW}提示: 请确保在本地构建前端并将 frontend/static 目录提交到 Git${NC}"
    exit 1
fi

cd "$APP_DIR"

# 5. 重建并重启后端容器
echo -e "${GREEN}[4/5] 正在重建后端容器...${NC}"

# 获取 git 信息并导出为环境变量，供 docker-compose 使用
export GIT_COMMIT_HASH=$(git rev-parse --short HEAD)
export GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
export GIT_COMMIT_DATE=$(git log -1 --format=%cd --date=iso)
echo "Git Info: ${GIT_COMMIT_HASH} / ${GIT_BRANCH} / ${GIT_COMMIT_DATE}"

# 强制重新构建并重启服务
if docker compose version &> /dev/null; then
    docker compose up -d --build jufirex-backend
else
    docker-compose up -d --build jufirex-backend
fi

# 6. 清理
echo -e "${GREEN}[5/5] 正在清理未使用的镜像...${NC}"

# 清理未使用的镜像
docker image prune -f

echo -e "${GREEN}更新完成!${NC}"
echo -e "${YELLOW}如果遇到问题，可以使用 git reset 回滚代码，或查看备份: ${BACKUP_DIR}${NC}"
echo -e "请检查网站是否正常运行。"
