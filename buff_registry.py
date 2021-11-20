from typing import Union, Tuple, List

from buff import MeleeBuff, Buff, HealthBuff, RangedBuff, MagicBuff, ArmorBuff, SpeedBuff
from buff_factory import BuffFactory
from card import Card


class BuffRegistry:
    alias = {
        'weaken': 'health-',
    }

    buffs = {  # applies to whole team
        'melee+': BuffFactory(MeleeBuff, 1),
        'melee-': BuffFactory(MeleeBuff, -1, True),
        'ranged+': BuffFactory(RangedBuff, 1),
        'ranged-': BuffFactory(RangedBuff, -1, True),
        'magic+': BuffFactory(MagicBuff, 1),
        'magic-': BuffFactory(MagicBuff, -1, True),
        'health+': BuffFactory(HealthBuff, 1),
        'health-': BuffFactory(HealthBuff, -1, True),
        'armor+': BuffFactory(ArmorBuff, 1),
        'armor-': BuffFactory(ArmorBuff, -1, True),
        'speed+': BuffFactory(SpeedBuff, 1),
        'speed-': BuffFactory(SpeedBuff, -1, True),
    }

    @classmethod
    def lookup(cls, key: str) -> BuffFactory:
        if key in cls.alias:
            key = cls.alias[key]

        if key not in cls.buffs:
            raise KeyError(f"ability {key} is not in {cls.buffs}")

        return cls.buffs[key]

    @classmethod
    def from_card(cls, src: Card, allies: List[Card], enemies: List[Card]):
        for ability in src.abilities:
            try:
                factory = cls.lookup(ability)
                factory.instantiate_buff(src, allies, enemies)
            except KeyError:
                continue

    @classmethod
    def instantiate_all(cls, deck1: List[Card], deck2: List[Card]):
        for card in deck1:
            cls.from_card(card, deck1, deck2)

        for card in deck2:
            cls.from_card(card, deck2, deck1)
