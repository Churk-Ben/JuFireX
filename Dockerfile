# 使用官方 Python 3.13 Slim 镜像，轻量且符合需求
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
# 1. 防止 Python 生成 .pyc 文件
# 2. 确保 Python 输出无缓冲（实时日志）
# 3. 设置时区为上海
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai

# 使用清华源替换 Debian 默认源 (加速 apt update)
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources

# 安装系统级依赖
# 虽然 slim 镜像很精简，但有些 Python 包可能需要编译工具
# 如果遇到 Pillow 或其他库的安装问题，可能需要解开下面的注释
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装 (使用清华源加速 pip)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码
# 我们只复制 backend 目录，保持结构一致性
COPY backend/ ./backend/

# 创建必要的目录（虽然 config.py 会自动创建，但在 Docker 中显式声明是个好习惯）
RUN mkdir -p logs database/defaults database/backups database/profiles database/projects database/navigations database/blogs

# 暴露端口
EXPOSE 8000

# 启动命令
# 使用 gunicorn 作为生产级 WSGI 服务器
# -w 4: 4个 worker 进程
# -b 0.0.0.0:8000: 绑定所有网络接口
# --access-logfile -: 将访问日志输出到标准输出
# --error-logfile -: 将错误日志输出到标准错误
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "backend.app:create_app()"]
