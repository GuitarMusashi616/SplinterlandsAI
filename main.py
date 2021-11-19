import random

import pandas as pd


def next_card(deck1, deck2):
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

    if random.random() < 0.5:
        return nominee1

    return nominee2


if __name__ == "__main__":
    pd.read_excel("cards.xlsx")