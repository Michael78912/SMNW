"""enemies.py- contains enemies that are used in SMNW.
may create a seperate library for these one day, but until I
decide to use something other than Blob and Stationary, I'll be fine.
"""


import random

from .enemy import Enemy

__all__ = ['Blob', 'Stationary']

GRAY = (220, 220, 220)

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
    _damaging = -1
    fell_on_last = 0
    on_screen = False
    intelligence = 4

    def __init__(self, colour, head, drops, drop_rates, attack, health, range, size):
        super().__init__()

        self.colour = colour
        self.health = health
        self.range = range
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

    # def hit(self, attack):
    #     super().hit(attack)
    #     dmg = self.damage_font.render(str(self.health), False, GRAY)
    #     rect = dmg.get_rect()
    #     rect.center = self.pos[0] + self.size_px // 2, self.pos[1] - 10
    #     pg.display.get_surface().blit(dmg, rect)

    def __repr__(self):
        return "Blob enemy type " + str(self._num)

    def draw(self, coordinates, surface, colour=None):
        """draws enemy to screen at coordinates.
        using cartesian system.
        """
        if self.dead:
            return
        self.on_screen = True
        surface.blit(self.head.get_image(colour), coordinates)
        self.pos = coordinates

    def move(self, all_players, surface, terrain_obj):
        """attempt to move the blob.. If it can't move,
        then don't move!
        """

        if random.randint(1, self.chance_of_motion) != 1:
            return

        # foot pos is where they are actually standing.
        foot_pos = self.pos[0], self.pos[1] + self.size_px
        pos_blocks = terrain_obj.px_pos_to_blocks(foot_pos)

        # we can use this column later to check if they are
        # up against a wall or something
        column = terrain_obj.grid[:,
                                  pos_blocks[0]
                                  ]

        # the block we are currently standing on
        current_block = terrain_obj[pos_blocks]

        # fall the amount. (0.5 water. 0 solid block, 2 air)
        self.pos = self.pos[0], self.pos[1] + current_block.solid

        current_x = self.pos[0]

        # search all players
        possible_destinations = [player.image.topright[0]
                                 for player in all_players]

        # search all destinations and pull the distance from self
        distances = [current_x - i if i <=
                     current_x else i - current_x for i in possible_destinations]

        # choose smallest distance to move to
        dest = possible_destinations[distances.index(min(distances))]

        # use self.intelligence to see if we move the proper direction or not
        move_proper = random.randint(1, self.intelligence) != 1

        # we want to move right if the destination is to the right
        move_right = dest >= current_x

        if move_right:
            # we *want* to move right
            # sorry for these lame comments, this logical stuff confuses me
            move_right = move_right and move_proper

        else:
            move_right = move_right and not move_proper

        if move_right:
            column = terrain_obj.grid[:,
                                      pos_blocks[0] + 1
                                      ]
        else:
            column = terrain_obj.grid[:,
                                      pos_blocks[0] + 1
                                      ]

        if column[int(pos_blocks[1]) - 1].solid == 0:
            # solid block, can not move.
            return

        self.pos = (
            self.pos[0] + 1 if move_right else self.pos[0] - 1), self.pos[1]

        self.draw(self.pos, surface)


class Stationary(Blob):
    """similar to blob, but does n ot move."""
    def move(self, _, surface, terrain):
        block = terrain[
            terrain.px_pos_to_blocks(
                self.pos
            )
        ]
        self.pos = self.pos[0], self.pos[1] + block.solid
