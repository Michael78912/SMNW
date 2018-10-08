"""
dicts.py
this module holds functions and data that deal
with large dictionaries, which this game uses a lot
of 
GetPics-return a dictionary containing 
string keys and pygame image equivelants.
COLOURS: a dictionary containing string keys
and RGB tuple values."""
import os
print('Howdy')
import pprint

from pygame.image import load
import pygame as pg

from database import *

__author__ = 'Michael Gill'
__version__ = '0.0'

CHANGE_COLOUR_DIRS = ('characters_parts',
                      'heads',
                      'attacks',
                      ) + tuple(ALL['all_weapons'].values())

print(CHANGE_COLOUR_DIRS)


def gather_pics(dir='.'):


    dictionary = {}
    enddir = os.path.split(dir)[-1]

    for item in os.listdir(dir):
        if '.' in item:
            pname, extension = [x.lower() for x in item.split('.')]
        fname = os.path.join(dir, item)

        if os.path.isdir(os.path.join(dir, item)):
            dictionary[item] = gather_pics(fname)

        elif extension in ('png', 'jpg'):
            dictionary[pname] = pg.image.load(fname)

            if enddir in CHANGE_COLOUR_DIRS:
                # heads, attacks, and weapons should be of each colour
                # print(dir)
                di = dictionary[pname] = {}
                for col in COLOURS:
                    # print(dir, col)
                    rgb_col = COLOURS[col]
                    di[col] = pg.image.load(os.path.join(dir, item))
                    change_colour_surface(di[col], *rgb_col)

    return dictionary


def change_colour_surface(surface, r, g, b):
    """changes the colour of all parts of a 
    surface except for the transparent parts.
    """
    arr = pg.surfarray.pixels3d(surface)
    arr[:, :, 0] = r
    arr[:, :, 1] = g
    arr[:, :, 2] = b


if __name__ == '__main__':
    dict = gather_pics('data')
    print('\n' * 1000)
    pprint.pprint(dict)
    # print(dict)
    print('Howdy')
    pg.image.save(gather_pics('data')['game_icon'], r'C:\Users\Michael\Desktop\test_images\howdy.png')
