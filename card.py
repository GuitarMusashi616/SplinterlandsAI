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

    def __repr__(self):
        return f"{self.name} {self.abilities} DMG:{self.dmg} ({self.attack_type.name}) HP:{self.health} ARM:{self.armor} SPD:{self.speed}"