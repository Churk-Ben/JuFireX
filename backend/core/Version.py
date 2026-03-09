# ------------------------------------------------------------
# @author: Churk
# @status: 完成
# @description: 版本模块
# ------------------------------------------------------------

from datetime import datetime
import subprocess
import os

from backend.config import Config


def get_git_info(cwd) -> dict:
    # 优先使用环境变量中的 Git 信息
    if os.environ.get("GIT_COMMIT_HASH"):
        return {
            "commit_hash": os.environ["GIT_COMMIT_HASH"],
            "branch": os.environ.get("GIT_BRANCH", "unknown"),
            "commit_date": os.environ.get("GIT_COMMIT_DATE", "unknown"),
        }

    try:
        commit_hash = (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=cwd,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=cwd,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
        commit_date = (
            subprocess.check_output(
                ["git", "log", "-1", "--format=%cd", "--date=iso"],
                cwd=cwd,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
        message = (
            subprocess.check_output(
                ["git", "log", "-1", "--pretty=%B"],
                cwd=cwd,
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
        return {
            "commit_hash": commit_hash,
            "branch": branch,
            "commit_date": commit_date,
        }
    except subprocess.CalledProcessError:
        return {
            "commit_hash": "unknown",
            "branch": "unknown",
            "commit_date": "unknown",
        }
    except FileNotFoundError:
        return {
            "commit_hash": "no-git",
            "branch": "no-git",
            "commit_date": "no-git",
        }


def get_version_info() -> dict:
    # 从 VERSION_FILE 读取语义版本
    try:
        semantic_version = Config.VERSION_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        semantic_version = "0.0.0"

    # 从 git 仓库获取版本信息
    git_info = get_git_info(Config.PROJECT_ROOT)

    # 构建版本字典
    version_data = {
        "version": semantic_version,
        "query_time": datetime.now().isoformat(),
        **git_info,
    }

    return version_data


# TODO: 此类以后将承包项目历史提交功能的查询
