import random
from typing import List, Tuple

import pandas as pd

from enums import Role
from card_bridge import CardBridge
from card import Card


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


def mana_cost(cards: List[Card]) -> int:
    return sum(card.mana_cost for card in cards)

def reset_cards(cards: List[Card]):
    for _ in range(len(cards)):
        front = cards.pop(0)
        fresh = CardBridge.card(front.name)
        cards.append(fresh)


def determine_winner(home, oppo):
    home_alive = any(card.health > 0 for card in home)
    oppo_alive = any(card.health > 0 for card in oppo)
    if home_alive and not oppo_alive:
        return "home wins"
    elif oppo_alive and not home_alive:
        return "oppo wins"
    else:
        raise ValueError(f"Game is not finished or everyone is dead \n{home} \n{oppo}")


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


if __name__ == "__main__":
    pd.read_excel("cards.xlsx")