import random
from enum import Enum

from enums import AttackType
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
        self.max_health = health
        self.health = health
        self.armor = armor
        self.abilities = set(abilities)
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

    def get_pos(self, allies) -> int:
        count = 0
        for card in allies:
            if card.health > 0:
                count += 1
            if id(card) == id(self):
                return count

    def can_attack(self, allies):
        if self.attack_type == AttackType.MAGIC:
            return True

        if self.attack_type == AttackType.NONE:
            return False

        pos = self.get_pos(allies)
        if self.attack_type == AttackType.MELEE:
            if 'sneak' in self.abilities or 'opportunity' in self.abilities:  # todo: make this future proof
                return True

            if pos == 2 and 'reach' in self.abilities:
                return True

            return pos == 1

        if self.attack_type == AttackType.RANGED:
            return pos != 1

        raise ValueError(f"{self} has attack type {self.attack_type}")

    def calc_evade_chance(self, card):
        # requires other card for speed, blind, etc
        if card.attack_type == AttackType.MAGIC:
            return 0
        evade_chance = 0
        speed_diff = self.speed - card.speed
        if speed_diff > 0:
            evade_chance += 0.1*speed_diff
        if 'flying' in self.abilities and 'flying' not in card.abilities:
            evade_chance += 0.25
        if 'dodge' in self.abilities:
            evade_chance += 0.25
        # todo: make some way to add the blind buff +15% evade
        return evade_chance

    def take_damage_from(self, card, verbose=False)->bool:  # also heals if has heal buff
        if card.health < card.max_health and 'heal' in card.abilities:
            card.health = min(card.health+2, card.max_health)

        if verbose:
            print(f"{card} --[[attacks]]-- {self}")
        if random.random() < self.calc_evade_chance(card):
            if verbose:
                print(f"{self.name} --[[evades the attack]]--")
                print()
            return False

        self.take_damage(card.dmg, card.attack_type == AttackType.MAGIC)
        if verbose:
            print(f"{self.name} --[[takes {card.dmg} damage]]--: {self}")
            print()
        return True

    def take_damage(self, amount, armor_ignored=False):
        if not armor_ignored and self.armor > 0:
            self.armor -= amount
            if self.armor < 0:
                self.armor = 0
            return

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.events.notify(EventType.ON_DEATH, self)

    def __repr__(self):
        return f"{self.name} {self.abilities} ({self.attack_type.name}) DMG:{self.dmg} ARM:{self.armor} SPD:{self.speed} HP:{self.health}"
