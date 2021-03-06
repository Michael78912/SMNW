import os.path
import random

import pygame as pg

from .smr_error import SMRError
from .particle import Particle
from .damagenumbers import DamageNumber


class Enemy:
    """base class for Stickman's new world enemies"""
    id = 0
    health = 0
    damage_font = pg.font.Font(os.path.join('data', 'Roboto-Regular.ttf'), 9)
    damage_numbers = []
    dead = False
    # I dont know why the hell it needs to start at -3, not 0, but it does
    _enemies = -3
    in_damage_state = False
    pos = (0, 0)

    def __init__(self, drops):
        Enemy._enemies += 1
        self.drops = drops
        self.id = self._enemies

    def hit(self, attack):
        self.health -= attack.damage
        # become red for 4 frames.
        self._damaging = 4
        self.damage_numbers.append(DamageNumber(self, attack.damage))

    def __copy__(self):
        return self.__class__(
            self.colour,
            self.head,
            self.drops,
            self.drop_rates,
            self.attack,
            self.health,
            self.range,
            self.size,
        )

    def update(self, game_state):
        self.damage_numbers = [x for x in self.damage_numbers if not x.dead]
        # print(self.damage_numbers)
        if not self.dead:

            for i in self.damage_numbers:
                i.update(game_state['MAIN_DISPLAY_SURF'])

            colour = None

            if self.in_damage_state:
                colour = 'red'

            self.in_damage_state = self._damaging >= 0
            self._damaging -= 1

            self.draw(self.pos, game_state['MAIN_DISPLAY_SURF'], colour)

            if self.health <= 0:
                i = get_enemy_by_id(
                    game_state['_STAGE_DATA']['enemies'], self.id)

                del game_state['_STAGE_DATA']['enemies'][i]

                self.dead = True

                particle_amount = self.size_px

                game_state['PARTICLES'] += make_particles_in(pg.Rect(
                    self.pos[0], self.pos[1], self.size_px, self.size_px), particle_amount,
                    self.head.head.get_at((5, 5)))

    def draw(*_):
        """to be overridden"""
        pass

    def move(*_):
        """to be overridden (unless stationary)"""
        pass

    def __repr__(self):
        return "{} enemy colour {} size {}".format(self.__class__.__name__, self.colour, self.size)


def make_particles_in(rect, num, colour):
    """make num many particles, within rect.
    """
    return [Particle(colour, Particle.default_path((x, y)), random.randint(70, 120))
            for x, y in zip(
            [random.randint(rect.left, rect.right) for _ in range(num)],
            [random.randint(rect.top, rect.bottom) for _ in range(num)],
            )
            ]


def get_enemy_by_id(enemies, id_):
    for i, e in enumerate(enemies):
        print("%s with id %s. looking for %s" % (e, e.id, id_))
        if e.id == id_:
            return i

    raise SMRError('Enemy with id %d could not be found' % id_)
