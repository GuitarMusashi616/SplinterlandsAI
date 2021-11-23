from typing import List

from battle import Battle, Result
from card import Card
from card_bridge import CardBridge
from elo import Elo
from util import reposition


class DeckProxy:
    def __init__(self, df_cards):
        self.df_cards = df_cards
        self.elo = 1000

    def __repr__(self):
        string = f'ELO: {self.elo} [\n'
        for x in self.df_cards:
            string += f'\t{x.Card}\n'

        return string + ']'

    def instantiate(self) -> List[Card]:
        return reposition([CardBridge.card_from_row(df_card) for df_card in self.df_cards])

    def battle(self, other) -> Result:
        result = Battle.begin(self.instantiate(), other.instantiate())
        self.elo, other.elo = Elo.battle(self.elo, other.elo, result.get_score())
        return result

    def __gt__(self, other) -> bool:
        return self.battle(other) == Result.WIN