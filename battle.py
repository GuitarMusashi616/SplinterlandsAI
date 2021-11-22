import random

from battle_order import BattleOrder
from buff_registry import BuffRegistry
from target_registry import TargetRegistry
from util import decks_each_have_an_alive_card, get_allies_enemies, determine_winner


class Battle:
    @classmethod
    def begin(cls, home, oppo, seed=None) -> bool:
        """True if home victory else False"""

        if type(seed) is int:
            random.seed(seed)

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

                enemy.take_damage_from(card)
            max_repeat -= 1

        result = determine_winner(home, oppo)
        if result == "home wins":
            return True


