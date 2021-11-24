from unittest import TestCase

from battle import Battle, Result
from battle_record import BattleRecord
from buff_registry import BuffRegistry
from card_bridge import CardBridge
from deck_proxy import DeckProxy
from test import get_alric_deck, get_pyre_deck, Element
from util import mons_stats, get_deck_combos


class BattleTesting(TestCase):
    def test_battle_recorder(self):
        br = BattleRecord()
        al = get_alric_deck()
        py = get_pyre_deck()

        br.save(al, py)
        self.assertEqual(br.round[0],"1032 1023 1023 1021 1031 3245 2035 1024 1012 0024 2031 1022")

    def test_instantiation_inspire_protect(self):
        home = ["Alric Stormbringer", "Frozen Soldier", "Enchanted Pixie", "Ice Pixie", "Medusa"]
        oppo = ["Mother Khala", "Clay Golem", "Silvershield Knight", "Truthspeaker"]
        home = CardBridge.collect(home)
        oppo = CardBridge.collect(oppo)

        home_bef = [(2, 5, 2, 3), (1, 0, 2, 1), (1, 0, 3, 1), (1, 0, 2, 3)]
        oppo_bef = [(3, 0, 1, 7), (1, 1, 4, 5), (0, 0, 2, 1)]
        home_aft = [(2, 5, 2, 3), (2, 0, 2, 1), (2, 0, 3, 1), (2, 0, 2, 3)]
        oppo_aft = [(4, 2, 1, 8), (2, 3, 4, 6), (0, 2, 2, 2)]

        self.assertListEqual(home_bef, mons_stats(home))
        self.assertListEqual(oppo_bef, mons_stats(oppo))
        BuffRegistry.instantiate_all(home, oppo)
        self.assertListEqual(home_aft, mons_stats(home))
        self.assertListEqual(oppo_aft, mons_stats(oppo))

    def test_void_shield_inspire_protect_battle(self):
        home = ["Alric Stormbringer", "Frozen Soldier", "Enchanted Pixie", "Ice Pixie", "Medusa"]
        oppo = ["Mother Khala", "Clay Golem", "Silvershield Knight", "Truthspeaker"]
        home = CardBridge.collect(home)
        oppo = CardBridge.collect(oppo)

        br = BattleRecord()
        Battle.begin(home, oppo, battle_record=br)

        self.assertEqual("1023 1031 1021 2523 3017 0021 1145", br.round[0])
        self.assertEqual("2023 2031 2021 2323 4015 0222 2346", br.round[1])
        self.assertEqual("2023 2031 2021 2323 2346 0222", br.round[2])
        self.assertEqual("2023 2031 2021 2223 0022", br.round[3])

    def test_taunt_reach_tank_heal_battle(self):
        home = ["Lyanna Natura", "Unicorn Mustang", "Goblin Thief", "Failed Summoner"]
        oppo = ["Mother Khala", "Shieldbearer", "Horny Toad", "Divine Healer"]
        home = CardBridge.collect(home)
        oppo = CardBridge.collect(oppo)

        br = BattleRecord()
        Battle.begin(home, oppo, verbose=True, battle_record=br)

        self.assertEqual("0024 2023 304a 2429 0014 1012", br.round[0])
        self.assertEqual("0025 2024 3049 202a 0015 1013", br.round[1])
        self.assertEqual("0025 2024 3047 2028 0015 1013", br.round[2])
        self.assertEqual("0025 2024 3045 2026 0015 1013", br.round[3])
        self.assertEqual("0025 2024 3044 2024 0015 1013", br.round[4])
        self.assertEqual("0025 2024 3041 1013 0015", br.round[5])
        self.assertEqual("0025 2024 3041 0015", br.round[6])

    def test_summoner_first_in_deck_proxy_instantiate(self):
        pyre = get_pyre_deck()
        alric = get_alric_deck()
        dpp = DeckProxy.from_cards(pyre)
        dpa = DeckProxy.from_cards(alric)

        self.assertEqual(dpp.instantiate()[0].name, "Pyre")
        self.assertEqual(dpa.instantiate()[0].name, "Alric Stormbringer")

    def test_elo(self):
        chosen = [
            'Pyre',
            'Giant Roc',
            'Kobold Miner',
            'Cocatrice',
            'Goblin Fireballer',
            'Goblin Shaman',
            'Fire Beetle',
        ]
        classic = DeckProxy.from_cards(get_pyre_deck())
        chosen = DeckProxy.from_string(chosen)
        old_elo = chosen.elo
        result = chosen.battle(classic)

        if result == Result.WIN:
            self.assertGreater(chosen.elo, old_elo)
        elif result == Result.DRAW:
            self.assertEqual(chosen.elo, old_elo)
        else:
            self.assertLess(chosen.elo, old_elo)


    def test_tourney(self):
        pass


if __name__ == "__main__":
    mana_cost = 16
    elements_to_search = [Element.FIRE, Element.WATER, Element.EARTH, Element.LIFE, Element.DEATH]
    group_sizes_to_search = range(1, 7)
    df_cards = []
    for i in group_sizes_to_search:
        for elem in elements_to_search:
            df_cards += get_deck_combos(elem, mana_cost - 3, 0, group_size=i)

    print(len(df_cards))
    decks = [DeckProxy(x) for x in df_cards]
    decks.sort(reverse=True)
    print(decks)