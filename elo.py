class Elo:
    @staticmethod
    def prob_A_wins(ratingA, ratingB):
        return 1 / (1 + 10 ** ((ratingB - ratingA) / 400))

    @staticmethod
    def new_rating(rating, score, expected_score):
        return rating + 32 * (score - expected_score)

    @classmethod
    def battle(cls, p1, p2, p1_score):
        assert 0 <= p1_score <= 1
        prob_p1_wins = cls.prob_A_wins(p1, p2)
        # print(f"p1 has {round(prob_p1_wins * 100)}% chance of winning")
        p1 = cls.new_rating(p1, p1_score, prob_p1_wins)
        p2 = cls.new_rating(p2, 1 - p1_score, 1 - prob_p1_wins)
        return p1, p2

    @classmethod
    def assertEqual(cls, left, right):
        assert left == right, f"{left} != {right}"

    @classmethod
    def test(cls):
        p1, p2 = 1656, 1763
        p1, p2 = cls.battle(p1, p2, 1)
        cls.assertEqual((p1, p2), (1676.777438307551, 1742.222561692449))


if __name__ == "__main__":
    Elo.test()