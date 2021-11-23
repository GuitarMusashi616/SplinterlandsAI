import random
from enum import Enum

from battle_order import BattleOrder
from buff_registry import BuffRegistry
from target_registry import TargetRegistry
from util import decks_each_have_an_alive_card, get_allies_enemies

class Result(Enum):
    WIN = 1
    LOSE = 2
    DRAW = 3

    def get_score(self):
        if self.WIN:
            return 1
        elif self.DRAW:
            return 0.5
        else:
            return 0

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
        max_repeat = 100

        while decks_each_have_an_alive_card(home, oppo) and max_repeat>0:
            for card in battle_order:
                allies, enemies = get_allies_enemies(card, home, oppo)
                enemy = TargetRegistry.choose_for(card, allies, enemies)

                if not enemy:
                    continue

                if not card.can_attack(allies):
                    continue

                enemy.take_damage_from(card, verbose)

            if battle_record:
                battle_record.save(home, oppo)
            max_repeat -= 1

        return cls.determine_winner(home, oppo)




