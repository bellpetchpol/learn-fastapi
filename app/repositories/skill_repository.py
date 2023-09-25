from math import ceil
from ..dependencies import db_dependency
from ..models import Skills
from ..dtos.request_dtos import PageResponseDto


class SkillRepository:
    def __init__(self, db: db_dependency):
        self.db = db

    def add(self, new_skill: Skills) -> Skills:
        self.db.add(new_skill)
        self.db.commit()
        return new_skill

    def read_by_id(self, skill_id: int) -> Skills | None:
        return self.db.query(Skills).filter(Skills.id == skill_id).first()

    def read_all(self, page: int, size: int) -> PageResponseDto[Skills]:
        offset = size * (page - 1)
        query = self.db.query(Skills)
        query = query.order_by(Skills.id)
        total = query.count()
        pages = ceil(total / size)

        result = PageResponseDto[Skills](
            items=query.offset(offset).limit(size).all(),
            page=page,
            pages=pages,
            size=size,
            total=total
        )

        return result
