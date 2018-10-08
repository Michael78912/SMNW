import math

import pygame as pg
from pygame.locals import QUIT


FPS = 20
CLOCK = pg.time.Clock()


class GravityItem:
    weight = 10   # weight is amount of pixels it should move down per frame - momentum
    sizey = sizex = 10

    def __init__(self, img, pos):
        self.img = img
        self.update_coords(pos)

    def update_coords(self, pos):
        self.topleft = pos
        self.bottomleft = pos[0], pos[1] + self.sizey
        self.topright = pos[0] + self.sizex, pos[1]
        self.bottomright = pos[0] + self.sizex, pos[1] + self.sizey

    def draw(self, surface, override_pos=None):
        if override_pos is not None:
            self.update_coords(override_pos)

        surface.blit(self.img, self.topright)

    def move_gravity_momentum(self, momentum, px_x):
        to_move = momentum - self.weight
        # if momentum is greater than weight, it will move up
        self.update_coords((
                self.topright[0] - px_x,
                self.topright[1] + to_move,
            ))

    def get_top_of_arc(self, enemy_pos):
        # use parabola, thx to Dracobot




def main():
    mainsurf = pg.display.set_mode((400, 400))
    sprite = pg.Surface((10, 10))
    sprite.fill((0, 255, 0))
    gv = GravityItem(sprite, (200, 200))

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                raise SystemExit
        gv.move_gravity_momentum(10, 1)
        gv.draw(mainsurf)
        pg.display.flip()
        CLOCK.tick(FPS)
        mainsurf.fill((255,) * 3)





if __name__ == '__main__':
    main()