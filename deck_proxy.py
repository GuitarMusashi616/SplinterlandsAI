from typing import List

from battle import Battle, Result
from card import Card
from card_bridge import CardBridge
from elo import Elo


class DeckProxy:
    name_to_df_card = {x.Card: x for x in CardBridge.df.itertuples()}

    def __init__(self, df_cards):
        self.df_cards = df_cards
        self.df_cards.sort(key=self.sort_order, reverse=True)
        self.elo = 1000

    def __repr__(self):
        string = f'ELO: {self.elo} [\n'
        for x in self.df_cards:
            string += f'\t{x.Card}\n'

        return string + ']'

    def instantiate(self) -> List[Card]:
        return [CardBridge.card_from_row(df_card) for df_card in self.df_cards]

    def battle(self, other, verbose=False) -> Result:
        result = Battle.begin(self.instantiate(), other.instantiate(), verbose=verbose)
        self.elo, other.elo = Elo.battle(self.elo, other.elo, result.value)
        return result

    # def __lt__(self, other):
    #     return self.elo < other.elo

    def __gt__(self, other) -> bool:
        return self.battle(other) == Result.WIN

    @staticmethod
    def sort_order(x):
        hp = x.Health
        if x.AttackType != 'melee':
            hp = -hp

        return x.Role == 'summoner', x.AttackType == 'melee', hp

    @classmethod
    def collect(cls, cards: List[str]):
        return cls.from_string(cards)

    @classmethod
    def from_cards(cls, cards: List[Card]):
        return cls.from_string([card.name for card in cards])

    @classmethod
    def from_string(cls, card_names: List[str]):
        deck = []
        for name in card_names:
            deck.append(cls.name_to_df_card[name])
        return DeckProxy(deck)


