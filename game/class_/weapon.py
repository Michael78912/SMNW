import os

import pygame

try:
    from _internal import *

except ImportError:
    from ._internal import *

__all__ = ['Weapon']


class Weapon:
    cooldown = 0
    def __init__(self, klass, name, colour, level, attack, range, alphatocolour=None):
        self.largeicon = PICS['weapons']['large_icon'][klass][repr(level)][
            colour]
        self.smallicon = PICS['weapons']['small_icon'][klass][repr(level)][
            colour]
        if alphatocolour is not None:
            change_alpha_to_colour(self.largeicon, alphatocolour)
            change_alpha_to_colour(self.smallicon, alphatocolour)

        self.name = name
        self.colour = colour
        self.range = range
        self.attack = attack

        rect = self.largeicon.get_rect()
        pos = rect.bottomright[0] - 4, rect.bottomright[1] - 9
        font = pygame.font.Font('freesansbold.ttf', 8)
        print(font.size('8'))
        surf = font.render(repr(level), True, COLOURS['black'])
        self.largeicon.blit(surf, pos)

    def can_attack(self):
        """return true if the weapon is able to attack."""
        return self.cooldown == 0

    def update(self):
        if self.cooldown != 0: self.cooldown -= 1

    def attack_enemy(self, origin, target, game_state):
        self.cooldown = self.attack.cooldown
        self.attack.attack(origin, target, game_state)


if __name__ == '__main__':
    pygame.init()
    a = pygame.display.set_mode((1000, 1000))
    a.fill(COLOURS['blue'])
    a.blit(
        Weapon('sword', 'grey', 1, {
            100: COLOURS['dark brown'],
            150: COLOURS['brown']
        }).largeicon, (0, 0))
    while 1:
        for ev in pygame.event.get():
            if ev.type == 12:
                raise SystemExit
        pygame.display.update()
