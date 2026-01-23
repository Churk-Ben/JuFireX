from typing import List, Dict, Any
from backend.config import Config
from .file_repo import FileRepository


class BlogRepository(FileRepository[Dict[str, Any]]):
    def __init__(self):
        super().__init__(Config.BLOGS_DIR)

    def get_by_author(self, author_id: int) -> List[Dict[str, Any]]:
        # 这是一个示例扩展方法
        all_blogs = self.list()
        # 假设 blog 数据中有 author_id 字段
        return [b for b in all_blogs if b.get("author_id") == author_id]
