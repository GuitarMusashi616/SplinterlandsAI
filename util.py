import random

import pandas as pd

from enums import Role
from card_bridge import CardBridge
from card import Card


def next_card(deck1, deck2, enable_random=True):
    nominee1 = max(deck1, key=lambda x: x.speed)
    nominee2 = max(deck2, key=lambda x: x.speed)

    if nominee1.speed > nominee2.speed:
        return nominee1

    if nominee1.speed < nominee2.speed:
        return nominee2

    if nominee1.attack_type.value < nominee2.attack_type.value:
        # larger attack type goes first
        return nominee2

    if nominee1.attack_type.value > nominee2.attack_type.value:
        return nominee1

    if enable_random and random.random() < 0.5:
        return nominee2

    return nominee1


def get_battle_order(home, visitor):
    result = []
    while home and visitor:
        card = next_card(home, visitor, False)
        try:
            home.remove(card)
        except ValueError:
            visitor.remove(card)

        result.append(card.name)
    return result


def mons_stats(cards):
    ls = []
    for card in cards:
        if card.role is Role.MONSTER:
            ls.append((card.dmg, card.armor, card.speed, card.health))
    return ls


def mana_cost(cards):
    return sum(card.mana_cost for card in cards)


def reset_cards(cards):
    for _ in range(len(cards)):
        front = cards.pop(0)
        fresh = CardBridge.card(front.name)
        cards.append(fresh)


if __name__ == "__main__":
    pd.read_excel("cards.xlsx")