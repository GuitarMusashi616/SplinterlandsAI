from test import get_alric_deck, get_pyre_deck, Role
from util import mons_stats


class BattleRecord:
    def __init__(self):
        self.round = []

    @staticmethod
    def hex(num):
        return hex(num)[2:]

    def get_back_line(self, cards):
        ls = []
        for card in cards:
            if card.health > 0:
                string = f"{self.hex(card.dmg)}{self.hex(card.armor)}{self.hex(card.speed)}{self.hex(card.health)} "
                ls.append(string)
        return ls

    def stringify_top(self, cards):
        ls = self.get_back_line(cards)

        if ls:
            item = ls.pop(0)
            ls.append(item)
        return "".join(ls)

    def stringify_bottom(self, cards):
        ls = self.get_back_line(cards[::-1])

        if ls:
            item = ls.pop()
            ls.insert(0, item)
        return "".join(ls)

    def save(self, home, oppo):
        assert home[0].role == Role.SUMMONER and oppo[0].role == Role.SUMMONER, f"home and oppo must have summoner in 1st slot:\n{home}\n{oppo}"
        string = self.stringify_top(home) + self.stringify_bottom(oppo)
        self.round.append(string.strip())

