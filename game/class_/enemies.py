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
    body = None
    on_screen = False
    intellegince = 4

    def __init__(self, stats, colour, head, drops, drop_rates, attack):
        base.Enemy.__init__(self, stats, colour)
        self.head = head
        # name is used by the game itself.
        self.name = head.name + '_blob'
        # pretty_name is the name that appears in the library
        self.pretty_name = head.pretty_name + ' Blob'
        self.drops = drops
        self.drop_rates = drop_rates
        self.attack = attack

    def draw(self, coordinates, surface):
        """draws enemy to screen at coordinates. 
                using cartesian system.
                """
        copy = surface.copy()
        self.on_screen = True
        surface.blit(self.head, coordinates)
        self.pos = coordinates

    def move(self, all_players, surface):
        """moves the enemy towards the closest player to it.
                the Blob does not move too much, and has a 1/4 (intelligence) 
                chance of moving the way away from the players.
                """

        possible_destinations = [player[0] for player in all_players]
        motion = BACKWARDS if random.randint(1, 4) == 1 else FORWARDS
        possible_destinations = [
            abs(self.pos[1] - destination)
            for destination in possible_destinations
        ]
        destination = min(possible_destinations)
        destination_player = all_players[possible_destinations.index(
            destination)]

        if motion == BACKWARDS:
            self.pos = (self.pos[0], self.pos[1] - 1)
            self.draw(self.pos, surface)

        else:
            self.pos = (self.pos[0], self.pos[1] + 1)
            self.draw(self.pos, surface)
