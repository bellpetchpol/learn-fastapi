from datetime import datetime
from .database import Base
from sqlalchemy import String, Enum, DateTime
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


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(25), unique=True, index=True)
    full_name: Mapped[str | None]
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)
    create_by: Mapped[str] = mapped_column(String(25))
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),
        default=datetime.utcnow())
    update_by: Mapped[str | None] = mapped_column(String(25))
    update_date: Mapped[datetime] = mapped_column(DateTime(timezone=True),
        default=datetime.utcnow())

    def __repr__(self) -> str:
        return f"Users(id={self.id}!r, username={self.username}!r, full_name={self.full_name}!r, hashed_password={self.hashed_password}!r, disabled={self.disabled}!r, create_by={self.create_by}!r, create_date={self.create_date}!r, update_by={self.update_by}!r, update_date={self.update_date}!r)"
