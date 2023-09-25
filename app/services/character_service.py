from typing import Annotated
from fastapi import Depends, HTTPException

from ..models import Characters, Weapons
from ..dtos.character_dtos import AddCharacterDto, CharacterRoleEnum, GetCharacterDto, UpdateCharacterDto
from ..dtos.request_dtos import PageResponseDto
from ..repositories.character_repository import CharacterRepository
from ..repositories.skill_repository import SkillRepository
from ..dependencies import auth_user_dependency
from ..dtos.weapon_dtos import AddWeaponDto
from random import randint, choice


class CharacterService:
    def __init__(self,
                 repo: Annotated[CharacterRepository, Depends()],
                 auth_user: auth_user_dependency,
                 skill_repo: Annotated[SkillRepository, Depends()]
                 ):
        self.repo = repo
        self.auth_user = auth_user
        self.skill_repo = skill_repo

    def read_all(self, page: int, size: int) -> PageResponseDto[GetCharacterDto]:
        db_page_response = self.repo.read_all(
            page=page, size=size, user_id=self.auth_user.user_id)
        page_response = PageResponseDto[GetCharacterDto](
            **db_page_response.model_dump())
        return page_response

    def read_by_id_return_db_character(self, character_id: int) -> Characters:
        db_character = self.repo.read_by_id(
            character_id=character_id, user_id=self.auth_user.user_id)
        if db_character is None:
            raise HTTPException(
                status_code=404, detail=f"Character id: {character_id} not found")
        return db_character

    def read_by_id(self, character_id: int) -> GetCharacterDto:
        db_character = self.read_by_id_return_db_character(
            character_id=character_id)
        return GetCharacterDto.model_validate(db_character)

    def add(self, new_character: AddCharacterDto) -> GetCharacterDto:
        db_character = Characters(**new_character.model_dump())
        db_character.user_id = self.auth_user.user_id
        db_character = self.repo.add(new_character=db_character)
        character = GetCharacterDto.model_validate(db_character)
        return character

    def add_weapon(self, character_id: int, new_weapon: AddWeaponDto) -> GetCharacterDto:
        db_character = self.read_by_id_return_db_character(
            character_id=character_id)
        db_character = self.repo.add_weapon(
            db_character=db_character,
            new_weapon=Weapons(**new_weapon.model_dump())
        )
        character = GetCharacterDto.model_validate(db_character)
        return character

    def add_skill(self, character_id: int, skill_id: int) -> GetCharacterDto:
        db_character = self.read_by_id_return_db_character(
            character_id=character_id)
        db_skill = self.skill_repo.read_by_id(skill_id=skill_id)
        if db_skill is None:
            raise HTTPException(
                status_code=404, detail=f"Skill id: {skill_id} not found")
        db_character = self.repo.add_skill(
            db_character=db_character,
            db_skill=db_skill
        )
        character = GetCharacterDto.model_validate(db_character)
        return character

    def update(self, character_id: int, update_character: UpdateCharacterDto) -> GetCharacterDto:
        db_character = self.read_by_id_return_db_character(
            character_id=character_id)
        updated_db_character = self.repo.update(
            db_character=db_character, update_character=update_character
        )
        result = GetCharacterDto.model_validate(updated_db_character)
        return result

    def delete(self, character_id: int) -> None:
        db_character = self.read_by_id_return_db_character(
            character_id=character_id)
        self.repo.delete(db_character=db_character)

    def randint_hp(self) -> int:
        return randint(100, 150)

    def randint_attack(self) -> int:
        return randint(10, 20)

    def randint_defence(self) -> int:
        return randint(5, 25)

    def randint_magic(self) -> int:
        return randint(5, 20)

    def dummy_character(self, character_name: str) -> AddCharacterDto:
        character_choices = [CharacterRoleEnum.Knight,
                             CharacterRoleEnum.Mage, CharacterRoleEnum.Cleric]
        return AddCharacterDto(
            name=character_name,
            role=choice(character_choices),
            hit_points=self.randint_hp(),
            attack=self.randint_attack(),
            defence=self.randint_defence(),
            magic=self.randint_magic()
        )

    def dummy_weapon(self) -> AddWeaponDto:
        weapons = [
            AddWeaponDto(name="ดาบ", damage=10),
            AddWeaponDto(name="หอก", damage=12),
            AddWeaponDto(name="โซ่", damage=11),
            AddWeaponDto(name="แส้", damage=9)
        ]
        return weapons[randint(0, 3)]

    def dummy(self) -> None:

        characters = [
            self.dummy_character("พี่เบล"),
            self.dummy_character("โน้ตซ่า"),
            self.dummy_character("เทค"),
            self.dummy_character("จั้ม"),
            self.dummy_character("โอลิเวีย"),
            self.dummy_character("แอลเค"),
            self.dummy_character("ยูอิ")
        ]
        
        for character in characters:
            db_character = self.add(character)
            self.add_weapon(db_character.id, self.dummy_weapon())
            weapon_set = set()
            for x in range(0,3):
                y = randint(0,2) + 1
                weapon_set.add(y)
            for weapon_id in weapon_set:
                self.add_skill(db_character.id, weapon_id)
