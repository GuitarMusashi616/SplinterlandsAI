import pandas as pd
import numpy as np

from card import Card
from util import AttackType, Role, Element


class CardBridge:
    """Wraps a DataFrame of card records, returns Card instances"""
    dic = {
        np.nan: AttackType.NONE,
        'melee': AttackType.MELEE,
        'ranged': AttackType.RANGED,
        'magic': AttackType.MAGIC,
        'summoner': Role.SUMMONER,
        'monster': Role.MONSTER,
        'fire': Element.FIRE,
        'water': Element.WATER,
        'earth': Element.EARTH,
        'life': Element.LIFE,
        'death': Element.DEATH,
        'dragon': Element.DRAGON,
        'neutral': Element.NEUTRAL,
    }

    df = pd.read_excel('cards.xlsx')

    @staticmethod
    def retrieve_ability_list(card: Card):
        ls = []
        if card.Ability1 is not np.nan:
            ls.append(card.Ability1)
        if card.Ability2 is not np.nan:
            ls.append(card.Ability2)
        return ls

    @classmethod
    def card_from_row(cls, card_row):
        inst = Card(
            card_row.Card,
            cls.dic[card_row.Role],
            cls.dic[card_row.Element],
            card_row['Mana Cost'],
            card_row.Dmg,
            cls.dic[card_row['Attack Type']],
            card_row.Speed,
            card_row.Health,
            card_row.Armor,
            cls.retrieve_ability_list(card_row),
        )
        return inst

    @classmethod
    def card(cls, i):
        return cls.card_from_row(cls.df.iloc[i])

    @classmethod
    def collect(cls, card_names):
        deck = []
        card_names = set(card_names)
        for i in range(len(cls.df)):
            if cls.df.iloc[i].name in card_names:
                deck.append(cls.card(i))
        return deck

    @classmethod
    def get_home_visitor(cls):
        home = [cls.card(x) for x in range(len(cls.df) // 2)]
        visitor = [cls.card(x) for x in range(len(cls.df) // 2, len(cls.df))]
        return home, visitor