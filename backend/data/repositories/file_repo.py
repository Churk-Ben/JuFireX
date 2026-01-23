import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional

# 文件仓库类
class FileRepository:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    # 获取项目路径
    def _get_item_path(self, item_id: str) -> Path:
        return self.base_path / item_id

    # 列出所有项目
    def list_items(self) -> List[Dict]:
        """扫描项目目录，返回所有有效项目的元数据"""
        items = []
        if not self.base_path.exists():
            return []
            
        for entry in os.scandir(self.base_path):
            if entry.is_dir():
                metadata = self.get_metadata(entry.name)
                if metadata:
                    metadata['id'] = entry.name
                    items.append(metadata)
        return items

    def get_metadata(self, item_id: str) -> Optional[Dict]:
        meta_path = self._get_item_path(item_id) / "metadata.json"
        if meta_path.exists():
            try:
                with open(meta_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def save_metadata(self, item_id: str, metadata: Dict):
        item_path = self._get_item_path(item_id)
        os.makedirs(item_path, exist_ok=True)
        
        meta_path = item_path / "metadata.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)

    def create_item(self, item_id: str, metadata: Dict) -> bool:
        item_path = self._get_item_path(item_id)
        if item_path.exists():
            return False
        self.save_metadata(item_id, metadata)
        return True

    def delete_item(self, item_id: str):
        item_path = self._get_item_path(item_id)
        if item_path.exists():
            shutil.rmtree(item_path)

    def exists(self, item_id: str) -> bool:
        return self._get_item_path(item_id).exists()
