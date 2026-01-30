from typing import List, Optional

from sqlalchemy import select

from backend.data.database import db
from backend.data.models.project import Project


class ProjectRepository:
    def __init__(self):
        self.model = Project

    def get_all(self, public_only: bool = False) -> List[Project]:
        stmt = select(self.model)
        if public_only:
            stmt = stmt.filter_by(is_public=True)
        stmt = stmt.order_by(self.model.order.desc(), self.model.created_at.desc())
        return list(db.session.scalars(stmt).all())

    def get_by_uuid(self, uuid: str) -> Optional[Project]:
        stmt = select(self.model).filter_by(uuid=uuid)
        return db.session.scalars(stmt).first()

    def create(self, data: dict) -> Project:
        # Handle tags list to string conversion if needed
        if "tags" in data and isinstance(data["tags"], list):
            data["tags"] = ",".join(data["tags"])

        proj = self.model(**data)
        db.session.add(proj)
        db.session.commit()
        return proj

    def update(self, uuid: str, data: dict) -> Optional[Project]:
        proj = self.get_by_uuid(uuid)
        if not proj:
            return None

        # Handle tags list to string conversion
        if "tags" in data and isinstance(data["tags"], list):
            data["tags"] = ",".join(data["tags"])

        for key, value in data.items():
            if hasattr(proj, key):
                setattr(proj, key, value)

        db.session.commit()
        return proj

    def delete(self, uuid: str) -> bool:
        proj = self.get_by_uuid(uuid)
        if not proj:
            return False

        db.session.delete(proj)
        db.session.commit()
        return True
