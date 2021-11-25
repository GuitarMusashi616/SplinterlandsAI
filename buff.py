from abc import ABC, abstractmethod

from card import Card
from events import EventListener, EventType
from enums import AttackType, Role


class Buff(ABC):
    @abstractmethod
    def apply(self):
        ...

    @abstractmethod
    def remove(self):
        ...


class BuffExpiresOnDeath(Buff, EventListener):
    """Either check when its alive (functional) or be notified when it's dead?"""

    def __init__(self, delta: int, card: Card, rem_on_death: Card):
        self.delta = delta
        self.card = card
        self.has_been_applied = False  # used to store prev stat val before buff
        self.apply()
        rem_on_death.events.subscribe(EventType.ON_DEATH, self)

    def update(self, data: Card):
        self.remove()

    @abstractmethod
    def apply(self):
        ...

    @abstractmethod
    def remove(self):
        ...


class StatBuff(BuffExpiresOnDeath, EventListener):
    """Can be positive or negative"""

    @abstractmethod
    def should_apply(self) -> bool:
        ...

    @abstractmethod
    def card_attrib_to_modify(self) -> str:
        ...

    @classmethod
    def attrib_min_val(cls) -> int:
        return 1

    def apply(self):
        self.change_attrib(self.card_attrib_to_modify(), self.delta)

    def remove(self):
        self.change_attrib(self.card_attrib_to_modify(), self.delta)

    def change_attrib(self, key, amount):
        if self.card.role is Role.MONSTER and self.should_apply():
            min_val = self.attrib_min_val()
            if self.delta < 0 and self.card.__dict__[key] <= min_val:
                #  dont make the health go down if its already at <= 1, will kill cards instead of debuffing them
                return
            self.card.__dict__[key] += amount
            self.has_been_applied = True

    def remove_attrib(self, key, amount):
        if self.has_been_applied:
            self.card.__dict__[key] -= amount
            self.has_been_applied = False


class AttackBuff(StatBuff):
    def card_attrib_to_modify(self):
        return "dmg"

    @abstractmethod
    def should_apply(self) -> bool:
        ...


class FlatBuff(StatBuff):

    def card_attrib_to_modify(self) -> str:
        ...

    def should_apply(self) -> bool:
        return True


class MeleeBuff(AttackBuff):
    def should_apply(self):
        return self.card.attack_type is AttackType.MELEE


class RangedBuff(AttackBuff):
    def should_apply(self):
        return self.card.attack_type is AttackType.RANGED


class MagicBuff(AttackBuff):
    def should_apply(self):
        return self.card.attack_type is AttackType.MAGIC


class HealthBuff(FlatBuff):
    def apply(self):
        self.change_attrib('health', self.delta)
        self.change_attrib('max_health', self.delta)

    def remove(self):
        self.change_attrib('health', self.delta)
        self.change_attrib('max_health', self.delta)


class ArmorBuff(FlatBuff):
    def card_attrib_to_modify(self) -> str:
        return 'armor'

    # @classmethod
    # def attrib_min_val(cls) -> int:
    #     # uncomment if armor- debuff makes 1 armor go to 0 armor
    #     return 0


class SpeedBuff(FlatBuff):
    def card_attrib_to_modify(self) -> str:
        return 'speed'
