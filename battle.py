class Battle:
    def __init__(self, p1cards, p2cards):
        self.p1cards = p1cards
        self.p2cards = p2cards

    @classmethod
    def attack_order(cls):
        i = 0
        while i < 100:
            i += 1
            yield i

    def apply_buffs(self):
        for card in self.p1cards:
            pass

