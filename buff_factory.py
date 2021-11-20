from typing import List
from card import Card


class BuffFactory:
    def __init__(self, cls: type, delta: int, is_offensive=False):
        self.cls = cls
        self.delta = delta
        self.is_offensive = is_offensive

    def instantiate_buff(self, src: Card, allies: List[Card], enemies: List[Card]):
        target_cards = enemies if self.is_offensive else allies
        for target in target_cards:
            self.cls(self.delta, target, src)
