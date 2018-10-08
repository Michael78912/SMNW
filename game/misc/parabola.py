import math
import sys
import os

from pprint import pprint

import pygame as pg
from pygame.locals import QUIT

sys.stdout = open(os.path.join(os.environ['USERPROFILE'], 'Desktop', 'stdout.log'), 'w')


CLOCK = pg.time.Clock()
FPS = 60

class Arcer:
    def __init__(self, img, range_, pos):
        self.img = img
        self.range = range_
        self.rect = img.get_rect(topleft=pos)
        self.sizey = self.rect.y
        self.sizex = self.rect.x
        self.update_coords(pos)

    def update_coords(self, pos):
        self.topleft = pos
        self.bottomleft = pos[0], pos[1] + self.sizey
        self.topright = pos[0] + self.sizex, pos[1]
        self.bottomright = pos[0] + self.sizex, pos[1] + self.sizey
        self.rect = self.img.get_rect(topleft=pos)

    def draw(self, surf):
        surf.blit(self.img, self.topright)

    def get_parabola(self, target):
        f = lambda x: (2 / math.pi) * math.atan(2 * (chary - tary) / (charx - tarx) ** 2 * (x - tarx))

        pt2 = tarx, tary = target
        pt1 = charx, chary = self.topleft

        playx, playy = [], []
        actualx = charx
        actualy = chary
        

        i = charx

        print('local variables before while loop:', end='')
        pprint(locals())

        while i <= 610 and i >= -1000:
            perc = f(actualx)
            print('actualx:', actualx, 'actualy:', actualy)
            print('playy: ', playy, '\n', 'playx: ', playx)
            print('charx, chary, tarx, tary to make sure they arent changing:', charx, chary, tarx, tary)
            actualy += perc
            actualx += 1 - perc
            playy.append(math.floor(actualy))
            playx.append(math.floor(actualx))
            if tarx >= charx:
                i += 1
            else:
                i -= 1

        return playx, playy
        #         if val == 0:
        #     while i <= 610 and i >= -1000:
        #         array.append((chary, round((chary - tary) / val * pow((i - tarx), 2) + tary)))
        #         if tarx >= charx:
        #             i += 1
        #         else:
        #             i -= 1

        # else:
        #     while i <= 610 and i >= -1000:
        #         array.append((i, round((chary - tary) / val * pow((i - tarx), 2) + tary)))
        #         if tarx >= charx:
        #             i += 1
        #         else:
        #             i -= 1


def main():
    display = pg.display.set_mode((800, 400))
    testsurf = pg.Surface((10, 10))
    testsurf.fill((0, 255, 0))
    target = (300, 300)
    test = Arcer(testsurf, 100, (20, 20))
    a = pg.Surface((10, 10))
    a.fill((0, 0, 255))
    display.blit(a, target)
    arr = test.get_parabola(target)
    #print(arr)
    index = 0
    import time
    time.sleep(3)

    while True:
        for ev in pg.event.get():
            if ev.type == QUIT:
                pg.quit()
                raise SystemExit

        pg.display.update()
        display.fill((0, 0, 0))
        display.blit(testsurf, (arr[0][index], arr[1][index]))
        #test.draw(display)
        #print(index)
        index += 1
        CLOCK.tick(25)
        display.blit(a, target)


if __name__ == '__main__':
    main()
