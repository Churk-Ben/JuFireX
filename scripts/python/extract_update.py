from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path
import shutil
import sys
from zipfile import ZIP_DEFLATED, ZipFile

import generate_version


UPDATE_ITEMS = [
    "backend",
    "static",
    # "requirements.txt",
    # "docker-compose.yml",
    # "Dockerfile",
]


def resolve_project_root(explicit_root: str | None) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    return Path(__file__).resolve().parents[2]


def copy_entry(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(
            src,
            dst,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            dirs_exist_ok=True,
        )
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def create_zip(source_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zip_file:
        for path in source_dir.rglob("*"):
            if path.is_file():
                zip_file.write(path, path.relative_to(source_dir))


def build_update_package(
    project_root: Path, output_dir: Path, clean: bool
) -> tuple[list[str], list[str]]:
    copied: list[str] = []
    missing: list[str] = []

    if clean and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for item in UPDATE_ITEMS:
        src = project_root / item
        dst = output_dir / item
        if src.exists():
            copy_entry(src, dst)
            copied.append(item)
            continue

        if item == "static":
            fallback_static = project_root / "frontend" / "static"
            if fallback_static.exists():
                copy_entry(fallback_static, dst)
                copied.append("static(来源: frontend/static)")
                continue

        missing.append(item)

    return copied, missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="提取并打包 JuFireX 服务器更新包")
    parser.add_argument(
        "--project-root",
        default=None,
        help="项目根目录，默认自动推断为 JuFireX 根目录",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="输出目录，默认 <project-root>/temp_update",
    )
    parser.add_argument(
        "--zip-path",
        default=None,
        help="zip 文件路径，默认 <project-root>/update_package_时间戳.zip",
    )
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="只生成目录，不生成 zip",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="不清理已有输出目录，直接覆盖写入",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = resolve_project_root(args.project_root)

    # Generate version info
    print("正在生成版本信息...")
    generate_version.main()

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else (project_root / "temp_update")
    )

    copied, missing = build_update_package(
        project_root, output_dir, clean=not args.no_clean
    )

    zip_path: Path | None = None
    if not args.no_zip:
        default_zip_name = (
            f"update_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )
        zip_path = (
            Path(args.zip_path).expanduser().resolve()
            if args.zip_path
            else (project_root / default_zip_name)
        )
        create_zip(output_dir, zip_path)

    print(f"项目目录: {project_root}")
    print(f"提取目录: {output_dir}")
    if copied:
        print("已提取内容:")
        for item in copied:
            print(f"  - {item}")
    if missing:
        print("未找到内容:")
        for item in missing:
            print(f"  - {item}")
    if zip_path:
        print(f"更新包 zip: {zip_path}")
    print("完成。将提取目录或 zip 上传到服务器并放到 temp_update 后执行 update.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
