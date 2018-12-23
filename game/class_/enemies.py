"""enemies.py- contains enemies that are used in SMNW.
may create a seperate library for these one day, but until I
decide to use something other than Blob and Stationary, I'll be fine.
"""


import random
import contextlib


from .enemy import Enemy
from . import terrain


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
        self.on_screen = True
        surface.blit(self.head.get_image(colour), coordinates)
        self.pos = coordinates

    def move(self, all_players, surface, terrain_obj):
        """attempt to move the blob.. If it can't move,
        then don't move!
        """
        if random.randint(1, self.chance_of_motion) != 1:
            return

        block = terrain_obj.get_array()[:,
                                        terrain_obj.px_to_blocks(self.pos[0])

                                        ][terrain_obj.px_to_blocks(self.pos[1] + (self.size_px - 1))]

        if terrain_obj.is_solid(block):
            return

        current_x = self.pos[0]

        possible_destinations = [player.image.topright[0]
                                 for player in all_players]

        distances = []
        for i in possible_destinations:
            distances.append(current_x - i if i <=
                             current_x else i - current_x)

        distance = min(distances)
        dest = possible_destinations[distances.index(distance)]
        move_proper = random.randint(1, self.intelligence) == 1
        move_right = dest >= current_x
        if move_right:
            # we *want* to move right
            # sorry for these lame comments, this logical stuff confuses me
            move_right = move_right and move_proper

        else:
            move_right = move_right and not move_proper

        blocks_y = terrain_obj.px_to_blocks(self.pos[1])
        if move_right:
            column = terrain_obj.get_array()[:, terrain_obj.px_to_blocks(
                current_x) + 1]
            if terrain_obj.is_solid(column[blocks_y - 1]):
                # solid to the top right of our precious little
                # enemy! Uh oh. It can't move.
                return
            self.pos = (self.pos[0] + 1, self.pos[1])
        else:
            column = terrain_obj.get_array()[:, terrain_obj.px_to_blocks(
                current_x) + 1]
            if terrain_obj.is_solid(column[blocks_y - 1]):
                return
            self.pos = (self.pos[0] - 1, self.pos[1])

    def move_old(self, all_players, surface, terrain_obj):
        # pylint: disable=too-many-locals
        """moves the enemy towards the closest player to it.
        the Blob does not move too much, and has a 1/4 (intelligence)
        chance of moving the way away from the players.
        """
        if random.randint(1, self.chance_of_motion) == 1:
            # innocent until proven guilty. (of being in a pit)
            can_move = True

            in_air = terrain.is_in_air(self.pos, terrain_obj, self.size * 10)
            print(in_air)

            current_block_x = terrain_obj.px_to_blocks(self.pos[0])
            current_block_y = terrain_obj.px_to_blocks(self.pos[1])

            right_column = list(terrain_obj.terrain2dlist_texts[terrain_obj.template]
                                ['text'][:, current_block_x + 1])

            left_column = list(terrain_obj.terrain2dlist_texts[terrain_obj.template]
                               ['text'][:, current_block_x - 1])

            top_levels = {i if obj == '*' else None for i,
                          obj in enumerate(right_column)}
            top_levels.remove(None)

            if in_air:
                # fall two pixels, because enemy is in air
                self.fell_on_last = 1
                self.pos = self.pos[0], self.pos[1] + 2

            current_x = self.pos[0]

            possible_destinations = [player.image.topright[0]
                                     for player in all_players]

            distances = []
            for i in possible_destinations:
                distances.append(current_x - i if i <=
                                 current_x else i - current_x)

            distance = min(distances)

            dest = possible_destinations[distances.index(distance)]

            move_proper = random.randint(1, self.intelligence) == 1

            if dest >= current_x:
                # greater. want to move to the right.
                if move_proper:
                    move_right = False
                    self.pos = (self.pos[0] - 1, self.pos[1])
                else:
                    move_right = True
                    self.pos = (self.pos[0] + 1, self.pos[1])

            else:
                # smaller. want to move to left.
                if move_proper:
                    move_right = False
                    self.pos = (self.pos[0] + 1, self.pos[1])
                else:
                    move_right = True
                    self.pos = (self.pos[0] - 1, self.pos[1])

            # check to see if the enemy can't move.


class Stationary(Blob):
    """similar to blob, but does n ot move."""
    def move(*_): pass
