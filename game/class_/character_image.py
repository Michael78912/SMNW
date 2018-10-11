"""
character_image.py
this is basically a test module at this point
attempt to build the image of the character
"""

__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
__version__ = '0.0 alpha'

import random
import time
import sys
import threading
import os

from pygame.locals import *
import pygame as pg

try:
    from sprite import SMRSprite
    from terrain import Terrain
    from _internal import PICS
    import events

except ImportError:
    from .sprite import SMRSprite
    from .terrain import Terrain
    from ._internal import PICS, COLOURS
    import class_.events as events

FPS = 50
CLOCK = pg.time.Clock()



def draw_sword(surface, armpoint, colour, length=12):
    """draws a sword on to armpoint (armpoint == hand?)"""
    colour = COLOURS[colour]
    point2 = armpoint[0], armpoint[1] - length
    return pg.draw.line(surface, colour, armpoint, point2)


def draw_halo(surface, headtopleft, colour):
    """draws a halo a couple pixels above headtopleft."""
    colour = COLOURS[colour]
    left, top = headtopleft[0] - 2, headtopleft[1] - 5
    width = 8
    height = 4
    rect = pg.Rect(left, top, width, height)
    print(rect)
    return pg.draw.ellipse(surface, colour, rect, 1)


def draw_bow(surface, armpoint, colour):
    """draws a bow to the end of armpoint."""
    # angle1, angle2 = 60, 80
    # rect = pg.Rect(0, 0, 7, 12)
    # rect.midleft = armpoint
    # print(rect)
    # pg.draw.arc(surface, colour, rect, angle1, angle2)
    pic = PICS['characters_parts']['bow'][colour]
    print(pic)

    area = armpoint[0] - 2, armpoint[1] - 7
    surface.blit(pic, area)
    # pg.image.save(surface, r'C:\Users\Michael\desktop\test_images\thing.png')


def draw_spear(surface, armpoint, colour):
    """draws a spear onto the end of the arm."""
    pic = PICS['characters_parts']['spear'][colour]
    pos = armpoint[0] - 6, armpoint[1] - 10
    surface.blit(pic, pos)
    # pg.image.save(surface, r'C:\Users\Michael\desktop\test_images\thing.png')
    return surface


def draw_wand(surface, armpoint, colour):
    """draws a wand on the end of the arm."""
    draw_sword(surface, armpoint, colour, 7)
   # pg.image.save(surface, r'C:\Users\Michael\desktop\test_images\thing.png')


DEFAULT_WEAPONS = {
    'swordsman': draw_sword,
    'angel': draw_halo,
    'archer': draw_bow,
    'spearman': draw_spear,
    'wizard': draw_wand,
}


