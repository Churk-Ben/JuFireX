# JuFire Studio - 工作室主页系统

一个基于 Flask + SocketIO + SQLite 的现代化工作室主页系统，采用 GitHub 风格设计。

## 功能特性

### 🏠 主页功能

- 工作室简介展示
- 项目卡片展示（支持图片、描述、GitHub链接、演示链接）
- 统计信息展示（项目数量、团队成员、GitHub Stars等）
- 用户注册登录入口
- 响应式设计，支持移动端

### 👥 用户系统

- **四级权限系统**：
  - 🔴 **超级管理员**：完整系统管理权限
  - 🟡 **管理员**：项目管理权限
  - 🔵 **成员**：导航页访问权限
  - ⚪ **游客**：基础浏览权限

### 📊 管理功能

- **项目管理**（管理员+）：
  - 创建、编辑、删除项目
  - 设置精选项目
  - 项目统计信息
- **用户管理**（超级管理员）：
  - 用户角色管理
  - 用户状态控制
  - 用户详情查看

### 🧭 导航系统

- 快速访问链接
- 开发工具导航
- 学习资源链接
- 常用服务链接

### 💬 实时通信

- 基于 SocketIO 的实时通知
- 系统消息推送

## 技术栈

- **后端**: Python Flask + Flask-SocketIO
- **数据库**: SQLite + SQLAlchemy
- **前端**: Bootstrap 5 + Font Awesome
- **实时通信**: Socket.IO
- **样式**: GitHub 风格暗色主题

## 快速开始

### 1. 环境要求

- Python 3.7+
- pip

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python app.py
```

### 4. 访问应用

打开浏览器访问：`http://localhost:5000`

### 5. 默认账号

- **用户名**: `admin`
- **密码**: `admin123`
- **角色**: 超级管理员

## 项目结构

```plaintext
JuFireStudio/
├── app.py                 # 主应用文件
├── requirements.txt       # 依赖包列表
├── README.md              # 项目说明
├── studio.db              # SQLite 数据库（运行后生成）
├── user_data/             # 用户上传数据
├── static/                # 静态文件
│   ├── css/               # 样式目录
│   │   └── style.css      # 自定义样式
│   └── js/                # 脚本目录
│       ├── main.js        # 全局主脚本
│       ├── profile.js     # 个人主页脚本
│       ├── admin-navigation.js # 后台导航管理脚本
│       └── ...            # 其他页面脚本
└── templates/             # 模板文件
    ├── base.html          # 基础模板
    ├── index.html         # 主页
    ├── login.html         # 登录页
    ├── register.html      # 注册页
    ├── profile.html       # 个人主页
    ├── navigation.html    # 前台导航页
    └── admin/             # 管理页面
        ├── projects.html  # 项目管理
        ├── users.html     # 用户管理
        ├── navigation.html # 导航管理
        └── studio_info.html # 工作室信息管理
```

## 用户权限说明

| 功能 | 游客 | 成员 | 管理员 | 超级管理员 |
|:---|:---:|:---:|:---:|:---:|
| 浏览主页 | ✅ | ✅ | ✅ | ✅ |
| 用户注册 | ✅ | ✅ | ✅ | ✅ |
| 个人主页 | ✅ | ✅ | ✅ | ✅ |
| 导航页面 | ❌ | ✅ | ✅ | ✅ |
| 项目管理 | ❌ | ❌ | ✅ | ✅ |
| 导航管理 | ❌ | ❌ | ✅ | ✅ |
| 用户管理 | ❌ | ❌ | ❌ | ✅ |
| 工作室信息管理 | ❌ | ❌ | ❌ | ✅ |

## API 接口

### 项目相关

- `POST /api/projects` - 创建项目
- `PUT /api/projects/<id>/featured` - 切换精选状态
- `DELETE /api/projects/<id>` - 删除项目

### 用户相关

- `PUT /api/users/<id>/role` - 更新用户角色
- `PUT /api/users/<id>/status` - 切换用户状态
- `GET /api/users/<id>` - 获取用户详情
- `DELETE /api/users/<id>` - 删除用户

### 导航链接相关

- `GET /api/navigation` - 获取所有导航链接
- `POST /api/navigation` - 创建导航链接
- `PUT /api/navigation/<id>` - 更新导航链接
- `DELETE /api/navigation/<id>` - 删除导航链接

### 工作室信息相关

- `GET /api/studio_info` - 获取工作室信息
- `PUT /api/studio_info` - 更新工作室信息

## 自定义配置

### 修改工作室信息

您可以通过访问后台管理页面的 “工作室信息” 标签页来直接修改工作室的各项信息，包括名称、描述、联系邮箱和 GitHub 地址等。所作修改将实时生效。

### 修改样式主题

编辑 `static/css/style.css` 文件中的 CSS 变量：

```css
:root {
    --github-bg: #0d1117;          /* 背景色 */
    --github-secondary: #161b22;    /* 次要背景色 */
    --github-accent: #58a6ff;       /* 强调色 */
    /* ... 其他颜色变量 */
}
```

## 开发说明

### 添加新功能

1. 在 `app.py` 中添加路由和API
2. 创建对应的模板文件
3. 在 `main.js` 中添加前端交互逻辑
4. 更新样式文件（如需要）

### 数据库迁移

如需修改数据库结构：

1. 修改 `app.py` 中的模型定义
2. 删除 `studio.db` 文件
3. 重新运行应用以创建新的数据库结构

## 部署建议

### 生产环境

1. 使用 Gunicorn 或 uWSGI 作为 WSGI 服务器
2. 配置 Nginx 作为反向代理
3. 使用 PostgreSQL 或 MySQL 替代 SQLite
4. 启用 HTTPS
5. 配置环境变量管理敏感信息

### Docker 部署

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目主页：[GitHub Repository]
- 问题反馈：[GitHub Issues]
- 邮箱：[your-email@example.com]

---

**JuFire Studio** - 让创意点燃未来 🔥
