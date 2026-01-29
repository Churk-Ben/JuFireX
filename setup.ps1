# 双系统共用磁盘时，从 Linux 切到 Windows 后执行此脚本：
# - 创建/更新 .venv 并安装 Python 依赖
# - 删除 Linux 下安装的 node_modules，按 Windows 平台重装前端依赖
# 在项目根目录用 PowerShell 运行: .\setup.ps1

Set-Location $PSScriptRoot

Write-Host ">>> 配置 Python 环境 (.venv)..." -ForegroundColor Cyan
uv sync

Write-Host ""
Write-Host ">>> 重装前端依赖 (Windows 平台)..." -ForegroundColor Cyan
Remove-Item -Recurse -Force frontend\node_modules -ErrorAction SilentlyContinue
Set-Location frontend; npm i; Set-Location ..

Write-Host ""
Write-Host ">>> 完成。之后直接运行 .\start.ps1 即可。" -ForegroundColor Green
