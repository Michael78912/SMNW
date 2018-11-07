"""a file for representing an attack."""

class Attack:
    def __init__(self, damage, cooldown):
        self.damage = damage
        self.cooldown = cooldown

    def __repr__(self):
    	return "{}(damage={}, cooldown={})".format(self.__class__.__name__, self.damage, self.cooldown)
