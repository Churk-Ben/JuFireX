from datetime import datetime
import json
from pathlib import Path
import subprocess


def get_git_info(cwd):
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
                ["git", "log", "-1", "--pretty=%B"], cwd=cwd, stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        return {
            "commit_hash": commit_hash,
            "branch": branch,
            "commit_date": commit_date,
            "message": message,
        }
    except subprocess.CalledProcessError:
        return {
            "commit_hash": "unknown",
            "branch": "unknown",
            "commit_date": "unknown",
            "message": "unknown",
        }
    except FileNotFoundError:
        return {
            "commit_hash": "no-git",
            "branch": "no-git",
            "commit_date": "no-git",
            "message": "no-git",
        }


def main():
    # Resolve project root (assuming this script is in scripts/python/)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parents[1]

    version_file = project_root / "version"
    output_file = project_root / "backend" / "version.json"

    # Read semantic version
    try:
        semantic_version = version_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        semantic_version = "0.0.0"

    # Get git info
    git_info = get_git_info(project_root)

    # Build version data
    version_data = {
        "version": semantic_version,
        "build_time": datetime.now().isoformat(),
        **git_info,
    }

    # Write to file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=2, ensure_ascii=False)

    print(f"Version info generated at {output_file}")
    # print(json.dumps(version_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
