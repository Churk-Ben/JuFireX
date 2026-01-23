import json
import os
from pathlib import Path
from typing import List, Optional, TypeVar, Dict, Any
from .base import BaseRepository

T = TypeVar("T", bound=Dict[str, Any])


class FileRepository(BaseRepository[T, str]):
    """
    基于文件系统的仓储通用实现 (JSON/Markdown等)
    这里简化为以文件名为 ID，内容为字典的模式
    """

    def __init__(self, directory: Path):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def _get_file_path(self, id: str) -> Path:
        # 假设 ID 就是文件名 (不含扩展名，或包含，这里简化处理)
        # 具体实现可能需要子类重写，这里默认处理 .json
        return self.directory / f"{id}.json"

    def get(self, id: str) -> Optional[T]:
        file_path = self._get_file_path(id)
        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 注入 ID 到数据中，方便使用
                if isinstance(data, dict):
                    data["id"] = id
                return data
        except Exception:
            return None

    def list(self, **kwargs) -> List[T]:
        results = []
        if not self.directory.exists():
            return results

        for filename in os.listdir(self.directory):
            if filename.endswith(".json"):
                file_id = filename[:-5]  # remove .json
                item = self.get(file_id)
                if item:
                    # 简单的内存过滤
                    match = True
                    for k, v in kwargs.items():
                        if item.get(k) != v:
                            match = False
                            break
                    if match:
                        results.append(item)
        return results

    def create(self, entity: T) -> T:
        # 必须确保 entity 中有 ID，或者自动生成 ID
        if "id" not in entity:
            raise ValueError("Entity must have an 'id' field for FileRepository")

        file_id = str(entity["id"])
        file_path = self._get_file_path(file_id)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(entity, f, ensure_ascii=False, indent=2)

        return entity

    def update(self, entity: T) -> T:
        return self.create(entity)  # 文件覆盖即更新

    def delete(self, id: str) -> bool:
        file_path = self._get_file_path(id)
        if file_path.exists():
            os.remove(file_path)
            return True
        return False

    def count(self, **kwargs) -> int:
        return len(self.list(**kwargs))
