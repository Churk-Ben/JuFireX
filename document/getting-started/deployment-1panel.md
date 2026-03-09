# 1Panel 部署指南

本指南将指导你如何使用 1Panel 面板部署 JuFireX 项目。

## 前置条件

1.  已安装 1Panel 面板。
2.  在 1Panel 中已安装 **OpenResty** (用于 Web 服务) 和 **Docker** (用于容器管理)。

## 第一步：后端部署 (Docker)

后端采用 Python Flask 开发，推荐使用 Docker 容器化部署。

### 1. 上传代码

将整个项目代码上传到服务器的某个目录，例如 `/opt/1panel/apps/jufirex`。
你可以使用 1Panel 的「文件」功能或 FTP/SFTP 工具上传。

### 2. 构建镜像

在 1Panel 的「容器」->「镜像」->「构建镜像」中操作，或者直接在终端执行：

```bash
cd /opt/1panel/apps/jufirex
docker build -t jufirex-backend:latest .
```

### 3. 创建容器

在 1Panel 的「容器」->「容器」列表点击「创建容器」：

- **名称**: `jufirex-backend`
- **镜像**: 选择刚才构建的 `jufirex-backend:latest`
- **端口**:
  - 容器端口: `8000`
  - 主机端口: `8000` (或者你喜欢的其他端口)
- **挂载**:
  - `./database` -> `/app/database` (读写) - **重要：用于持久化数据库**
  - `./logs` -> `/app/logs` (读写)
  - `./.env` -> `/app/.env` (只读)
  - `./version` -> `/app/version` (只读)
- **环境**: (可选，如果不想用 .env 文件)
  - `SECRET_KEY`: 设置一个随机字符串
  - `TZ`: `Asia/Shanghai`
- **启动命令**: 默认即可 (`gunicorn ...`)

点击确认创建并启动。确保容器状态为 "Running"。

## 第二步：前端部署 (静态网站)

前端采用 Vue.js + Vite 开发，需要构建为静态文件。

### 1. 本地构建

在你的本地开发机上执行：

```bash
cd frontend
npm install
npm run build
```

构建完成后，会生成 `frontend/static` 目录。

### 2. 上传静态文件

在 1Panel 的「网站」->「静态网站」中创建一个新网站：

- **主域名**: 你的域名 (例如 `jufirex.com` 或 IP)
- **代号**: `jufirex`

网站创建后，进入网站目录（通常是 `/opt/1panel/apps/openresty/openresty/www/sites/jufirex/index`），删除默认文件，将本地构建好的 `frontend/static` 目录下的**所有文件**上传到这个目录。

### 3. 配置反向代理 (关键)

为了让前端能访问后端 API，需要配置 Nginx 反向代理。

在 1Panel 「网站」列表中，点击刚才创建的网站 -> 「配置」 -> 「反向代理」 -> 「添加反向代理」：

- **代理名称**: `api`
- **代理目录**: `/api` (注意：这是前端请求的前缀)
- **目标 URL**: `http://127.0.0.1:8000` (注意：这里填后端的地址和端口)

保存配置。

### 4. 处理前端路由 (可选但推荐)

如果前端使用了 History 模式路由（即 URL 不带 `#`），需要在 Nginx 配置文件中添加 try_files。
点击「配置文件」，在 `location / { ... }` 块中添加：

```nginx
location / {
    try_files $uri $uri/ /index.html;
    index index.html index.htm;
}
```

(1Panel 默认的静态网站配置通常已经包含了类似的 index 配置，但 try_files 需要手动确认)

> 一个完整的前端配置示例：

```nginx
server {
    listen 5173 ;
    listen 5000 ;
    server_name jufirex.com jufirex.com;
    index index.php index.html index.htm default.php default.htm default.html;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $http_connection;
    access_log /www/sites/jufirex/log/access.log main;
    error_log /www/sites/jufirex/log/error.log;
    location ^~ /.well-known/acme-challenge {
        allow all;
        root /usr/share/nginx/html;
    }
    location / {
        # 解决刷新 404 问题
        try_files $uri $uri/ /index.html;
    }
    root /www/sites/jufirex/index;
    error_page 404 /404.html;
    limit_conn perserver 300;
    limit_conn perip 25;
    limit_rate 512k;
    include /www/sites/jufirex/proxy/*.conf;
}
```

## 第三步：验证

1.  访问你的域名/IP，应该能看到前端页面。
2.  尝试登录或进行操作，检查是否能正常调用后端 API。
3.  查看后端容器日志 (`docker logs jufirex-backend`) 确认无报错。

## 常见问题

- **数据库在哪里？**: 默认使用 SQLite，文件位于映射的 `database` 目录中。
- **上传图片失败**: 检查 `database/blogs` 等目录的写入权限，Docker 容器内通常需要 root 权限或正确的用户 ID (UID)。
- **API 404**: 检查反向代理配置是否生效，尝试访问 `http://你的域名/api/` 看是否有响应。
