## 项目整体结构概览

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
