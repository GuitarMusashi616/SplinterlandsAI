import math
from typing import List
from unittest import TestCase, main

from battle import Battle
from buff import MeleeBuff, HealthBuff
from buff_factory import BuffFactory
from buff_registry import BuffRegistry
from card import Card
from card_bridge import CardBridge
from util import *


def get_pyre_deck():
    card_names = [
        "Pyre",
        "Cerberus",
        "Kobold Miner",
        "Serpentine Spy",
        "Goblin Shaman",
        "Goblin Fireballer",
        "Fire Beetle",
    ]
    return CardBridge.collect(card_names)


def get_alric_deck():
    card_names = [
        "Alric Stormbringer",
        "Serpent of Eld",
        "Ice Pixie",
        "Enchanted Pixie",
        "Medusa",
        "Elven Mystic",
        "Sabre Shark",
    ]
    return CardBridge.collect(card_names)


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
        result = get_battle_order(home, visitor)

        for i in range(len(expected)):
            self.assertEqual(result[i], expected[i])

    def test_collect_card_deck(self):
        card_names = [
            "Pyre",
            "Cerberus",
            "Kobold Miner",
            "Serpentine Spy",
            "Goblin Shaman",
            "Goblin Fireballer",
            "Fire Beetle",
        ]
        deck = CardBridge.collect(card_names)
        self.assertListEqual(card_names, [x.name for x in deck])

    def test_rem_buff_on_death(self):
        card = CardBridge.card(1)
        inspire_card = CardBridge.card(2)
        MeleeBuff(1, card, inspire_card)
        self.assertEqual(2, card.dmg)
        inspire_card.take_damage(5)
        self.assertEqual(1, card.dmg)
        self.assertEqual(0, inspire_card.health)

    def test_buff_factory_affect_enemies(self):
        home, visitor = CardBridge.get_home_visitor()
        shaman = next(x for x in home + visitor if x.name == "Goblin Shaman")
        weaken = BuffFactory(HealthBuff, -1, True)
        before_health = [x.health for x in visitor]

        weaken.instantiate_buff(shaman, home, visitor)
        after_health = [x.health for x in visitor]
        self.assertListEqual(after_health, [x if x <= 1 else x - 1 for x in before_health])

        shaman.take_damage(5)
        after_death_health = [x.health for x in visitor]
        self.assertListEqual(after_death_health, before_health)

    def test_apply_buffs_to_whole_team(self):
        home = get_pyre_deck()
        oppo = get_alric_deck()
        # magic buff, speed buff, health buff
        home_bef = [(2, 0, 3, 5), (1, 0, 2, 2), (2, 0, 3, 1), (0, 0, 2, 4), (1, 0, 1, 2), (1, 0, 2, 4)]
        home_aft = [(2, 0, 4, 5), (1, 0, 3, 2), (2, 0, 4, 1), (0, 0, 3, 4), (1, 0, 2, 2), (1, 0, 3, 4)]
        oppo_bef = [(3, 2, 4, 5), (1, 0, 3, 1), (1, 0, 2, 1), (1, 0, 2, 3), (1, 0, 2, 3), (1, 0, 3, 2)]
        oppo_aft = [(3, 2, 4, 4), (2, 0, 3, 1), (2, 0, 2, 1), (2, 0, 2, 2), (2, 0, 2, 2), (1, 0, 3, 1)]

        self.assertListEqual(home_bef, mons_stats(home))
        self.assertListEqual(oppo_bef, mons_stats(oppo))
        BuffRegistry.instantiate_all(home, oppo)
        self.assertListEqual(home_aft, mons_stats(home))
        self.assertListEqual(oppo_aft, mons_stats(oppo))

    def test_card_eq(self):
        card = CardBridge.card(1)
        card_diff = CardBridge.card(2)  # different card
        card_copy = CardBridge.card(1)

        self.assertNotEqual(card, card_diff)
        self.assertEqual(card, card)
        self.assertEqual(card, card_copy)
        card.health += 2
        self.assertNotEqual(card, card_copy)
        card.health -= 2
        self.assertEqual(card, card_copy)

    def test_deck_utils(self):
        # card instances cannot be reused, must use CardBridge again so save as string lists
        # or call reset on them, gets the same deck from CardBridge
        # also need a util func to count up mana cost
        home = get_pyre_deck()
        oppo = get_alric_deck()
        self.assertEqual(mana_cost(home), 20)
        self.assertEqual(mana_cost(oppo), 26)

        for card in home:
            card.armor += 4
        for card in oppo:
            card.armor += 4

        reset_cards(home)
        reset_cards(oppo)
        self.assertListEqual(home, get_pyre_deck())
        self.assertListEqual(oppo, get_alric_deck())

    def test_card_in_deck(self):
        # card in deck based on memory address (exact instance) vs same stats
        home = get_pyre_deck()
        pyre = CardBridge.card('Pyre')
        self.assertIn(home[0], home)
        self.assertIn(pyre, home)
        self.assertTrue(any(map(lambda x: id(x) == id(home[0]), home)))
        self.assertFalse(any(map(lambda x: id(x) == id(pyre), home)))

    def test_better_fighter_iter(self):
        home = get_pyre_deck()
        oppo = get_alric_deck()
        # for card, enemies in Battle.attack_order(home, oppo):  # if a monster in the queue dies make sure its removed from queue
        #     Battle.attack(card, enemies)  # if id(card) in home then attack oppo
        #     # enemy = card.choose_target(enemies) # depends on abilities
        #     # enemy.take_damage_from(card)
        #
        #
        # for card in Battle.rem_fighters(home):
        #     Battle.

    def test_choose_target(self):
        pass

    # def test_battling_already(self):
    #     home = get_pyre_deck()
    #     oppo = get_alric_deck()
    #     BuffRegistry.instantiate_all(home, oppo)  # todo: order of buffs matter eg +1 health before -1 health
    #
    #     # continue if some card in deck 1 and some card in deck 2 is alive
    #     while any(card.health > 0 for card in home) and any(card.health > 0 for card in oppo):
    #         home_fighters = [x for x in home if x.dmg > 0 and x.health > 0]
    #         oppo_fighters = [x for x in oppo if x.dmg > 0 and x.health > 0]
    #         fighter = next_card(home_fighters, oppo_fighters)
    #         try:
    #             home_fighters.remove(fighter)
    #         except ValueError:
    #             oppo_fighters.remove(fighter)


if __name__ == '__main__':
    main()
