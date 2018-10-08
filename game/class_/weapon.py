import os

import pygame

try:
    from _internal import *

except ImportError:
    from ._internal import *

print(PICS)

__all__ = ['Weapon']


class Weapon:
    def __init__(self, klass, colour, level, alphatocolour=None):
        self.largeicon = PICS['weapons']['large_icon'][klass][repr(level)][
            colour]
        self.smallicon = PICS['weapons']['small_icon'][klass][repr(level)][
            colour]
        if alphatocolour is not None:
            change_alpha_to_colour(self.largeicon, alphatocolour)
            change_alpha_to_colour(self.smallicon, alphatocolour)

        rect = self.largeicon.get_rect()
        pos = rect.bottomright[0] - 4, rect.bottomright[1] - 9
        font = pygame.font.Font('freesansbold.ttf', 8)
        print(font.size('8'))
        surf = font.render(repr(level), True, COLOURS['black'])
        self.largeicon.blit(surf, pos)


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
