import random
from itertools import combinations, product
from typing import List, Tuple, Iterable, Union

import pandas as pd

from enums import Role, Element
from card_bridge import CardBridge
from card import Card

class HighScore:
    def __init__(self):
        self.highest_score = 0
        self.highest_object = None

    def update_score(self, score, obj=None, verbose=False):
        if score > self.highest_score:
            self.highest_score = score
            if verbose:
                print(f"NEW HIGH SCORE {score}")


# def next_card(deck1: List[Card], deck2: List[Card], enable_random=True) -> Card:
#     nominee1 = max(deck1, key=lambda x: x.speed)
#     nominee2 = max(deck2, key=lambda x: x.speed)
#
#     if nominee1.speed > nominee2.speed:
#         return nominee1
#
#     if nominee1.speed < nominee2.speed:
#         return nominee2
#
#     if nominee1.attack_type.value < nominee2.attack_type.value:
#         # larger attack type goes first
#         return nominee2
#
#     if nominee1.attack_type.value > nominee2.attack_type.value:
#         return nominee1
#
#     if enable_random and random.random() < 0.5:
#         return nominee2
#
#     return nominee1


# def get_battle_order(home: List[Card], visitor: List[Card], enable_random=True) -> List[Card]:
#     result = []
#     while home and visitor:
#         card = next_card(home, visitor, enable_random)
#         try:
#             home.remove(card)
#         except ValueError:
#             visitor.remove(card)
#
#         result.append(card)
#     return result


def mons_stats(cards: List[Card]) -> List[Tuple[int, int, int, int]]:
    ls = []
    for card in cards:
        if card.role is Role.MONSTER:
            ls.append((card.dmg, card.armor, card.speed, card.health))
    return ls


def mana_cost(cards: Iterable[Card]) -> int:
    return sum(card.mana_cost for card in cards)


def reset_cards(cards: List[Card]):
    for _ in range(len(cards)):
        front = cards.pop(0)
        fresh = CardBridge.card(front.name)
        cards.append(fresh)


def decks_each_have_an_alive_card(home: List[Card], visitor: List[Card]) -> bool:
    return any(card.health > 0 for card in home) and any(card.health > 0 for card in visitor)


def card_inst_in_deck(card: Card, deck: List[Card]):
    return any(map(lambda x: id(card) == id(x), deck))


def get_allies_enemies(card: Card, deck1: List[Card], deck2: List[Card]) -> Tuple[List[Card], List[Card]]:
    in_deck1 = card_inst_in_deck(card, deck1)
    in_deck2 = card_inst_in_deck(card, deck2)

    if in_deck1 and not in_deck2:
        return deck1, deck2
    elif in_deck2 and not in_deck1:
        return deck2, deck1
    else:
        raise ValueError(f"{card} does not appear exclusively in deck1 or deck2\ndeck1:{deck1}\ndeck2:{deck2}\n")


def get_monster_pos(ally: Card, allies: List[Card]) -> int:
    count = 0
    for card in allies:
        if card.health > 0:
            count += 1
        if id(card) == id(ally):
            return count


def reposition(cards):
    front = sorted([x for x in cards if x.attack_type.value == 2], key=lambda x: x.health, reverse=True)
    back = sorted([x for x in cards if x.attack_type.value != 2], key=lambda x: x.health)
    return front + back


# class ComboGen:
#     def __init__(self, df, group_sizes):
#         self.df = df
#         self.group_size = group_sizes
#
#     def __iter__(self):
#         self.i = 0
#         self.gens = [combinations(self.df.itertuples(), i) for i in self.group_sizes]
#
#     def __next__(self):
#         while not self.gens[self.i]:
#             self.i += 1
#             if self.i >= len(self.gens):
#                 raise StopIteration








def generate_combos_of(df, group_sizes: range):
    """eg range(4,6) -> yields combos of 4 followed by combos of 5"""
    for i in group_sizes:
        gen = combinations(df.itertuples(), i)
        return next(gen)


def get_df_cards_of(element):
    df = CardBridge.df

    df_monsters = df[(df.Role == 'monster') & ((df.Element == element) | (df.Element == 'neutral'))]
    df_summoners = df[(df.Role == 'summoner') & ((df.Element == element) | (df.Element == 'neutral'))]
    return df_monsters, df_summoners


def filter_mana_cost(choices: Iterable, max_mana: int = 30, mana_within=3):
    return list(filter(lambda deck: max_mana-mana_within < sum(map(lambda card: card.ManaCost, deck)) < max_mana, choices))


def get_deck_combos(element: Element, max_mana: int, mana_within=3):
    element = element.name.lower()
    df_monsters, df_summoners = get_df_cards_of(element)
    choices = combinations(df_monsters.itertuples(), 6)
    mana_constrained = filter_mana_cost(choices, max_mana, mana_within)
    full_decks = product(df_summoners.itertuples(), mana_constrained)
    full_decks_recombined = list(map(lambda x: [x[0]] + list(x[1]), full_decks))
    return full_decks_recombined


if __name__ == "__main__":
    pd.read_excel("cards.xlsx")
