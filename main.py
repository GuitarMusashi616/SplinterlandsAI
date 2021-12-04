import time
import sys

from deck_proxy import DeckProxy
from enums import Result
from util import get_deck_combos_of_mana_cost
from pathos.multiprocessing import Pool


def battle(d1, d2, out_q):
    if d1 > d2:
        out_q.put(d1)


def cut_half(decks):
    return [deck1 if deck1.battle(deck2) == Result.WIN else deck2 for deck1, deck2 in zip(decks[::2], decks[1::2])]


def tourney(decks):
    while len(decks) > 1:
        decks = cut_half(decks)
        print(f"{len(decks)} left for this thread")
    return decks[0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("First command line arg must be an int specifying max mana cost")
        sys.exit()

    target_mana_cost = int(sys.argv[1])
    group_sizes_to_search = range(1, 7) if target_mana_cost < 22 else range(6,7)
    within = 3 if target_mana_cost < 18 else 0

    print(f"Finding best deck that costs {target_mana_cost} mana (may take up to 20 minutes)")
    decks = [DeckProxy(x) for x in get_deck_combos_of_mana_cost(target_mana_cost, within, group_sizes_to_search=group_sizes_to_search)]
    n_splits = 8
    split_decks = [decks[i::n_splits] for i in range(n_splits)]

    print("Multiprocessor combination search started...\n")
    tic = time.time()
    results = split_decks
    with Pool() as p:
        results = p.map(tourney, results)

    toc = time.time()
    results.sort(reverse=True)
    print("Top 8 Deck Combos from Best to Worst:")
    print(results)
    print(f"{toc - tic} seconds")


