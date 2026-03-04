#!/bin/bash

# JuFireX 安全更新脚本
# 使用方法: 
# 1. 确保新代码已上传到服务器 (例如 /opt/1panel/apps/jufirex/temp_update)
# 2. 运行此脚本: ./update.sh

APP_DIR="/opt/1panel/apps/jufirex"
BACKUP_DIR="${APP_DIR}/backups/$(date +%Y%m%d_%H%M%S)"
TEMP_UPDATE_DIR="${APP_DIR}/temp_update"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}开始执行 JuFireX 安全更新流程...${NC}"

# 1. 检查更新文件是否存在
if [ ! -d "$TEMP_UPDATE_DIR" ]; then
    echo -e "${RED}错误: 未找到更新文件目录 $TEMP_UPDATE_DIR${NC}"
    echo "请先将新版本代码上传到该目录"
    exit 1
fi

# 2. 创建备份
echo -e "${GREEN}[1/5] 正在备份当前版本...${NC}"
mkdir -p "$BACKUP_DIR"
# 备份后端代码
if [ -d "${APP_DIR}/backend" ]; then
    cp -r "${APP_DIR}/backend" "${BACKUP_DIR}/"
fi
# 备份前端静态文件
if [ -d "${APP_DIR}/static" ]; then
    cp -r "${APP_DIR}/static" "${BACKUP_DIR}/"
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

# 3. 更新文件
echo -e "${GREEN}[2/5] 正在应用更新...${NC}"

# 更新后端代码
if [ -d "${TEMP_UPDATE_DIR}/backend" ]; then
    rm -rf "${APP_DIR}/backend"
    cp -r "${TEMP_UPDATE_DIR}/backend" "${APP_DIR}/"
    echo "后端代码已更新"
fi

# 更新前端静态文件
if [ -d "${TEMP_UPDATE_DIR}/static" ]; then
    rm -rf "${APP_DIR}/static"
    cp -r "${TEMP_UPDATE_DIR}/static" "${APP_DIR}/"
    echo "前端静态文件已更新"
fi

# 更新配置文件
if [ -f "${TEMP_UPDATE_DIR}/requirements.txt" ]; then
    cp "${TEMP_UPDATE_DIR}/requirements.txt" "${APP_DIR}/"
fi
if [ -f "${TEMP_UPDATE_DIR}/docker-compose.yml" ]; then
    cp "${TEMP_UPDATE_DIR}/docker-compose.yml" "${APP_DIR}/"
fi
if [ -f "${TEMP_UPDATE_DIR}/Dockerfile" ]; then
    cp "${TEMP_UPDATE_DIR}/Dockerfile" "${APP_DIR}/"
fi

# 4. 重建并重启后端容器
echo -e "${GREEN}[3/5] 正在重建后端容器...${NC}"
cd "$APP_DIR" || exit

# 检查是否需要重新构建镜像 (依赖变更)
REBUILD_NEEDED=false
if [ -f "${TEMP_UPDATE_DIR}/requirements.txt" ] || [ -f "${TEMP_UPDATE_DIR}/Dockerfile" ]; then
    REBUILD_NEEDED=true
fi

if [ "$REBUILD_NEEDED" = true ]; then
    echo "检测到依赖或配置变更，正在重新构建镜像..."
    docker-compose build --no-cache
fi

echo "重启服务..."
docker-compose up -d

# 5. 清理临时文件
echo -e "${GREEN}[4/5] 清理临时文件...${NC}"
rm -rf "$TEMP_UPDATE_DIR"

echo -e "${GREEN}[5/5] 更新完成!${NC}"
echo -e "${YELLOW}如果遇到问题，可以使用备份文件回滚: ${BACKUP_DIR}${NC}"
echo -e "请检查网站是否正常运行: http://YOUR_DOMAIN"
