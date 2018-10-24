import json as _json
import os
import enum

import pygame as _pg

_pg.mixer.pre_init(44100, 16, 2, 4096)
_pg.init()

import save
import class_ as _class_
from class_.sprite import SMRSprite as SpriteUtils

SURFACE = _pg.display.set_mode((800, 600))
_pg.display.set_caption("Stickman's New World")

_HOME = os.getenv('USERPROFILE') or os.getenv("HOME")
SAVE_DIR = os.path.join(_HOME, '.stickman_new_world')


class Area(enum.Enum):
    """area of the game currently."""
    TITLE = 0
    MAP = 1
    STAGE = 2
    PAUSE = 3


# dictionary of color strings containing RGB values
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
#open = lambda file: __builtins__.open(os.path.join('config', file))


_DECODE = _json.JSONDecoder()
SETTINGS = _DECODE.decode(open(os.path.join('config', 'settings.json')).read())
ALL = _DECODE.decode(open(os.path.join('config', 'data.json')).read())
ALL_CLASSES = ['Swordsman', 'Spearman', 'Wizard', 'Archer', 'Angel']
# print(ALL)

ALL_TERRAINS = [
    _class_.Terrain('dirt', 'flat'),
]

# ALL_LEVELS = {
#     'village':
#     _class__.Stage(
#         position_on_map=(18, 589),
#         all_screens=[_class_.PeacefulScreen()],
#         boss_screen=None,
#         surface=SURFACE,
#         terrain=ALL_TERRAINS[0],
#         comes_from=None,
#         decorations=_class__.BackGroundImage('hut',
#                                             SpriteUtils.get_topleft_coord(
#                                                 ALL_TERRAINS[0],
#                                                 *SpriteUtils.find_closest_of(
#                                                     ALL_TERRAINS[0], '*'))))
# }

ALL_LEVELS = {
    _class_.Stage(
        "Test Stage",
        position_on_map=(70, 569),
        all_screens=[_class_.Screen(
            {_class_.Blob(
                COLOURS['blue'],
                _class_.EnemyHead(
                    'sad_box',
                    'red',
                    1,
                ),
                (),
                (),
                _class_.Attack(),
                1
            ): 6,
            _class_.Blob(
                COLOURS['red'],
                _class_.EnemyHead(
                    'normal',
                    'green',
                    6,
                    ),
                (),
                (),
                _class_.Attack(),
                6,
                ): 3,
            },
        )],
        boss_screen=None,
        surface=SURFACE,
        terrain=_class_.Terrain('dirt', 'flat'),
        comes_from=None,
        # peaceful=True,
    ),
}

ALL_SCREENS = []

ALL_WEAPONS = []

ALL_COMPOS = []

if os.path.exists(SAVE_DIR):
    _SAVE = save.read_file()
    print(_SAVE)
    _INV_RAW = _SAVE['inventory']
    x, y = max([int(i.split('x')[0]) for i in _INV_RAW]), max(
        [int(i.split('x')[1]) for i in _INV_RAW])
    _INV = _class_.InventoryHandler(x, y)
    _INV.sort_dict(_INV_RAW)

    MAIN_GAME_STATE = {
        'AREA': 0,
        'SETTINGS': SETTINGS,
        'GAME_DATA': _SAVE,
        'INVENTORY': _INV,
        'MAIN_DISPLAY_SURF': SURFACE,
    }
else:
    MAIN_GAME_STATE = {
        'AREA': 0,
        'SETTINGS': SETTINGS,
        'GAME_DATA': {},
        'INVENTORY': {},
        'MAIN_DISPLAY_SURF': SURFACE,
    }


import picture_collect

PICS = picture_collect.gather_pics('data')
