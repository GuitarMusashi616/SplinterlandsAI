import random
from abc import ABC, abstractmethod
from typing import List, Optional

from card import Card
from enums import AttackType


class Target(ABC):
    @staticmethod
    def select_first(enemies: List[Card]):
        for card in enemies:
            if card.health > 0:
                return card

    @staticmethod
    def select_last(enemies: List[Card]):
        for card in enemies[::-1]:
            if card.health > 0:
                return card

    @abstractmethod
    def choose(self, enemies: List[Card]) -> Card:
        ...


class DefaultTarget(Target):
    """Returns the first alive monster from the deck"""
    def choose(self, enemies: List[Card]) -> Optional[Card]:
        return self.select_first(enemies)


class SneakTarget(Target):
    """Returns the last monster in deck with health > 0"""
    def choose(self, enemies: List[Card]) -> Optional[Card]:
        return self.select_last(enemies)


class SnipeTarget(Target):
    """Returns ranged, magic, or no attack monster not in 1st position"""
    def choose(self, enemies: List[Card]) -> Card:
        first_rejected = False
        for card in enemies:
            if card.health > 0:
                if card.attack_type in {AttackType.RANGED, AttackType.MAGIC, AttackType.NONE} and first_rejected:
                    return card
                first_rejected = True
        return self.select_first(enemies)  # if nothing to snipe then just hit the first position


class OpportunityTarget(Target):
    """Returns the lowest health enemy monster > 0"""
    def choose(self, enemies: List[Card]) -> Optional[Card]:
        candidates = sorted(enemies, key=lambda x: (x.health, random.random()))
        for card in candidates:
            if card.health > 0:
                return card
