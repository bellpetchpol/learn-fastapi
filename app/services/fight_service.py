from typing import Annotated

from fastapi import Depends
from ..repositories.character_repository import CharacterRepository
from ..dependencies import auth_user_dependency
from ..dtos.fight_dtos import GetResultDto
from random import sample, randint

from ..models import Characters


class FightService:
    def __init__(self,
                 character_repo: Annotated[CharacterRepository, Depends()],
                 auth_user: auth_user_dependency,
                 ):
        self.character_repo = character_repo
        self.auth_user = auth_user

    def start(self) -> list[GetResultDto]:
        response = list[GetResultDto]()
        page_response = self.character_repo.read_all(
            1, 100, self.auth_user.user_id)
        players = page_response.items
        while len(players) > 1:
            # shuffle player turn
            players = sample(players, len(players))
            for player in players:
                if player.hit_points <= 0:
                    break
                attacker = player
                defenders = [
                    character for character in players if character.id != player.id and character.hit_points > 0]
                if (len(defenders) == 1):
                    defender = defenders[0]
                else:
                    defender = defenders[randint(0, len(defenders) - 1)]
                if randint(0, 1) == 0:
                    # attack with weapon
                    damage = attacker.weapon.damage + attacker.attack
                    attack_with = attacker.weapon.name
                else:
                    # attack with skill
                    skills = attacker.skills
                    if (len(skills) == 1):
                        skill = skills[0]
                    else:
                        skill = skills[randint(0, len(skills) - 1)]
                    # skill = skills[randint(0, len(skills) - 1)]
                    damage = attacker.magic + skill.damage
                    attack_with = skill.name
                if damage - defender.defence < 0:
                    total_damage = 0
                else:
                    total_damage = damage - defender.defence
                defender.hit_points -= total_damage
                result = GetResultDto(
                    attacker=f"{attacker.name} HP {attacker.hit_points}",
                    defender=f"{defender.name} HP {defender.hit_points}",
                    message=f"{attacker.name} ใช้ {attack_with} ({damage}) โจมตี {defender.name} ({defender.defence}) สร้างความเสียหาย {total_damage}"
                )
                index = 0
                for character in players:
                    if defender.id == character.id:
                        character.hit_points = defender.hit_points
                        if character.hit_points <= 0:
                            players.pop(index)
                    index += 1

                if defender.hit_points <= 0:
                    result.message += " ถึงตาย!"

                response.append(result)
        survivor = players[0]
        response.append(GetResultDto(
            attacker=survivor.name,
            message=f"{survivor.name} เป็นผู้ชนะ!",
            defender=""
        ))
        return response

    # def start(self) -> list[GetResultDto]:
    #     response = list[GetResultDto]()
    #     page_response = self.character_repo.read_all(
    #         1, 100, self.auth_user.user_id)
    #     characters = page_response.items
    #     player_ids: list[int] = []
    #     is_game_over = False
    #     while is_game_over == False:
    #         for character in characters:
    #             if character.hit_points > 0:
    #                 player_ids.append(character.id)

    #         turn_order_ids: list[int] = sample(player_ids, len(player_ids))
    #         for player_id in turn_order_ids:
    #             attackers = [
    #                 character for character in characters if character.id == player_id]
    #             defenders = [
    #                 character for character in characters if character.id != player_id and character.id in player_ids]
    #             if len(attackers) > 0:
    #                 attacker = attackers[0]
    #             defender = defenders[randint(0, len(defenders) - 1)]
    #             if randint(0, 1) == 0:
    #                 # attack with weapon
    #                 damage = attacker.weapon.damage + attacker.attack
    #                 attack_with = attacker.weapon.name
    #             else:
    #                 # attack with skill
    #                 skills = attacker.skills
    #                 skill = skills[randint(0, len(skills) - 1)]
    #                 damage = attacker.magic + skill.damage
    #                 attack_with = skill.name

    #             defender.hit_points -= damage
    #             result = GetResultDto(
    #                 attacker=attacker.name,
    #                 defender=defender.name,
    #                 message=f"{attacker.name} ใช้ {attack_with} โจมตี {defender.name} สร้างความเสียหาย {damage}"
    #             )
    #             if defender.hit_points <= 0:
    #                 result.message += " ถึงตาย!"

    #             response.append(result)

    #         if len([character.id for character in characters if character.hit_points > 0]) == 1:
    #             is_game_over = True

    #     return response
