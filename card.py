import random
from enum import Enum

from events import EventManager, EventType


class Card:
    def __init__(self, name, role, element, mana_cost, dmg, attack_type, speed, health, armor, abilities):
        self.name = name
        self.role = role
        self.element = element
        self.mana_cost = mana_cost
        self.dmg = dmg
        self.attack_type = attack_type
        self.speed = speed
        self.health = health
        self.armor = armor
        self.abilities = abilities
        self._events = EventManager()

    @property
    def events(self):
        return self._events

    def __eq__(self, other):
        assert isinstance(other, self.__class__), "Can only compare cards of same class"
        for s_key, s_val in self.__dict__.items():
            if not isinstance(s_val, EventManager):
                if s_val != other.__dict__[s_key]:
                    return False
        return True

    def calc_evade_chance(self, card):
        # requires other card for speed, blind, etc
        return 0.1 * self.speed

    def take_damage_from(self, card):
        if random.random() < self.calc_evade_chance(card):
            return

        self.take_damage(card.dmg)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.events.notify(EventType.ON_DEATH, self)

    def __repr__(self):
        return f"{self.name} {self.abilities} DMG:{self.dmg} ({self.attack_type.name}) HP:{self.health} ARM:{self.armor} SPD:{self.speed} "
