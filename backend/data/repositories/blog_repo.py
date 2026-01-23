from typing import List, Dict
from backend.config import Config
from backend.data.repositories.file_repo import FileRepository

class BlogRepository(FileRepository):
    def __init__(self):
        super().__init__(Config.BLOGS_DIR)

    def get_by_author(self, author_id: int) -> List[Dict]:
        all_blogs = self.list_items()
        return [b for b in all_blogs if b.get('author_id') == author_id]