class CharacterImage(SMRSprite):
    """
    this is a sprite that at this point, should really
    just be able to move around.
    """
    sizex = 7
    sizey = 9
    size = (5, 10)
    head_radius = 2
    head_diameter = head_radius * 2

    def __init__(self, type_, weapon,
                 pos: 'the topleft corner (in cartesian system)',
                 main_game_state, event_queue):

        SMRSprite.__init__(self, main_game_state, event_queue, pos)
        self.type_ = type_
        self.weapon = weapon
        self.topleft = pos
        self.bottomleft = pos[0], pos[1] + self.sizey
        self.topright = pos[0] + self.sizex, pos[1]
        self.bottomright = pos[0] + self.sizex, pos[1] + self.sizey

    def build_image(self, surface):
        """
        constructs and draws the stickman to the 
        screen.
        """

        # this is the image of the character
        mainsurf = pg.surface.Surface(self.size)

        # all these are making the right arm
        rarm = [
            [..., ...], [..., ...]
        ]  # skeleton for 2D-lsit (First time to actually get to use Ellipsis!)
        rarm[0][0] = self.topright[0] - (self.sizex // 2)
        # X- coordinate should be directly on arm
        rarm[0][1] = self.topright[1] - (self.sizey // 6 * 9)
        # 3 quarters up the arm should be good

        # exactly on edge of player's hitbox
        rarm[1][0] = self.topright[0]

        # randomly on the top half of hitbox
        rarm[1][1] = random.randint(self.topright[1] - (self.sizey // 2),
                                    self.topright[1])

        self.rarm_rect = pg.draw.line(surface, COLOURS['beige'], rarm[0],
                                      rarm[1])

        # larm is basically a repeat of rarm, only a few modifications
        larm = [[..., ...], [..., ...]]
        # same coordinate for part that attaches to body is OK
        larm[0] = rarm[0]
        larm[1][0] = self.topleft[0]
        larm[1][1] = random.randint(self.topleft[1] - (self.sizey // 2),
                                    self.topright[1])

        self.larm_rect = pg.draw.line(surface, COLOURS['beige'], *larm)

        body1 = self.topright[0] - self.sizex // 2
        body2 = self.topleft[1] - self.sizey
        start = body1, body2

        body1 = self.bottomright[0] - self.sizex // 2
        body2 = self.bottomright[1] - self.sizey
        end = body1, body2

        self.body = pg.draw.line(surface, COLOURS['beige'], start, end, 1)

        head_center_pos = self.topright[0] - self.sizex // 2, self.topleft[1] - (
            self.sizey + 2)
        self.head = {'center': head_center_pos, 'radius': self.head_radius}
        self.head_rect = pg.draw.circle(surface, COLOURS['beige'],
                                        head_center_pos, self.head_radius, 1)

        rleg = [[..., ...], [..., ...]]
        rleg[0] = end
        rleg[1][0] = random.randint(self.bottomleft[0],
                                    self.sizex // 2 + self.bottomleft[0])
        rleg[1][1] = self.bottomleft[1]
        self.rleg = rleg

        self.rleg_rect = pg.draw.line(surface, COLOURS['beige'], *rleg)

        lleg = [[..., ...], [..., ...]]
        lleg[0] = end
        lleg[1][0] = random.randint(self.bottomright[0],
                                    self.sizex // 2 + self.bottomright[0])
        lleg[1][1] = self.bottomright[1]
        self.lleg = lleg
        self.lleg_rect = pg.draw.line(surface, COLOURS['beige'], *lleg)

        if self.type_ == 'angel':
            draw_halo(surface, self.head_rect.topleft, self.weapon.colour)
        else:
            DEFAULT_WEAPONS[self.type_](surface, rarm[1], self.weapon.colour)

    def move_to_x(self, pos: 'x', surface, pixels=1, invisible=False):
        """
        moves the character image by pixels
        towards the destination.
        INCOMPLETE: only X coordinates are supported
        """

        current = self.topleft[0]

        current_pos = current - pixels if pos < current else current + pixels
        print(current_pos)
        self.update_coords((current_pos, self.topleft[1]))
        self.build_image(surface)
        return current_pos

    def move_to_y(self, pos: 'y', surface, pixels=1, invisible=False):
        current = self.topleft[1]

        current_pos = current - pixels if pos < current else current + pixels
        print(current_pos)
        self.update_coords((current_pos, self.topleft[1]))
        self.build_image(surface)
        return current_pos

    def move_to(self, pos: 'x / y', surface, pixels=1):
        coord = random.randrange(1)
        func = self.move_to_y if coord == 1 else self.move_to_x
        return coord, func(pos[coord], surface, pixels)

    def _mainloop(self, pos, surface, pixels, invisible=False, *args,
                  **kwargs):
        new_pos = -1  # the coordinate can never be this
        at_pos = False
        # at pos will keep the main loop going

        while True:
            if not self._internal_events.empty():
                f = self._internal_events.get()
                if type(f) == events.Quit:
                    print('return')
                    print('exiting')
                    os._exit(0)

                elif type(f) == events.Pause:
                    if f.keep:
                        self.internal_event(f)
                        continue

            # print(threading.current_thread())
            # print(new_pos)
            if not at_pos:
                new_pos = self.move_to_x(pos, surface, pixels, invisible,
                                         *args, **kwargs)
            CLOCK.tick(FPS)
            if pos == new_pos:
                at_pos = True

    def start_thread(self, move_to, surf, pixels=1, daemon=False):
        self.mainproc = threading.Thread(
            target=self._mainloop, args=(move_to, surf, pixels), daemon=daemon)

        self.mainproc.start()


class WeaponDummy:

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return 'WeaponDummy object with Surface %s' % self.image


def main():
    pg.init()
    a = pg.display.set_mode((800, 400))
    testsurf = pg.surface.Surface((2, 2))
    testsurf.fill(COLOURS['green'])
    t = Terrain('dirt', 'flattish')
    t_surf = t.build_surface()
    a.blit(t_surf, (0, 0))
    print('blitted')
    #d = CharacterImage('test', WeaponDummy(testsurf), (0, 0), {}, {})
    #d.start_thread((200, 100), a)
    print(
        CharacterImage.get_topleft_coord(t,
                                         *CharacterImage.find_closest_of(
                                             t, '*')))
    truecoord = CharacterImage.find_closest_of(
        t, '*')[0], CharacterImage.find_closest_of(t, '*')[1]
    print(
        CharacterImage.get_topleft_coord(t, *truecoord),
        CharacterImage.get_topleft_coord(t,
                                         *CharacterImage.find_closest_of(
                                             t, '*')))
    # s.start_thread(CharacterImage.get_topleft_coord(t, *CharacterImage.find_closest_of(t, '#')), a)
    # for i in range(100):
    #     i = CharacterImage('test', WeaponDummy(testsurf), (0,0), {}, {})
    #     i.start_thread((0, 0 ), a)
    pause = events.Pause()
    s = CharacterImage('test', WeaponDummy(testsurf),
                       CharacterImage.get_topleft_coord(t, *truecoord), {}, {})
    print(CharacterImage.get_topleft_coord(t, *truecoord))
    s.start_thread(800, a)

    while True:
        #a.blit(PICS['Maps']['army'], CharacterImage.get_topleft_coord(t, *CharacterImage.find_closest_of(t, '*')))
        # s.build_image(a)
        for i in pg.event.get():
            if i.type == QUIT:
                print('hello?')
                # cleanup and saving and stuff like that can go here, but for now time.sleep tests it.
                # always remove the pause from _internal_events before putting
                # Quit
                os._exit(0)

                #import time; time.sleep(1)

        try:
            pg.display.update()
            a.fill(COLOURS['black'])
            a.blit(t_surf, (0, 0))
        except pg.error:
            # os._exit is about to be called in a seperate thread
            pass

        print('updated')
        CLOCK.tick(FPS)


def main2():
    s = pg.Surface((100, 100))
    c = CharacterImage('swordsman', None, (20, 20), {}, None)
    c.build_image(s)
    pg.image.save(s, r'C:\Users\Michael\Desktop\hi.png')

if __name__ == '__main__':
    main2()
