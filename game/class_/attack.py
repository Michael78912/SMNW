"""a file for representing an attack."""

class Attack:
    def __init__(self, damage, cooldown):
        self.damage = damage
        self.cooldown = cooldown

    def __repr__(self):
    	return "{}(damage={}, cooldown={})".format(self.__class__.__name__, self.damage, self.cooldown)
    
    def attack(self, pt1, pt2, game_state): pass


class MeleeAttack(Attack):
    """attack that is not ranged."""
    def attack(self, _, target, _2):
        """attack the enemey"""
        target.hit(self)

class RangedAttack(Attack):
    def __init__(self, damage, cooldown, projectile):
        super().__init__(damage, cooldown)
        self.projectile = projectile
    
    def attack(self, pt1, pt2, game_state):
        self.projectile.start(pt1, pt2.pos)
        game_state['PROJECTILES'].append(self.projectile)