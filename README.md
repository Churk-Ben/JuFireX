# JuFireX Studio

## 功能特性

### 👥 用户系统

- **四级权限系统**：
  - 🔴 **超级管理员**：完整系统管理权限
  - 🟡 **管理员**：所有项目的管理权限
  - 🔵 **成员**：拥有自己的博客空间、项目存档空间
  - ⚪ **游客及未注册用户**：基础浏览权限、导航页访问权限

### 📊 管理功能

- **项目管理**（管理员+）：
  - 创建、编辑、删除项目
  - 设置精选项目
  - 项目统计信息
  - 项目文档管理
- **用户管理**（超级管理员）：
  - 用户角色管理
  - 用户状态控制
  - 用户详情查看

### 🧭 导航系统

- 快速访问链接
- 开发工具导航
- 学习资源链接
- 常用服务链接


## 项目结构
```plaintext
JuFireX/
├── database/                   # 数据存储根目录
│   ├── profiles/               # 用户数据库 (SQLite)
│   ├── projects/               # 项目文件存储 (File System)
│   ├── blogs/                  # 博客文件存储 (File System)
│   └── navs/                   # 导航数据库 (SQLite)
├── frontend/                   # 现有前端代码
└── backend/
    ├── legacy/                 # [保留] 旧代码，仅作参考
    ├── Logger.py               # [复用] 现有的日志模块
    ├── app.py                  # 新的后端入口
    ├── config.py               # 配置文件
    ├── api/                    # [API 层] 路由与控制器
    │   ├── __init__.py
    │   ├── auth.py             # 认证接口
    │   ├── user.py             # 用户管理接口
    │   ├── project.py          # 项目管理接口
    │   └── nav.py              # 导航接口
    ├── core/                   # [业务层] 核心逻辑
    │   ├── __init__.py
    │   ├── security.py         # 权限与认证逻辑 (4层权限)
    │   └── services/           # 业务服务
    └── data/                   # [数据层] 数据访问对象 (DAO/Repository)
        ├── __init__.py
        ├── database.py         # 数据库连接管理 (多库支持)
        ├── models/             # 数据模型定义
        │   ├── user.py
        │   └── nav.py
        └── repositories/       # 具体的数据操作类
            ├── user_repo.py    # 操作 profiles 数据库
            ├── nav_repo.py     # 操作 navs 数据库
            ├── project_repo.py # 操作 projects 文件夹结构
            └── blog_repo.py    # 操作 blogs 文件夹结构
```