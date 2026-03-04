#!/usr/bin/env bash
# Linux 使用 .venv-linux，与 Windows 的 .venv 分开；node_modules 也需在 Linux 下重装。
# 从 Windows 切到 Linux 后请先执行: ./setup-linux.sh
# 请用 ./start.sh 运行，不要 source。
cd "$(dirname "$0")"

BACKEND_PID=
FRONTEND_PID=
cleanup() {
  echo
  echo "正在停止服务..."
  [[ -n $BACKEND_PID  ]] && kill $BACKEND_PID  2>/dev/null || true
  [[ -n $FRONTEND_PID ]] && kill $FRONTEND_PID 2>/dev/null || true
  exit 0
}
trap cleanup SIGINT SIGTERM

echo "启动后端..."
(
  if [[ -f .venv-linux/bin/activate ]]; then source .venv-linux/bin/activate; fi
  UV_PROJECT_ENVIRONMENT=.venv-linux uv run ./backend/app.py
) &
BACKEND_PID=$!

echo "启动前端..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!

wait
