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

## 四、推荐的推进方向（Roadmap 建议）

如果你现在「有点没有方向」，可以从下面几个维度逐步推进：

### 1. 完善基础文档

- **README**：目前只写了项目名，可以补充：
  - 项目简介、技术栈说明
  - 本地启动步骤（复制本文件中的关键部分）
  - 目录结构简要说明
- **API 文档**：`docs/api.md` 已经较完整，可以：
  - 为每个模块补充更多示例请求 / 响应
  - 标注权限要求（游客 / 登录用户 / 管理员 / 超管）
  - 为错误码、错误场景增加说明

### 2. 前端体验与组件库完善

- 梳理已有页面：
  - `pages/Blogs.vue` / `pages/blog/Detail.vue`
  - `pages/Navigations.vue`
  - `pages/Projects.vue` 与 `pages/project/FileTreeView.vue`, `Overview.vue`
  - `pages/user/Profile.vue`, `Settings.vue` 等
- 可以做的事情：
  - 统一列表页的 UI（基于 `CommonTable`）。
  - 完善 Markdown 编辑与展示体验（基于 `MarkdownContainer`）。
  - 优化头像上传 / 裁剪流程（基于 `AvatarCropper`）。
  - 完善多语言（`locales/manifests/en.json`, `jp.json`, `zh-CN.json`）内容，让文案更完整。

### 3. 权限与安全细节

- 后端 `auth` / `user` 模块已经有基础的登录、注册、头像等接口，可以继续：
  - 细化角色权限（游客 / 成员 / 管理员 / 超管）的可见内容和可操作范围。
  - 在前端路由守卫中根据用户角色控制访问（如 `admin` 页面仅管理员可见）。
  - 固化统一的认证机制（JWT / Session / Cookie），并在 `frontend/src/utils/request.ts` 中集中处理。

### 4. 项目模块（Project）的深入

- 后端已支持：
  - 获取项目列表、详情
  - 读取项目文件树与文件内容
- 可以进一步：
  - 在前端的 `project` 页面里实现更好用的文件浏览器（树形 + 代码高亮）。
  - 支持按项目内搜索文件 / 关键字（可考虑后端实现简单搜索接口）。
  - 将项目 README、元数据等以更直观的方式展示。

### 5. 工程化与质量

- 增加自动化：
  - 基本的单元测试（后端：`pytest`；前端：`vitest` 或 `jest`）。
  - 简单的格式化 / Lint（Python：`ruff` / `black`；前端：`eslint` + `prettier`）。
- 配置 CI（如 GitHub Actions）：
  - push / PR 时自动运行测试与 Lint。

---

## 五、代码风格与约定（可逐步补充）

暂定一些推荐约定，后续可根据实际情况在此文件继续完善：

- **后端**
  - 尽量保持「Controller（API 层）薄，Service 层厚」的结构。
  - 所有对数据库的直接访问统一放在 `repositories` 层。
  - API 返回统一使用 `docs/api.md` 中的响应格式（包含 `level`、`message`、`data`）。

- **前端**
  - 新建页面尽量使用组合式 API（`<script setup lang="ts">`）。
  - 所有 HTTP 调用通过 `frontend/src/services/` 层统一封装，不直接在组件里写 `fetch/axios`。
  - 全局状态放入 Pinia store，页面仅关心展示与交互。

---

## 六、下一步可以怎么做？

如果你现在希望「立刻动手做点什么」，可以从下面任选一个小目标开始：

1. **补全 README**：把本文件中「环境准备」「启动方式」精简版搬到 `README.md`。
2. **检查并统一前端接口调用**：确认所有页面都通过 `services` 层调用后端，而不是散落的请求。
3. **为某个模块补充前端管理页**：例如给导航或项目模块增加一个更完善的后台管理 UI。
4. **完善多语言文案**：补全 `en/jp/zh-CN` 三套文案，顺便梳理文案命名规范。

当你完成以上任意一个目标时，就会自然地产生下一步要做什么的想法，可以把新的约定继续写回本文件，逐步把它发展成项目的「贡献指南」与「架构说明」。

