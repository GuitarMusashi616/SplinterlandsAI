import math
from unittest import TestCase, main

from card_bridge import CardBridge
from main import *


class MyTestCase(TestCase):
    def test_cards_ordered_by_speed(self):
        cards = [CardBridge.card(x) for x in range(10)]

        cards.sort(key=lambda x: x.speed, reverse=True)

        prev_speed = math.inf
        for card in cards:
            self.assertTrue(card.speed <= prev_speed, f"{card.speed} from {card} should be <= {prev_speed}")
            prev_speed = card.speed

    def test_no_summoner_battle_card_turns(self):
        home, visitor = CardBridge.get_home_visitor()
        expected = [
            "Spark Pixies",
            "Serpentine Soldier",
            "Fire Elemental",
            "Serpentine Spy",
            "Cerberus",
            "Goblin Shaman",
            "Giant Roc",
            "Kobold Miner",
            "Fire Beetle",
            "Kobold Bruiser",
            "Magma Troll",
        ]
        result = []

        while home and visitor:
            card = next_card(home, visitor)
            try:
                home.remove(card)
            except ValueError:
                visitor.remove(card)

            result.append(card.name)

        for i in range(len(expected)):
            self.assertEqual(result[i], expected[i])


if __name__ == '__main__':
    main()
