import random
from enum import Enum

from battle_order import BattleOrder
from buff_registry import BuffRegistry
from target_registry import TargetRegistry
from util import decks_each_have_an_alive_card, get_allies_enemies
from enums import Result


class Battle:
    @staticmethod
    def determine_winner(home, oppo):
        home_alive = any(card.health > 0 for card in home)
        oppo_alive = any(card.health > 0 for card in oppo)
        if home_alive and not oppo_alive:
            return Result.WIN
        elif oppo_alive and not home_alive:
            return Result.LOSE
        else:
            return Result.DRAW
            # raise ValueError(f"Game is not finished or everyone is dead \n{home} \n{oppo}")

    @classmethod
    def begin(cls, home, oppo, seed=None, verbose=False, battle_record=None) -> Result:
        """True if home victory else False"""

        if type(seed) is int:
            random.seed(seed)

        if battle_record:
            battle_record.save(home, oppo)

        BuffRegistry.instantiate_all(home, oppo)

        battle_order = BattleOrder(home, oppo)
        MAX_REPEAT = 100
        repeats = MAX_REPEAT

        while decks_each_have_an_alive_card(home, oppo) and repeats>0:
            if verbose:
                print(f"START OF ROUND {MAX_REPEAT+1-repeats}\n")
            for card in battle_order:
                allies, enemies = get_allies_enemies(card, home, oppo)
                enemy = TargetRegistry.choose_for(card, allies, enemies)
                card.try_heal()

                if not enemy:
                    continue

                if not card.can_attack(allies):
                    continue

                enemy.take_damage_from(card, verbose)

            if battle_record:
                battle_record.save(home, oppo)
            repeats -= 1


        return cls.determine_winner(home, oppo)




