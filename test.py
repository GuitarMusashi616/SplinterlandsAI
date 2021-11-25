import math
from itertools import combinations
from typing import List
from unittest import TestCase, main

from battle import Battle, Result
from battle_order import BattleOrder
from buff import MeleeBuff, HealthBuff
from buff_factory import BuffFactory
from buff_registry import BuffRegistry
from card import Card
from card_bridge import CardBridge
from deck import Deck
from deck_proxy import DeckProxy
from target_registry import TargetRegistry
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


def get_lyanna_deck():
    card_names = [
        "Lyanna Natura",
        "Goblin Sorcerer",
        "Elven Cutthroat",
        "Goblin Thief",
        "Failed Summoner",
        "Khmer Princess",
        "Child of the Forest",
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
        random.seed(10)
        home, visitor = get_pyre_deck(), get_alric_deck()
        expected = [
            "Serpent of Eld",
            "Ice Pixie",
            "Cerberus",
            "Serpentine Spy",
            "Sabre Shark",
            "Elven Mystic",
            "Medusa",
            "Enchanted Pixie",
            "Fire Beetle",
            "Kobold Miner",
            'Goblin Shaman',
            "Goblin Fireballer",
        ]
        result = [card.name for card in BattleOrder(home, visitor)]
        self.assertListEqual(expected, result)

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

    def test_battle_order(self):
        home = get_pyre_deck()
        oppo = get_alric_deck()
        BuffRegistry.instantiate_all(home, oppo)
        prev_speed = math.inf
        for card in BattleOrder(home, oppo):
            self.assertGreaterEqual(prev_speed, card.speed)
            self.assertGreater(card.health, 0)
            prev_speed = card.speed

    def test_targets(self):
        # todo: card targets enemy (snipe, opportunity, sneak)
        # todo: check card order (make sure summoner-monster-monster-...)
        # todo: mock random for testing (make it play out like actual recorded battle)
        home = get_pyre_deck()
        oppo = get_alric_deck()
        enemy = TargetRegistry.choose_for(home[0], home, oppo)  # melee tank targets first
        self.assertEqual(enemy.name, 'Serpent of Eld')

        enemy = TargetRegistry.choose_for(home[2], home, oppo)  # sneak hits last target
        self.assertEqual(enemy.name, 'Sabre Shark')

        enemy = TargetRegistry.choose_for(home[3], home, oppo)  # oppo hits weakest
        self.assertIn(enemy.name, {'Ice Pixie', 'Enchanted Pixie'})

        enemy = TargetRegistry.choose_for(home[-1], home, oppo)  # sneak hits last target
        self.assertEqual(enemy.name, 'Ice Pixie')

    def test_actual_battle_from_replay(self):
        # pick = random.randint(1, 10000000) # 7074366
        score = 0
        random.seed(50067)
        order = [
            ('Child of the Forest', 'Goblin Shaman', True),
            ('Cerberus', 'Goblin Sorcerer', True),
            ('Serpentine Spy', 'Elven Cutthroat', True),
            ('Fire Beetle', 'Failed Summoner', True),
            ('Kobold Miner', 'Child of the Forest', True),
            ('Goblin Fireballer', 'Goblin Thief', True),
            ('Goblin Thief', 'Cerberus', True),
            ('Khmer Princess', 'Cerberus', True),
            ('Child of the Forest', 'Goblin Shaman', True),
            ('Cerberus', 'Goblin Thief', True),
            ('Serpentine Spy', 'Child of the Forest', True),
            ('Fire Beetle', 'Khmer Princess', True),
            ('Kobold Miner', 'Khmer Princess', True),
            ('Goblin Fireballer', 'Failed Summoner', True),
            ('Cerberus', 'Failed Summoner', True),
        ]

        home = get_pyre_deck()
        oppo = get_lyanna_deck()

        home_bef = [(2, 0, 3, 5), (1, 0, 2, 2), (2, 0, 3, 1), (0, 0, 2, 4), (1, 0, 1, 2), (1, 0, 2, 4)]
        home_aft = [(2, 0, 4, 5), (1, 0, 3, 2), (2, 0, 4, 1), (0, 0, 3, 4), (1, 0, 2, 2), (1, 0, 3, 4)]
        oppo_bef = [(1, 0, 2, 2), (1, 0, 3, 1), (2, 0, 2, 3), (0, 0, 2, 4), (1, 0, 1, 2), (1, 0, 5, 2)]
        oppo_aft = [(1, 0, 2, 2), (1, 0, 3, 1), (2, 0, 2, 3), (0, 0, 2, 4), (1, 0, 1, 2), (1, 0, 5, 2)]

        self.assertListEqual(home_bef, mons_stats(home))
        self.assertListEqual(oppo_bef, mons_stats(oppo))
        BuffRegistry.instantiate_all(home, oppo)
        battle_order = BattleOrder(home, oppo)
        self.assertListEqual(home_aft, mons_stats(home))
        self.assertListEqual(oppo_aft, mons_stats(oppo))

        while decks_each_have_an_alive_card(home, oppo):
            for card in battle_order:
                allies, enemies = get_allies_enemies(card, home, oppo)
                enemy = TargetRegistry.choose_for(card, allies, enemies)

                if not enemy:
                    break

                if not card.can_attack(allies):
                    continue

                got_hit = enemy.take_damage_from(card)
                attacker, defender, was_hit = order.pop(0)
                if attacker == card.name:
                    score += 1
                if defender == enemy.name:
                    score += 1
                if was_hit == got_hit:
                    score += 1
                self.assertFalse(attacker != card.name or defender != enemy.name or was_hit != got_hit)

        self.assertEqual(45, score)

    def test_battle_class(self):
        home_won = Battle.begin(get_pyre_deck(), get_lyanna_deck())
        self.assertTrue(home_won)

    def test_deck_class_sort(self):
        home = Deck(get_alric_deck())
        oppo = Deck(get_pyre_deck())
        visitor = Deck(get_lyanna_deck())

        comp = [oppo, home, visitor]
        comp.sort()
        self.assertEqual(id(comp[0]), id(visitor))
        self.assertEqual(id(comp[1]), id(oppo))
        self.assertEqual(id(comp[2]), id(home))

    def test_sort_deck_list(self):
        limit = 20
        element = 'fire'
        # full_viable = self.sort_by_best(element, limit, limit < 20)
        # full_viable.sort()
        # print(full_viable)

    # def test_gen_combos(self):
    #     df_monsters, _ = get_df_cards_of('fire')
    #     choices = generate_combos_of(df_monsters)
    #
    #     choices = [len(x) for x in choices]
    #
    #     self.assertEqual(choices[0], 4)
    #     self.assertEqual(choices[-1], 6)

    @staticmethod
    def faster_search():
        decks = get_deck_combos(Element.EARTH, 28)
        deck_proxies = [DeckProxy(x) for x in decks]
        prev_best = random.choice(deck_proxies)
        for i, deck in enumerate(deck_proxies):
            results = {Result.WIN: 0, Result.DRAW:0, Result.LOSE: 0}
            while True:
                results[deck.battle(prev_best)] += 1
                if results[Result.WIN] >= 5:
                    prev_best = deck
                    print(f"NEW HIGH SCORE {i}:")
                    print(deck)
                    break
                elif results[Result.LOSE] >= 5:
                    break

    @staticmethod
    def elo_search():
        decks = [DeckProxy(x) for x in get_deck_combos(Element.FIRE, 28, 3)]
        weights = [x.elo for x in decks]
        best_deck = decks[0]
        for _ in range(10000):
            deck1, deck2 = random.choices(decks, k=2, weights=weights)
            deck1.battle(deck2)
            if deck1.elo > best_deck.elo:
                best_deck = deck1
                print(best_deck)
            if deck2.elo > best_deck.elo:
                best_deck = deck2
                print(best_deck)

        decks.sort(key=lambda x:x.elo, reverse=True)
        for deck in decks:
            print(deck)




    @classmethod
    def find_best_in_element(self):
        limit = 30
        element = 'fire'
        tournament_size = 5
        full_viable = self.sort_by_best(element, limit, limit < 20)

        prev_best = random.choice(full_viable)
        for i, deck in enumerate(full_viable):
            if deck < prev_best and deck < prev_best and deck < prev_best:
                prev_best = deck
                # prev_best.pop(0)
                # prev_best.append(deck)
                print(f"NEW HIGH SCORE deck #{i}:")
                print(deck)

        print(prev_best)

    @classmethod
    def sort_by_best(self, element, limit=20, extended_search=False, summ_cost=3):
        options = [CardBridge.card(i) for i in CardBridge.df[CardBridge.df.Element == element].index]
        options.extend(CardBridge.card(i) for i in CardBridge.df[CardBridge.df.Element == 'neutral'].index)
        monsters = [x for x in options if x.role == Role.MONSTER]
        summs = [x for x in options if x.role == Role.SUMMONER]
        combos = list(combinations(monsters, 6))
        if extended_search:
            for i in range(4,6):
                combos.extend(list(combinations(monsters, i)))

        viable = [x for x in combos if mana_cost(x) < limit-summ_cost]
        full_viable = []
        for summ in summs:
            for cards in viable:
                cards = reposition(cards)
                cards = [summ] + list(cards)
                full_viable.append(Deck(cards))
        return full_viable


if __name__ == '__main__':
    MyTestCase.faster_search()
