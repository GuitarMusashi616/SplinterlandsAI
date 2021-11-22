from battle import Battle
from card_bridge import CardBridge
from util import reset_cards
import random


class Deck:
    """Wraps a card list, can be sorted to determine the best deck"""
    def __init__(self, cards):
        self.cards = cards

    def __repr__(self):
        string = ""
        for card in self.cards:
            string += repr(card) + '\n'
        return string+'\n'

    def __lt__(self, other):
        # random.seed(10)
        self_names = [x.name for x in self.cards]
        other_names = [x.name for x in other.cards]
        result = not Battle.begin(CardBridge.collect(self_names), CardBridge.collect(other_names))
        return result

