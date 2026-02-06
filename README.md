## JuFireX 开发指导

本指南面向未来继续维护 / 扩展 JuFireX 的开发者，帮助你快速了解项目结构、启动方式，以及可以继续推进的方向。

---

## 一、项目整体结构概览

- **后端 (`backend/`)**：Flask 应用，提供 RESTful API，实际接口详见 `docs/api.md`。
  - `backend/app.py`：Flask 应用入口，`create_app` 工厂 + CORS + 数据库初始化 + 蓝图注册。
  - `backend/api/`：按领域拆分的蓝图（`auth.py`, `blog.py`, `navigation.py`, `project.py`, `user.py`）。
  - `backend/data/`：数据库相关（`database.py`、`models/`、`repositories/`），以及 `seed.py`、`seed_large.py` 数据填充脚本。
  - `backend/services/`：领域服务层，封装业务逻辑，避免在视图里写太多逻辑。
  - `backend/core/`：基础设施，如日志、权限/安全工具等。

- **前端 (`frontend/`)**：Vue 3 + Vite + TypeScript 单页应用。
  - `frontend/src/pages/`：页面路由视图，例如登录/注册、博客列表与详情、导航、项目等。
  - `frontend/src/components/`：可复用组件（如 `avatar-cropper`、`common-table`、`markdown-container` 等）。
  - `frontend/src/stores/`：Pinia 状态管理（如 `user`、`theme`）。
  - `frontend/src/services/`：访问后端 API 的封装层（`auth.ts`, `blog.ts`, `project.ts` 等）。
  - `frontend/src/utils/request.ts`：HTTP 请求封装，统一处理 baseURL、错误提示等。

- **启动脚本**
  - `setup-linux.sh`：在 Linux 下初始化 Python 虚拟环境 `.venv-linux`，并安装前端依赖。
  - `start.sh`：同时启动后端（通过 `uv` 运行 `backend/app.py`）与前端（`npm run dev`），用于本地开发。

---

## 二、本地开发环境准备与启动

### 1. 环境要求

- **系统**：Linux（脚本已针对 Linux 做了适配；Windows 使用 PowerShell 脚本）
- **Python**：版本见项目根目录 `pyproject.toml` / `.python-version`
- **Node.js**：建议与 `frontend` 中 `package-lock.json` 匹配的 LTS 版本
- **包管理**：
  - 后端：`uv`（通过 `setup-linux.sh` 调用）
  - 前端：`npm`

### 2. 一次性初始化（Linux）

在项目根目录执行：

```bash
./setup-linux.sh
```

该脚本会：

- 创建 / 更新 `.venv-linux` 虚拟环境并安装 Python 依赖
- 删除 Windows 平台的 `node_modules`，重新安装 Linux 平台的前端依赖

### 3. 启动开发环境

同样在项目根目录执行：

```bash
./start.sh
```

脚本会：

- 启动后端：在 `.venv-linux` 中运行 `backend/app.py`（Flask），监听 `0.0.0.0:5000`
- 启动前端：在 `frontend` 目录执行 `npm run dev`，默认 Vite Dev Server（通常是 `http://localhost:5173`）

在浏览器中访问前端地址即可开始调试，前端会通过代理 / 直接请求后端 `/api/...` 接口。

---

## 三、日常开发流程建议

### 1. 新功能开发基本步骤

以「新增某个业务模块」为例（如以后要加 `Task` 模块）：

1. **后端**
   - 在 `backend/data/models/` 中定义模型（如 `task.py`）。
   - 在 `backend/data/repositories/` 中为模型写仓储访问逻辑。
   - 在 `backend/services/` 中编写业务服务（如 `task_service.py`）。
   - 在 `backend/api/` 中新增蓝图文件 `task.py`，定义路由与请求 / 响应数据结构。
   - 在 `backend/api/__init__.py` 里注册新的蓝图。
   - 如有需要，更新 `docs/api.md`，补充 API 文档。

2. **前端**
   - 在 `frontend/src/services/` 中添加 `task.ts`，封装对后端 API 的调用。
   - 在 `frontend/src/pages/` 下新增对应页面，如 `pages/admin/Tasks.vue` 或用户侧页面。
   - 在 `frontend/src/router/index.ts` 中增加路由配置。
   - 如需状态管理或缓存，在 `frontend/src/stores/` 中新增或扩展 store。
   - 使用已有的基础组件（如 `CommonTable`, `MarkdownContainer`, `ScrollContainer` 等）快速搭建 UI。

3. **测试与联调**
   - 启动 `./start.sh`，前后端联调。
   - 利用前端页面或一个简单的 API 测试页（如 `pages/ApiTest.vue`）来手动测试。

### 2. 调试与日志

- 后端使用 `backend/core/Logger.py` 提供的日志工具，`backend/app.py` 中已在启动时初始化日志记录器。
- 在开发中可以：
  - 在服务层或 API 层适当增加 `logger.info/debug`，观察关键流程。
  - 慎用过多的 `print`，统一使用日志工具，便于以后切换日志级别和输出位置。

### 3. 数据库与示例数据

- 使用 `backend/data/database.py` 的 `init_db` 进行数据库初始化。
- 可以通过 `backend/data/seed.py` 或 `seed_large.py` 预置开发环境用的测试数据（具体内容可在需要时打开文件查看）。
- 建议约定：
  - 本地开发使用单独的数据库文件 / 实例，避免污染生产。
  - 在文档中补充：如何重置本地数据库、如何导入示例数据（后续可以在这里继续完善）。

---
