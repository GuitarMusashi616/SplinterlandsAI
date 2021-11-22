from typing import List

from card import Card
from enums import AttackType
from target import DefaultTarget, OpportunityTarget, SnipeTarget, SneakTarget, Target
from util import get_monster_pos


class TargetRegistry:
    mods = {
        'opportunity': OpportunityTarget(),
        'snipe': SnipeTarget(),
        'sneak': SneakTarget(),
    }

    @classmethod
    def check_exceptions(cls, targeting: Target, card: Card, allies: List[Card]):
        """If the card is melee and 1st position and has opportunity/sneak, return default targeting"""
        if card.attack_type == AttackType.MELEE \
                and isinstance(targeting, (OpportunityTarget, SneakTarget)) \
                and get_monster_pos(card, allies) == 1:
            return DefaultTarget()
        return targeting

    @classmethod
    def choose_for(cls, card: Card, allies: List[Card], enemies: List[Card]) -> Card:
        targeting = DefaultTarget()
        for ability in card.abilities:
            if ability in cls.mods:
                targeting = cls.mods[ability]
                break

        targeting = cls.check_exceptions(targeting, card, allies)
        return targeting.choose(enemies)
