"""
_internal.py - a VERY messy module that i 
kind of hate myself for making, but a lot of my 
files in the class_ library rely on it 
(if i could remove it, I would) :(
"""

from pprint import pprint
import os
import sys

import pygame as pg
from pygame.locals import *

import random

CHANGE_COLOUR_DIRS = ('characters_parts',
                      'heads',
                      'attacks',
                      'sword',
                      'bow',
                      'knife',
                      'spear',
                      'wand',
                      )

# print(sys.executable, 'HOWDY HO')
pg.init()
BACKWARDS = 'backwards'
FORWARDS = 'forwards'
DIR = '..\\' if os.getcwd().endswith('class_') else ''

__author__ = 'NOT Michael Gill'
__version__ = '0.0'

VALID_ENEMY_HEADS = ['smile', 'frown', 'triangle']
COLOURS = {
    'brown': (101, 67, 33),
    'dark brown': (210, 105, 30),
    'azure': (0, 127, 255),
    'light azure': (135, 206, 235),
    'light beige': (225, 198, 153),
    'beige': (232, 202, 145),
    'green': (0, 128, 0),
    'blue': (0, 0, 128),
    'light green': (109, 227, 59),
    'light blue': (173, 216, 230),
    'light red': (250, 128, 114),
    'red': (128, 0, 0),
    'dark red': (255, 0, 0),
    'dark blue': (0, 0, 255),
    'dark green': (0, 255, 0),
    'black': (0, 0, 0),
    'light black': (211, 211,
                    211),  # names like this are stupid, but must be used
    'aqua': (0, 255, 255),
    'white': (255, 255, 255),
    'teal': (0, 128, 128),
    'purple': (128, 128, 0),
    'light purple': (177, 156, 217),
    'light yellow': (255, 255, 224),
    'light cyan': (224, 255, 255),
    'light grey': (211, 211, 211),
    'dark purple': (255, 255, 0),
    'yellow': (255, 255, 0),
    'silver': (192, 192, 192),
    'gold': (192, 192, 96),
    'grey': (211, 211, 211),
    'cyan': (175, 238, 238),
}

COLOURS['gray'] = COLOURS['grey']
COLOURS['light gray'] = COLOURS['light grey']
COLOURS['light gronce'] = COLOURS['light grey']  # for Zeodexic
COLOURS['gronce'] = COLOURS['grey']


def _gather_pics(dir='.'):


    dictionary = {}
    enddir = os.path.split(dir)[-1]

    for item in os.listdir(dir):
        if '.' in item:
            pname, extension = [x.lower() for x in item.split('.')]
        fname = os.path.join(dir, item)

        if os.path.isdir(os.path.join(dir, item)):
            dictionary[item] = _gather_pics(fname)

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


# def change_alpha_to_colour(surface, colour):
#     """changes all the alpha values in surface
#     to colour.
#     """
#     alpha = pg.surfarray.pixels_alpha(surface)
#     for line in alpha:
#         for index in range(len(alpha)):
#             if line[index] != 0:
#                 line[index] =

PICS = _gather_pics(os.path.join(DIR, 'data'))
# print(DIR)
TDIR = os.path.join(DIR, 'terrains')
"""characters.py- a module of subclasses
each of these classes is a class of stickman from 
stickmanranger.
"""

DEFAULT_STATS = (50, 0, 0, 0, 0)


def change_alpha_to_colour(surf, alpha_to_colour):
    # print(alpha_to_colour)
    for alpha_value, colour in zip(alpha_to_colour.keys(),
                                   alpha_to_colour.values()):
        alpha = pg.surfarray.pixels_alpha(surf)
        colours = pg.surfarray.pixels3d(surf)
        # print(alpha)
        for i, index1 in zip(alpha, range(len(alpha))):
            for val, index in zip(i, range(len(i))):
                if val == alpha_value:
                    colours[index1][index] = colour
                    alpha[index1][index] = 255


def _Box(size, colour, pos, surface, alpha=None, image=None) -> tuple:
    """
    return a square rectangle, surface pair
    uses MyRect
    """
    # print(pos)
    new_surf = pg.surface.Surface(size)
    new_surf.fill(colour)

    if alpha is not None:
        new_surf.set_alpha(alpha)

    surface.blit(new_surf, pos)

    if image is not None:
        surface.blit(image, pos)

    return MyRect(new_surf.get_rect(topleft=pos)), new_surf


# pprint(PICS)
