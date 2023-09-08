from .database import Base
from sqlalchemy import Column, Integer, String, Enum
from .dtos.character_dtos import CharacterRoleEnum


class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    role = Column(type_=Enum(CharacterRoleEnum, name="character_role"))
    hit_points = Column(Integer)
    attack = Column(Integer)
    defence = Column(Integer)
    magic = Column(Integer)
