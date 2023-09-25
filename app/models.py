from datetime import datetime
from .database import Base
from sqlalchemy import Column, ForeignKey, String, Enum, DateTime, Table, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .dtos.character_dtos import CharacterRoleEnum

character_skill_table = Table(
    "characters_skills",
    Base.metadata,
    Column("id", type_=Integer, primary_key=True, index=True),
    Column("character_id", ForeignKey("characters.id")),
    Column("skill_id", ForeignKey("skills.id"))
)


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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["Users"] = relationship(back_populates="characters")
    weapon: Mapped["Weapons"] = relationship(back_populates="character")
    skills: Mapped[list["Skills"]] = relationship(
        secondary=character_skill_table)

    def __repr__(self) -> str:
        return f"Character(id={self.id}!r, name={self.name}!r, role={self.role.value}!r, hit_points={self.hit_points}!r, attack={self.attack}!r, defence={self.defence}!r, magic={self.magic}!r, user_id={self.user_id}!r)"


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

    characters: Mapped[list["Characters"]
                       ] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"Users(id={self.id}!r, username={self.username}!r, full_name={self.full_name}!r, hashed_password={self.hashed_password}!r, disabled={self.disabled}!r, create_by={self.create_by}!r, create_date={self.create_date}!r, update_by={self.update_by}!r, update_date={self.update_date}!r)"


class Weapons(Base):
    __tablename__ = "weapons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    damage: Mapped[int]

    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    character: Mapped["Characters"] = relationship(back_populates="weapon")

    def __repr__(self) -> str:
        return f"Weapons(id={self.id}!r, name={self.name}, damage={self.damage}, character_id={self.character_id})"


class Skills(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    damage: Mapped[int]
