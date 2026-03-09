## 本地开发环境准备与启动

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
- 删除 Windows 平台的 `node_modules` 目录（如果存在），重新安装 Linux 平台的前端依赖

### 3. 启动开发环境

同样在项目根目录执行：

```bash
./start.sh
```

脚本会：

- 启动后端：在 `.venv-linux` 中运行 `backend/app.py`（Flask），监听 `0.0.0.0:5000`
- 启动前端：在 `frontend` 目录执行 `npm run dev`，默认 Vite Dev Server（通常是 `http://localhost:5173`）

在浏览器中访问前端地址即可开始调试，前端会通过代理 / 直接请求后端 `/api/...` 接口。
