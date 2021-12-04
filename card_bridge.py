import pandas as pd
import numpy as np

from card import Card
from enums import AttackType, Role, Element


class CardBridge:
    """Wraps a DataFrame of card records, returns Card instances"""
    dic = {
        np.nan: AttackType.NONE,
        'none':AttackType.NONE,
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
    def retrieve_ability_list(card_row):
        ls = []
        if card_row.Ability1 is not np.nan:
            ls.append(card_row.Ability1)
        if card_row.Ability2 is not np.nan:
            ls.append(card_row.Ability2)
        return ls

    @classmethod
    def card_from_row(cls, card_row):
        try:
            inst = Card(
                card_row.Card,
                cls.dic[card_row.Role],
                cls.dic[card_row.Element],
                card_row.ManaCost,
                card_row.Dmg,
                cls.dic[card_row.AttackType],
                card_row.Speed,
                card_row.Health,
                card_row.Armor,
                cls.retrieve_ability_list(card_row),
            )
            return inst
        except KeyError as e:
            print("Spreadsheet item is blank or invalid")
            raise e

    @classmethod
    def card(cls, i):
        if type(i) is int:
            return cls.card_from_row(cls.df.iloc[i])
        if type(i) is str:
            for j in range(len(cls.df)):
                if cls.df.Card[j] == i:
                    return cls.card_from_row(cls.df.iloc[j])
            raise KeyError(f"{i} not found in any card name")

    @classmethod
    def collect(cls, card_names):
        card_names_set = set(card_names)
        unsorted_deck = {}
        for i in range(len(cls.df)):
            name = cls.df.Card[i]
            if name in card_names_set:
                unsorted_deck[name] = cls.card(i)

        deck = []
        for name in card_names:
            deck.append(unsorted_deck[name])
        return deck

    @classmethod
    def get_home_visitor(cls):
        length = 16
        home = [cls.card(x) for x in range(length // 2)]
        visitor = [cls.card(x) for x in range(length // 2, length)]
        return home, visitor