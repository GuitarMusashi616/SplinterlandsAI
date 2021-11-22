import math
import random


class BattleOrder:
    def __init__(self, p1cards, p2cards):
        self.p1cards = p1cards
        self.p2cards = p2cards
        self.speed = math.inf
        self.sorted_cards = sorted(self.p1cards + self.p2cards,
                                key=lambda x: (x.speed, x.attack_type.value, random.random()), reverse=True)

    def __iter__(self):
        self.all_cards = self.sorted_cards.copy()
        return self

    def __next__(self):
        if not self.all_cards:
            raise StopIteration

        candidate = self.all_cards.pop(0)
        while candidate.health < 1 or candidate.dmg < 1:  # if card is dead, a summoner, or does no dmg, skip
            if not self.all_cards:
                raise StopIteration
            candidate = self.all_cards.pop(0)

        return candidate


        # run through both lists for highest speed
        # return highest of the two candidates (speed then magic, ranged, melee then chance)