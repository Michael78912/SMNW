try:
    from enemy import Enemy
except ImportError:
    from .enemy import Enemy
import random

__all__ = ['Blob']

BACKWARDS = 'backwards'
FORWARDS = 'forwards'


class Blob(Enemy):
    """
        stats are as follows:
        (health, EXP, GOLD, SILVER)
        """
    # Blob enemy has no body
    _amount = 0
    body = None
    chance_of_motion = 3
    on_screen = False
    intelligence = 4

    def __init__(self, colour, head, drops, drop_rates, attack, size):
        super().__init__(colour)
        self._num = self._amount + 1
        self.__class__._amount += 1
        self.head = head
        self.size_px = head.size_px
        self.size = size
        # name is used by the game itself.
        self.name = head.name + '_blob'
        # pretty_name is the name that appears in the library
        self.pretty_name = head.pretty_name + ' Blob'
        self.drops = drops
        self.drop_rates = drop_rates
        self.attack = attack


    def __repr__(self):
        return "Blob enemy type " + str(self._num)

    def copy(self):
        """return a new instance of Blob exactly equivalent to self."""
        new = self.__class__(self.colour, self.head, self.drop_rates, self.attack, self.size)
        new.__dict__ = self.__dict__
        return new

    def draw(self, coordinates, surface):
        """draws enemy to screen at coordinates. 
        using cartesian system.
        """
        self.on_screen = True
        surface.blit(self.head.get_image(), coordinates)
        self.pos = coordinates

    def move(self, all_players, surface):
        """moves the enemy towards the closest player to it.
        the Blob does not move too much, and has a 1/4 (intelligence) 
        chance of moving the way away from the players.
        """
        if random.randint(1, self.chance_of_motion) == 1:
            print('moving', self)
            current_x = self.pos[0]

            possible_destinations = [player.image.topright[0] for player in all_players]

            distances = []
            for i in possible_destinations:
                distances.append(current_x - i if i <= current_x else i - current_x)

            distance = min(distances)

            dest = possible_destinations[distances.index(distance)]

            move_proper = random.randint(1, self.intelligence) == 1


            if dest >= current_x:
                # greater. want to move to the right.
                if move_proper:
                    self.pos = (self.pos[0] - 1, self.pos[1])
                else:
                    self.pos = (self.pos[0] + 1, self.pos[1])

                

            else:
                # smaller. want to move to left.
                if move_proper:
                    self.pos = (self.pos[0] + 1, self.pos[1])
                else:
                    self.pos = (self.pos[0] - 1, self.pos[1])

