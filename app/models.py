from .database import Base
from sqlalchemy import String, Enum
from sqlalchemy.orm import mapped_column, Mapped
from .dtos.character_dtos import CharacterRoleEnum


class Characters(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=True)
    role: Mapped[CharacterRoleEnum] = mapped_column(
        Enum(CharacterRoleEnum, name="character_role"))
    hit_points: Mapped[int]
    attack: Mapped[int]
    defence: Mapped[int]
    magic: Mapped[int]
    
    def __repr__(self) -> str:
        return f"Character(id={self.id}!r, name={self.name}!r, role={self.role.value}!r, hit_points={self.hit_points}!r, attack={self.attack}!r, defence={self.defence}!r, magic={self.magic}!r)"
