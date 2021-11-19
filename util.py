from enum import Enum


class AttackType(Enum):
    NONE = 1
    MELEE = 2
    RANGED = 3
    MAGIC = 4


class Role(Enum):
    SUMMONER = 1
    MONSTER = 2


class Element(Enum):
    FIRE = 1
    WATER = 2
    EARTH = 3
    LIFE = 4
    DEATH = 5
    DRAGON = 6
    NEUTRAL = 7
