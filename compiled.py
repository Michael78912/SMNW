import zipfile
import tarfile
import gzip
import bz2
import os
import subprocess
import shutil
import glob
import json

GIT_SCRIPT = """
git clone https://michael78912/smnw-archives
cd smnw-archives
git init
echo copying archives...
cp ../Archives/* .
git add *
git push origin master
"""


def make_xz(file, dir='.'):
    """
    compresses file and saves it to
    [file].xz in the dir.
    """
    os.system('xz -k ' + os.path.join(dir, file))


def make_tarfile(source_dir):
    with tarfile.open(source_dir + '.tar', "w") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def make_gz(file, dir='.'):
    os.system('gzip -k ' + file)


def make_bz2(file, dir='.'):

    os.system('bzip2 -k ' + os.path.join(dir, file))


def make_zipfile(dir):
    print('writing xipfile')
    zipfile.main(['-c', dir + '.zip', dir])


def make_7z(dir):
    print('writeing 7z')
    try:
        os.remove('logs.7z')
    except:
        pass
    old = os.getcwd()
    os.chdir(dir)
    os.system('7z a %s -r' % dir)

    shutil.move('logs.7z', '..')
    os.chdir(old)


def get_ver():
    old_ver_file = json.load(open('/mnt/m/stickman\'s_new_world/game/config/config.json'))
    old_ver = old_ver_file['version']
    new_ver = input('old version: {}. new version: '.format(old_ver))
    old_ver_file['version'] = new_ver
    json.dump(old_ver_file, open('/mnt/m/stickman\'s_new_world/game/config/config.json'))
    with open('Archives/ver.txt', 'w') as verfile:
        verfile.write(new_ver)
    
    

def write_archive():
    for arc in glob.glob('stickman*.*'):
        os.remove(arc)

    for func in (make_zipfile, make_tarfile, make_7z):
        func('logs')

    for arc in glob.glob('logs.*'):
        os.rename(arc, 'stickman\'s new world.' + arc.split('.')[1])

    for func in (make_xz, make_bz2, make_gz):
        func('"stickman\'s new world.tar"')

    shutil.rmtree('Archives')
    os.mkdir('Archives')

    for arc in glob.glob('stickman*.*'):
        shutil.move(arc, 'Archives')
    get_ver()
    os.system('bash tmp.sh')


write_archive()
import os

file = open('compiled.py', 'w')

def f(dir='.'):
    for i in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, i)):
            f(os.path.join(dir, i))

        elif i.endswith('.py'):
            file.write(open(os.path.join(dir, i)).read())

f()
file.close()
from py_compile import compile as compile_py
from argparse import ArgumentParser
from json import JSONDecoder
from glob import glob
import os
import sys

__version__ = '0.0'
__author__ = 'Michael Gill'


def version():
    """
    outputs version info to the screen.
    """
    print('compile_all version {__version__} by {__author__}.'.format(
        **globals()))


def main(
        dir=os.path.abspath('.'),
        outputdir='compiled',
        recurse_dirs=False,
        placeinsubdirs=False):
    """
    compiles all files ending in .py or .pyw to
    .pyc files, and places them in outputdir.
    if recurse_dirs == True, then it will be done to
    all subdirectories as well.
    """
    try:
        if glob(os.path.join(dir, '*.py')) + glob(os.path.join(dir,
                                                               '*.pyw')) == []:
            print(dir + ', no python source files found!')
        os.listdir(dir)
    except PermissionError:
        print(dir, 'permission denied!')
        return
    for file in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, file)) and recurse_dirs:
            if placeinsubdirs:
                new_outputdir = os.path.join(outputdir, file)
            else:
                new_outputdir = outputdir
            print('entering', file)
            main(
                dir=os.path.join(dir, file),
                outputdir=new_outputdir,
                recurse_dirs=True,
                placeinsubdirs=placeinsubdirs)

        if not recurse_dirs and os.path.isdir(os.path.join(dir, file)):
            continue

        else:
            if file.endswith(('.py', '.pyw')):
                print('attempting to compile', os.path.join(dir, file))
                print(
                    compile_py(
                        os.path.join(dir, file),
                        os.path.join(outputdir,
                                     '.'.join(file.split('.')[:-1]) + '.pyc')),
                    'compiled.')


if __name__ == '__main__':
    parser = ArgumentParser(
        description='compiles all python files in directory.')
    parser.add_argument(
        '--directory',
        '-d',
        help='the input directory with your python files.')

    parser.add_argument(
        '--output-dir', '-o', help='the output directory for the files to go.')

    parser.add_argument(
        '--recurse-subdirs',
        '-r',
        help='recurse the subdirectories',
        action="store_true")
    parser.add_argument(
        '--place-subfiles-in-subdirs',
        '-p',
        help='store the files from sub-directories in the equivalent sub directories. must be used with the -r option.',
        action='store_true')
    parser.add_argument(
        '--version',
        '-v',
        help='output the version information and exit.',
        action='store_true')

    a = parser.parse_args()
    if a.output_dir is None:
        a.output_dir = os.path.join(os.path.abspath('.'), 'compiled')

    if a.directory is None:
        a.directory = os.path.abspath('.')

    if a.version:
        version()

    else:
        main(
            dir=a.directory,
            outputdir=a.output_dir,
            recurse_dirs=a.recurse_subdirs,
            placeinsubdirs=a.place_subfiles_in_subdirs,
        )
import os


def main(dir):
    for i in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, i)):
            main(os.path.join(dir, i))
        elif i.endswith('.py'):
            print('formatting %s' % i)
            os.system('yapf -i ' + os.path.join(dir, i))
            os.system('autopep8 -i ' + os.path.join(dir, i))


if __name__ == '__main__':
    main('.')
import urllib.request
import json
import os
try:
    import httplib

except ImportError:
    import http.client as httplib


def have_internet():
    conn = httplib.HTTPConnection("www.example.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


VER_URL = "https://drive.google.com/uc?export=download&id=17KGPTgF6xWKH3dk7Sd74niL548WU6Tts"


def check_update():
    data = {}
    # VER_URL is a shared google drive link that has the current version of stickmanranger
    with urllib.request.urlopen(VER_URL) as response:
        version = response.read().decode()
    # decode the current version from "settings.json"
    current_version = json.JSONDecoder().decode(
        open(os.path.join('config', 'windows_config.json')).read())['version']
    # if the version is the same
    print(current_version, version)

    if current_version == version:
        return False
    return True


def main():
    print(check_update())
    if check_update():
        import run_auto_install


main()
"""a file for representing an attack."""

class Attack:
    def __init__(self, damage, cooldown):
        self.damage = damage
        self.cooldown = cooldown

    def __repr__(self):
    	return "{}(damage={}, cooldown={})".format(self.__class__.__name__, self.damage, self.cooldown)
try:
    from _internal import PICS
except ImportError:
    from ._internal import PICS


class BackGroundImage:
    """
    this has no effect on the stage itself, 
    but is just for decoration.
    """

    def __init__(self, name, topright, priority=1, put_on_terrain=None):
        self.toprgight = topright
        self.image = PICS['backgrounds'][name]
        self.priority = priority
        try:
            self.__class__.instances.append(self)
        except AttributeError:
            # this is the first instance
            self.__class__.instances = [self]

    def __del__(self):
        # must remove the current instance from instances
        self.__class__.instances.pop(self.__class__.instances.index(self))

    def draw(self, surf):
        """
        draw the image to surf
        """
        surf.blit(self.image, self.topright)

    @classmethod
    def draw_all(cls, surf):
        """
        draw all of the current instances to surf
        """
        orderedpairs = sorted(
            [(ins.priority, ins) for ins in cls.instances], key=lambda x: x[0])

        for pair in orderedpairs:
            pair[1].draw(surf)


if __name__ == '__main__':
    print(BackGroundImage('hut', (0, 0)).instances)
try:
    from character_image import CharacterImage
    from klass import Class

except ImportError:
    from .character_image import CharacterImage
    from .klass import Class


class Character(Class, CharacterImage):
    ...
"""characters.py- a module of subclasses
each of these classes is a class of stickman from 
stickmanranger.
"""
try:
    from _internal import *
    from klass import Class

except ImportError:
    from ._internal import *
    from .klass import Class

__all__ = ['Swordsman', 'Angel', 'Archer', 'Spearman', 'Wizard']

DEFAULT_STATS = (50, 0, 0, 0, 0)


class Swordsman(Class):
    image = PICS['characters']['swordsman']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'swordsman', player_num, weapon, main_game_state, stats)


class Angel(Class):
    image = PICS['characters']['angel']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'angel', player_num, weapon, main_game_state, stats)


class Archer(Class):
    image = PICS['characters']['archer']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'archer', player_num, weapon, main_game_state, stats)


class Spearman(Class):
    image = PICS['characters']['spearman']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'spearman', player_num, weapon, main_game_state, stats)


class Wizard(Class):
    image = PICS['characters']['wizard']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'wizard', player_num, weapon, main_game_state, stats)
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



def draw_sword(surface, armpoint, colour, length=16):
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
    return pg.draw.ellipse(surface, colour, rect, 1)


def draw_bow(surface, armpoint, colour):
    """draws a bow to the end of armpoint."""
    # angle1, angle2 = 60, 80
    # rect = pg.Rect(0, 0, 7, 12)
    # rect.midleft = armpoint
    # print(rect)
    # pg.draw.arc(surface, colour, rect, angle1, angle2)
    pic = PICS['characters_parts']['bow'][colour]

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
    has_drawn = False
    sizex = 7
    sizey = 10
    hitbox = (11, 26)
    size = (sizex * 2, sizey * 2)
    head_radius = 3
    head_diameter = head_radius * 2

    def __init__(self, type_, weapon,
                 pos: 'the topleft corner (in cartesian system)',
                 main_game_state):

        SMRSprite.__init__(self, main_game_state, None, pos)
        self.type_ = type_
        self.weapon = weapon
        self.topleft = pos
        self.bottomleft = pos[0], pos[1] + self.sizey
        self.topright = pos[0] + self.sizex, pos[1]
        self.bottomright = pos[0] + self.sizex, pos[1] + self.sizey

    def build_image(self, surface, colour, rebuild=True):
        """constructs and draws the stickman to the 
        screen. if rebuild is false, use the last image.
        """
        if rebuild or not self.has_drawn:
            self.has_drawn = True

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

            self.rarm = rarm

            self.rarm_rect = pg.draw.line(surface, colour, rarm[0],
                                          rarm[1], 2)

            # larm is basically a repeat of rarm, only a few modifications
            larm = [[..., ...], [..., ...]]
            # same coordinate for part that attaches to body is OK
            larm[0] = rarm[0]
            larm[1][0] = self.topleft[0]
            larm[1][1] = random.randint(self.topleft[1] - (self.sizey // 2),
                                        self.topright[1])

            self.larm = larm

            self.larm_rect = pg.draw.line(surface, colour, larm[0], larm[1], 2)

            body1 = self.topright[0] - self.sizex // 2
            body2 = self.topleft[1] - self.sizey
            start = body1, body2

            body1 = self.bottomright[0] - self.sizex // 2
            body2 = self.bottomright[1] - self.sizey
            end = body1, body2

            self.start, self.end = start, end

            self.body = pg.draw.line(surface, colour, start, end, 2)

            head_center_pos = self.topright[0] - self.sizex // 2, self.topleft[1] - (
                self.sizey + 2)
            self.head_center = head_center_pos
            self.head = {'center': head_center_pos, 'radius': self.head_radius}
            self.head_rect = pg.draw.circle(surface, colour,
                                            head_center_pos, self.head_radius, 1)

            rleg = [[..., ...], [..., ...]]
            rleg[0] = end
            rleg[1][0] = random.randint(self.bottomleft[0],
                                        self.sizex // 2 + self.bottomleft[0])
            rleg[1][1] = self.bottomleft[1]
            self.rleg = rleg

            self.rleg_rect = pg.draw.line(surface, colour, rleg[0], rleg[1], 2)

            lleg = [[..., ...], [..., ...]]
            lleg[0] = end
            lleg[1][0] = random.randint(self.bottomright[0],
                                        self.sizex // 2 + self.bottomright[0])
            lleg[1][1] = self.bottomright[1]
            self.lleg = lleg
            self.lleg_rect = pg.draw.line(surface, colour, lleg[0], lleg[1], 2)

            

        else:
            pg.draw.line(surface, colour, self.rarm[0], self.rarm[1], 2)
            pg.draw.line(surface, colour, self.larm[0], self.larm[1], 2)
            pg.draw.line(surface, colour, self.rleg[0], self.rleg[1], 2)
            pg.draw.line(surface, colour, self.lleg[0], self.lleg[1], 2)
            pg.draw.line(surface, colour, self.start, self.end, 2)
            pg.draw.circle(surface, colour, self.head_center, self.head_radius, 1)

        if self.type_ == 'angel':
                draw_halo(surface, self.head_rect.topleft, self.weapon.colour)
        else:
            DEFAULT_WEAPONS[self.type_](surface, self.rarm[1], self.weapon.colour)

        self.rect = pg.Rect(self.topright, self.hitbox)


    def move_to_x(self, pos: 'x', surface, pixels=1, invisible=False):
        """
        moves the character image by pixels
        towards the destination.
        INCOMPLETE: only X coordinates are supported
        """

        current = self.topleft[0]

        current_pos = current - pixels if pos < current else current + pixels
        self.update_coords((current_pos, self.topleft[1]))
        # self.build_image(surface)

        return current_pos

    def move_to_y(self, pos: 'y', surface, pixels=1, invisible=False):
        current = self.topleft[1]

        current_pos = current - pixels if pos < current else current + pixels
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

    def __init__(self, colour):
        self.colour = colour
    def __repr__(self):
        return 'WeaponDummy object with Surface %s' % self.image



def main2():
    s = pg.Surface((100, 100))
    c = CharacterImage('swordsman', None, (20, 20), {}, None)
    c.build_image(s)
    pg.image.save(s, r'C:\Users\Michael\Desktop\hi.png')

if __name__ == '__main__':
    main2()
"""damagenumbers- an enemy will have a list of damage numbers.
it will display them all over time.
"""
import os
import random

import pygame as pg
GRAY = (220, 220, 220)

class DamageNumber:
	"""display as a number coming from the enemy"""
	lifespan = 60
	dead = False
	font = pg.font.Font(os.path.join('data', 'Roboto-Regular.ttf'), 9)

	def __init__(self, enemy, damage):
		"""initiate instance>"""
		self.surf = self.font.render(str(damage), False, GRAY)
		self.rect = self.surf.get_rect()
		self.rect.center = (enemy.pos[0] + enemy.size_px // 2) + random.randint(-3, 3), enemy.pos[1] - 10

	def update(self, surface):
		"""update and draw to surface"""
		if self.lifespan == 0:
			self.dead = True
		if not self.dead:
			surface.blit(self.surf, self.rect)
			self.rect.y = self.rect.y - 1
			self.lifespan -= 1"""
drop.py
this is a base class, that is to derive compos/weapons from (and anything i might add later ;))
definitely not to be used directly.
"""


class DropItem:
    def __init__(self, smallicon, largeicon, surface, stats_to_display=''):
        self.smallicon = smallicon
        self.largeicon = largeicon
        if isinstance(stats_to_display, dict):
            self.stats_to_display = stats_to_display

        elif isinstance(stats_to_display, str):
            d = stats_to_display.split('\n')
            stats_to_display = {}
            for i in d:
                stats_to_display[i.split(':')[0]] = i.split(':')[1]
            self.stats_to_display = stats_to_display

    def draw_large(self, pos):
        """
        blits self.largeicon to surface.
        """
        self.surface.blit(self.largeicon, pos)

    def draw_small(self, pos):
        self.surface.blit(self.smallicon, pos)
"""enemies.py- contains enemies that are used in SMNW.
may create a seperate library for these one day, but until I 
decide to use something other than Blob and Stationary, I'll be fine.
"""


import random


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
        # pylint: disable=too-many-locals
        """moves the enemy towards the closest player to it.
        the Blob does not move too much, and has a 1/4 (intelligence)
        chance of moving the way away from the players.
        """
        if random.randint(1, self.chance_of_motion) == 1:
            # innocent until proven guilty. (of being in a pit)
            can_move = True

            in_air = terrain.is_in_air(self.pos, terrain_obj, self.size_px)

            current_block_x = terrain_obj.px_to_blocks(self.pos[0])
            current_block_y = terrain_obj.px_to_blocks(self.pos[1])

            next_column = list(terrain_obj.terrain2dlist_texts[terrain_obj.template]
                               ['text'][:, current_block_x - 1])

            top_levels = {i if obj == '*' else None for i,
                          obj in enumerate(next_column)}
            top_levels.remove(None)

            if in_air:
                # fall two pixels, because enemy is in air
                self.fell_on_last = 1
                self.pos = self.pos[0], self.pos[1] + 2

            elif self.fell_on_last == 1:
                self.fell_on_last = 0
                # for some strange reason that is completely beyond me,
                # all enemies seem to stay 4 pixels above ground after falling.
                # this fixes that.
                self.pos = self.pos[0], self.pos[1] + 4

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


class Stationary(Blob):
    """similar to blob, but does n ot move."""
    def move(*_): pass
import os.path

import pygame as pg

from .smr_error import SMRError
from .damagenumbers import DamageNumber


class Enemy:
    """base class for stickmanranger enemies"""
    id = 0
    health = 0
    damage_font = pg.font.Font(os.path.join('data', 'Roboto-Regular.ttf'), 9)
    damage_numbers = []
    dead = False
    # I dont know why the hell it needs to start at -3, not 0, but it does
    _enemies = -3
    in_damage_state = False
    pos = (0, 0)

    def __init__(self):
        Enemy._enemies += 1
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
        #print(self.damage_numbers)
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
                i = get_enemy_by_id(game_state['_STAGE_DATA']['enemies'], self.id)
                print('lol. enemy with id %s is now IN THE VOID.' % self.id)
                del game_state['_STAGE_DATA']['enemies'][i]
                self.dead = True


    def draw(*_):
        """to be overridden"""
        pass

    def move(*_):
        """to be overridden (unless stationary)"""
        pass

    def __repr__(self):
        return "{} enemy colour {} size {}".format(self.__class__.__name__, self.colour, self.size)


def get_enemy_by_id(enemies, id_):
    for i,e  in enumerate(enemies):
        print("%s with id %s. looking for %s" % (e, e.id, id_))
        if e.id == id_:
            return i

    raise SMRError('Enemy with id %d could not be found' % id_)

import pygame

try:
    from _internal import *
except ImportError:
    from ._internal import *

DEF_SIZE = 1


class EnemyHead:
    cached_colours = {}
    def __init__(self, type_str, colour, size=DEF_SIZE):
        print(size)
        self.type_str = type_str
        self.colour = colour
        self.size_px = size * 10
        img = PICS['heads'][type_str][colour].copy()
        self.head = pygame.transform.scale(img, (size * 10, size * 10))
        print({100: COLOURS[' '.join(('light', colour))]})
        change_alpha_to_colour(self.head, {100: COLOURS['light ' + colour]})
        self.name = colour + '_' + type_str
        self.pretty_name = ' '.join((colour, type_str)).title()

    def get_image(self, colour_override=None):
        if colour_override is None:
            return self.head

        # return a copy of the overridden image.
        pic = PICS['heads'][self.type_str][colour_override].copy()
        change_alpha_to_colour(pic, {100: COLOURS['light ' + colour_override]})
        pic = pygame.transform.scale(pic, (self.size_px, self.size_px))
        return pic


def main():
    import pygame
    image = pygame.image.load('happy.png')
    pygame.image.save(image, 'purplehappy.png')

if __name__ == '__main__':
    s = EnemyHead('happy', 'green')
    print(vars(s))
    import pygame
    pygame.image.save(s.head, 'C:\\Users\\Michael\\Desktop\\head.png')
    a = pygame.display.set_mode((1000, 1000))
    a.fill(COLOURS['white'])
    s.head.set_alpha(100)
    #change_alpha_to_colour(s.head, {100: (255, 0, 0)})
    a.blit(s.head, (0, 0))
    pygame.display.update()
    while True:
        for i in pygame.event.get():
            if i.type == 12:
                raise SystemExit

import threading
import os

import pygame as pg

try:
    from enemy_head import EnemyHead
    from sprite import SMRSprite
except ImportError:
    from .sprite import SMRSprite
    from .enemy_head import EnemyHead

FPS = 50
CLOCK = pg.time.Clock()


class EnemyImage(SMRSprite):
    def __init__(self, pos, size, colour, head_type, main_game_state,
                 event_queue):
        SMRSprite.__init__(self, main_game_state, event_queue, pos)
        head = EnemyHead(head_type, colour, size)
        head_rect = head.head.get_rect()
        body_size = self.get_body_size()
        head_width = head_rect.width
        head_height = head_rect.height
        body_width = body_size.width
        body_height = body_size.height
        print('!!!!!!!!', colour, head)
        print(locals())

        real_width = body_width if body_width > head_width else head_width
        real_height = body_height if body_height > head_width else head_width
        self.size = (real_width, real_height)
        self.update_coords(pos)
        self.head = head
        self.main_game_state = main_game_state
        self.event_queue = event_queue

    def move_to_x(self, pos, surf, pixels=1):
        current = self.topleft[0]
        dest = current - pixels if pos < current else current + pixels
        self.update_coords((dest, self.topleft[1]))
        self.draw(surf)

    def draw(self, surf):
        """
        since the basic class, just 
        blits the head to the screen.
        """

        surf.blit(self.head.head, self.topleft)

    def start_thread(self, surf, pos):
        self.mainthread = threading.Thread(
            target=self._mainloop,
            args=(surf, pos),
        )
        self.mainthread.start()

    def _mainloop(self, pos, surf):
        at_pos = False
        while True:
            if at_pos:
                continue

            self.move_to_x(pos, surf)

            if self.topleft == pos:
                at_pos = True

            CLOCK.tick(FPS)

    @staticmethod
    def get_body_size():
        return pg.Rect((0, 0), (0, 0))


if __name__ == '__main__':
    d = EnemyImage((0, 0), 2, 'green', 'happy', {}, {})
    s = pg.Surface((10, 10))
    s.fill((255, 255, 255))
    d.draw(s)
    pg.image.save(s, r'C:\Users\Michael\Desktop\s.png')

    s = pg.display.set_mode((500, 500))
    d.start_thread(10, s)

    while True:
        for e in pg.event.get():
            if e.type == 12:
                os._exit(0)
        pg.display.update()
        s.fill((0, 0, 0))
        CLOCK.tick(FPS)
"""
events.py
these are simple event classes for 
stickman's new world.
there are 2 ways to use these.
in main_event_queue or _internal_event_queue.
in _internal_event_queue it will act in the 
thread with that sprite, and in main_event_queue,
it will act in the main loop itself.
"""


class _Event:
    """
    base class for the other events.
    """

    def __init__(self, code=None, mode=exec):
        self.code = code

    def __call__(self):
        self._exec()

    def __repr__(self):
        return '%a object at %s' % (self.__class__, hex(id(self)))

    def _exec(self):
        """
        to be overridden.
        """
        if self.code is not None:
            self.mode(self.code)


class Quit(_Event):
    def __init__(self):
        Quit.code = compile('import os; os._exit(0)', 'Quit Event', 'exec')
        self.mode = exec


class Pause(_Event):
    keep = True


class SayHello(_Event):
    """
    test event.
    """

    def __init__(self):
        SayHello.code = compile('print("Hello!")', 'SayHello event', 'exec')
        self.mode = exec

    def _exec(self):
        self.mode(self.code)


# print(SayHello())

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
    from ._internal import PICS
    import class_.events as events

FPS = 50
CLOCK = pg.time.Clock()
COLOURS = {
    'beige': (242, 189, 107),
    'green': (0, 128, 0),
    'blue': (0, 0, 128),
    'red': (128, 0, 0),
    'dark red': (255, 0, 0),
    'dark blue': (0, 0, 255),
    'dark green': (0, 255, 0),
    'black': (0, 0, 0),
    'aqua': (0, 255, 255),
    'white': (255, 255, 255),
    'teal': (0, 128, 128),
    'purple': (128, 128, 0),
    'dark purple': (255, 255, 0),
    'yellow': (255, 255, 0),
    'silver': (192, 192, 192),
    'gold': (192, 192, 96),
    'gray': (211, 211, 211),
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

    def __init__(self,
        type_,
        weapon,
        pos: 'the topleft corner (in cartesian system)',
        main_game_state,
        event_queue):

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
        # skeleton for 2D-lsit (First time to actually get to use Ellipsis!)
        rarm = [[..., ...], [..., ...]]
        rarm[0][0] = self.topright[0] - (self.sizex // 2)
        # X- coordinate should be directly on arm
        rarm[0][1] = self.topright[1] - (self.sizey // 6 * 9)
        # 3 quarters up the arm should be good

        # exactly on edge of player's hitbox
        rarm[1][0] = self.topright[0]

        # randomly on the top half of hitbox
        rarm[1][1] = random.randint(
            self.topright[1] - (self.sizey // 2), self.topright[1])

        self.rarm_rect = pg.draw.line(
            surface, COLOURS['beige'], rarm[0], rarm[1])

        # larm is basically a repeat of rarm, only a few modifications
        larm = [[..., ...], [..., ...]]
        # same coordinate for part that attaches to body is OK
        larm[0] = rarm[0]
        larm[1][0] = self.topleft[0]
        larm[1][1] = random.randint(
            self.topleft[1] - (self.sizey // 2), self.topright[1])

        self.larm_rect = pg.draw.line(surface, COLOURS['beige'], *larm)

        body1 = self.topright[0] - self.sizex // 2
        body2 = self.topleft[1] - self.sizey
        start = body1, body2

        body1 = self.bottomright[0] - self.sizex // 2
        body2 = self.bottomright[1] - self.sizey
        end = body1, body2

        self.body = pg.draw.line(surface, COLOURS['beige'], start, end, 1)

        head_center_pos = self.topright[0] - \
            self.sizex // 2, self.topleft[1] - (self.sizey + 2)
        self.head = {'center': head_center_pos, 'radius': self.head_radius}
        self.head_rect = pg.draw.circle(
            surface, COLOURS['beige'], head_center_pos, self.head_radius, 1)

        rleg = [[..., ...], [..., ...]]
        rleg[0] = end
        rleg[1][0] = random.randint(
            self.bottomleft[0], self.sizex // 2 + self.bottomleft[0])
        rleg[1][1] = self.bottomleft[1]
        self.rleg = rleg

        self.rleg_rect = pg.draw.line(surface, COLOURS['beige'], *rleg)

        lleg = [[..., ...], [..., ...]]
        lleg[0] = end
        lleg[1][0] = random.randint(
            self.bottomright[0], self.sizex // 2 + self.bottomright[0])
        lleg[1][1] = self.bottomright[1]
        self.lleg = lleg
        self.lleg_rect = pg.draw.line(surface, COLOURS['beige'], *lleg)

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

    def _mainloop(self, pos, surface, pixels, invisible=False, *args, **kwargs):
        new_pos = [-1, -1]  # the coordinate can never be this
        at_pos = False
        # at pos will keep the main loop going

        while True:
            if not self._internal_events.empty():
                f = self._internal_events.get()
                f()

            coord, moved_to = self.move_to(pos, surface, pixels)
            if coord == 0: pass

    def start_thread(self, move_to, surf, terrain, pixels=1, daemon=False):
        self.mainproc = threading.Thread(
            target=self._mainloop, args=(
                move_to, surf, terrain, pixels), daemon=daemon
            )

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
    # d = CharacterImage('test', WeaponDummy(testsurf), (0, 0), {}, {})
    # d.start_thread((200, 100), a)
    print(CharacterImage.get_topleft_coord(
        t, *CharacterImage.find_closest_of(t, '*')))
    truecoord = CharacterImage.find_closest_of(
        t, '*')[0], CharacterImage.find_closest_of(t, '*')[1]
    print(CharacterImage.get_topleft_coord(t, *truecoord),
          CharacterImage.get_topleft_coord(t, *CharacterImage.find_closest_of(t, '*')))
    # s.start_thread(CharacterImage.get_topleft_coord(t, *CharacterImage.find_closest_of(t, '#')), a)
    # for i in range(100):
    #     i = CharacterImage('test', WeaponDummy(testsurf), (0,0), {}, {})
    #     i.start_thread((0, 0 ), a)
    pause = events.Pause()
    s = CharacterImage('test', WeaponDummy(testsurf),
                       CharacterImage.get_topleft_coord(t, *truecoord), {}, {})
    print(CharacterImage.get_topleft_coord(t, *truecoord))
    s.start_thread((800, a, t)

    while True:
        # a.blit(PICS['Maps']['army'], CharacterImage.get_topleft_coord(t, *CharacterImage.find_closest_of(t, '*')))
        # s.build_image(a)
        for i in pg.event.get():
            if i.type == QUIT:
                print('hello?')
                # cleanup and saving and stuff like that can go here, but for now time.sleep tests it.
                # always remove the pause from _internal_events before putting Quit
                os._exit(0)


                # import time; time.sleep(1)




        try:
            pg.display.update()
            a.fill(COLOURS['black'])
            a.blit(t_surf, (0, 0))
        except pg.error:
            # os._exit is about to be called in a seperate thread
            pass


        print('updated')
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
from pprint import pprint

import pygame as pg

try:
    from _internal import COLOURS
except ImportError:
    from ._internal import COLOURS


LARGEICONSIZE = 10

class InventoryHandler:
    def __init__(self, sizex, sizey):
        self.datas = [[None for i in range(sizey)] for i in range(sizex)]
        #print(self.datas)

        #print(self.datas)

    def sort_dict(self, dictionary):
        """
        sorts dictionary shaped like: {'1x2': whatever} and puts it into 
        the internal 2d list.
        """
        #print(self.datas)
        for indexes in sorted(dictionary):
            x = int(indexes.split('x')[0])
            y = int(indexes.split('x')[1])
            # print(x, y)
            # print("self.datas[{}][{}] = dictionary['{}']".format(
            #     x - 1, y - 1, indexes))
            self.datas[x - 1][y - 1] = dictionary[indexes]
            #print(self.datas)

    def build(self, surf=None, topright=(0, 0), gap=7, bgcolour=COLOURS['black'], padding=2):
        """
        creates the surface of the inventory image
        :param surf: pass a surface if you want the image to be appended to the surface
        :param topright:the topright corner for the blitting to start
        :param gap: gap between blocks
        :param bgcolour: the background colour of the blocks
        :param padding: the padding on the edge of the surface
        :return: the new/appended surface
        """
        lengthx, lengthy = 0, 0
        blacksurf = pg.Surface((LARGEICONSIZE, LARGEICONSIZE))
        blacksurf.fill(bgcolour)

        # need to calculate dimensions of surface

        lenarry = len(self.datas)
        lenarrx = len(self.datas[0])    # length of the first element == all the others

        for i in range(lenarrx):
            lengthx += (gap + LARGEICONSIZE)
        lengthx += (padding * 2)   # the padding must be multiplied by 2, for both sides
        lengthx -= (LARGEICONSIZE - (padding + 1))

        for i in range(lenarry):
            lengthy += (gap + LARGEICONSIZE)
        lengthy += (padding * 2)
        lengthy -= (LARGEICONSIZE - (padding + 1))

        if surf is None:
            surf = pg.Surface((lengthx, lengthy))
            surf.fill((255, 255, 255))

        where_to_blit = list(map(lambda x: padding + x, topright))

        for x in range(lenarry):
            for i in range(lenarrx):
                # print('where to blit:', where_to_blit)
                surf.blit(blacksurf, where_to_blit)
                where_to_blit[0] += (LARGEICONSIZE + gap)
            where_to_blit[0] = (padding + topright[0])    # reset X coordinates
            where_to_blit[1] += (LARGEICONSIZE + gap)

        return surf



if __name__ == '__main__':
    a = InventoryHandler(2, 3)
    s = {
        '1x1': '0',
        '1x2': '1',
        '1x3': '2',
        '2x1': '3',
        '2x2': '4',
        '2x3': '5',
    }
    a.sort_dict(s)
    # pprint(a.datas)
    pg.image.save(a.build(), r'C:\Users\Michael\Desktop\image.png')
from bs4 import BeautifulSoup
from urllib.request import urlopen
import random


class Joker:
    def __init__(self):
        parser = BeautifulSoup(
            urlopen('https://michael78912.github.io/puns.html'), 'lxml')
        self.division = parser.p.get_text().split('\n')[2:-1]
        self.joke = random.choice(self.division).strip()

    def say_joke(self):
        print(self.joke)

    def new_joke(self):
        self.joke = random.choice(self.division)


print(Joker().joke)
"""klass.py (I know it's spelt wrong, OK)?
base class for all character classes in SMNW. handles 
image generation, spawning, and default movement, and attacking.
"""
import random

from . import terrain
from .character_image import CharacterImage
from .smr_error import SMRError


BEIGE = (232, 202, 145)




class Class:
    """
    base class for stickman ranger classes.
    """

    # I, personally think that a character class in a reasonably large
    # game should be allowed to have at least a few more attributes than
    # seven. I am so, so, sorry if you hate me, pylint.
    # and too many arguments to __init__? whats that about?

    # pylint: disable=too-many-instance-attributes, too-many-arguments

    attack_radius = 0
    chance_of_motion = 4
    max_motion = 3
    jump_height = 10
    _chance_of_update = 2

    def __init__(
            self,
            type_,
            player_num,
            weapon,
            main_game_state,
            stats=(50, 0, 0, 0, 0),
            spec=None,
    ):

        # the following two lines of code may seem redundant, but for a reason.
        try:
            self.health, self.str_, self.dex, self.mag, self.spd = stats
        except ValueError:
            raise SMRError('invalid length of tuple "stat" argument')
        self.stats = stats
        self.player_num = player_num
        self.weapon = weapon
        self.image = CharacterImage(
            type_, weapon, (0, 0), main_game_state)
        self.type_ = type_
        self.spec = spec

    def __repr__(self):
        return """character number {} type {}""".format(self.player_num, self.type_)

    def hit(self, damage):
        'takes damage by specified amount'
        self.health -= damage

    def heal(self, damage):
        'heals by specified amount'
        self.health += damage

    def level_up(self, *args):
        'raises characters stats by specified amount'
        assert len(args) > 6, 'Too many stats to raise'
        if self.spec is None:
            if not None in args:
                self.spec = args[-1]
            else:
                raise TypeError(
                    'Cannot assign a special value to class, cannot support special value.'
                )
        # add stats
        for index in enumerate(args):
            self.stats[index] += args[index]

    def spawn_on_screen(self, game_state):
        """adds the character to the screen, the very beginning,
        on the top, but not above or underground.
        """
        # surface.blit(self.image, surface.terrain.array[0])

        display = game_state['MAIN_DISPLAY_SURF']

        x = 15    # we always want to spawn characters at x=15.

        y = game_state['_STAGE_DATA']['stage'].terrain.get_spawn_point(x, self.image.sizey)
        self.image.update_coords((x, y))
        self.image.build_image(display, BEIGE)

    def update(self, game_state):
        """attempt to move, and attack."""
        terrain_obj = game_state['_STAGE_DATA']['stage'].terrain
        self.weapon.update()

        current_block_x = terrain_obj.px_to_blocks(self.image.topleft[0])
        current_block_y = terrain_obj.px_to_blocks(self.image.topleft[1])
        next_column = list(
            terrain_obj.terrain2dlist_texts[terrain_obj.template]['text'][:, current_block_x + 1])
        top_levels = {i if obj == '*' else None for i,
                      obj in enumerate(next_column)}
        top_levels.remove(None)

        #underground = terrain.is_underground(self.image.topleft, terrain_obj, self.image.sizey - 3)
        can_move = True

        # if underground:
        #     print(self, "is underground!")
        #     self.image.update_coords((self.image.x, self.image.y - 1))

        if top_levels:
            # Umm, there is nowhere to go. whoever made this terrain file is
            # a complte asshole, doing this to these poor characters. :(
            print(Warning('there is no top level terrain for the character to go'))

        else:
            # get how far they would have to move.

            distance = terrain_obj.blocks_to_px(
                min([current_block_y - i for i in top_levels]) + 1)

            print('has to climb %d pixels' % distance)
            if 0 < distance <= self.jump_height:
                print('howdy. jumping...')
                # 10 pixels is the maximum a player can climb, without any sort of tool.
                self.image.update_coords((self.image.x, self.image.y - 12))

            elif distance > self.jump_height:
                # can not jump, and can not move. stay still.
                print('cannot move')
                can_move = False

        in_air = terrain.is_in_air(self.image.topleft, terrain_obj, 5)
        if in_air:
            self.image.update_coords(
                (self.image.topleft[0], self.image.topleft[1] + 1))
            print(self, "needs to fall")

        try:
            motion_target = get_closest_enemy(
                game_state, self.image.topright[0])
        except ValueError:
            # no more enemies remaining, `min` will raise a ValueError.
            return
        target_x = motion_target.pos[0]

        x = self.image.topright[0]

        distance = target_x - x if target_x >= x else x - target_x

        if distance <= self.weapon.range:
            # self.weapon.attack_enemy(motion_target)
            self.attack(motion_target)
        print(((self.image.topright[0] - target_x) if self.image.topright[0] > target_x else (target_x - self.image.topright[0])))

        can_move = random.randint(0, self.chance_of_motion) == 1 and can_move
        # can_move = can_move and ((self.image.topright[0] - target_x) if self.image.topright[0] > target_x else (target_x - self.image.topright[0]))
        can_move = can_move and distance >= self.weapon.range

        if can_move:
            print(self, "moving...")

            self.image.move_to_x(self.image.topright[0] + self.max_motion,
                                 game_state['MAIN_DISPLAY_SURF'],
                                 pixels=random.randint(1, self.max_motion))

        if game_state['MOUSEDOWN']:
            if self.image.rect.collidepoint(game_state['MOUSE_POS']):
                self.image.update_coords(game_state['MOUSE_POS'])

        # game_state['MAIN_DISPLAY_SURF'].blit(self.picture, self.image.topright)

        update = random.randint(0, self._chance_of_update) == 1
        if distance <= self.weapon.range:
            update = False

        if not self.image.has_drawn:
            #  needs to draw at least once. override.
            update = True

        self.image.build_image(
            game_state['MAIN_DISPLAY_SURF'], BEIGE, rebuild=update)

    def attack(self, target):
        """attack the target enemy."""
        if self.weapon.can_attack():
            self.weapon.attack_enemy(target)


def get_closest_enemy(game_state, pos):
    """get and return the closest enemy to pos."""
    possible_destinations = [enemy.pos[0]
                             for enemy in game_state['_STAGE_DATA']['enemies']]
    print(possible_destinations)

    distances = [pos - i if i <= pos else i -
                 pos for i in possible_destinations]

    distance = min(distances)

    return game_state['_STAGE_DATA']['enemies'][distances.index(distance)]
try:
    from _internal import *
    from smr_error import SMRError
except ImportError:
    from ._internal import *
    from .smr_error import SMRError
import pygame as pg
col = COLOURS


class MyRect(pg.Rect):
    """this class is simply for keeping track of 
    when boxes are shaded"""
    shaded = False
    _accumval = 0
    underlined = False
    PicInside = None
    PicReprInside = ''

    def __init__(self, *args, colour=col['white']):
        pg.Rect.__init__(self, *args)
        self.colour = colour


    def shade(self, Surface, Colour='gray'):
        #if not self.Shaded:
        if type(Colour) not in (str, tuple, list):
            raise TypeError(
                'Colour argument must be string or RGB sequence.')

        if type(Colour) == str:
            try:
                Colour = col[Colour]  # convert the string to RGB tuple
            except KeyError:
                raise Exception(
                    'The Colour {} could not be found. please specify an RGB tuple instead'.
                    format(Colour))


        new_surf = pg.Surface((self.width, self.height))
        new_surf.set_alpha(75)
        new_surf.fill(Colour)
        Surface.blit(new_surf, (self.x, self.y))

        #else:
        #    raise SMRError('The Box is already shaded')

    def unshade(self, Surface, OrigSurf):
        """
        practically the opposite of shade.
        unshades the box, which is crucial.
        """
        #if self.Shaded:
        self.Shaded = False
        filler = (255, 255, 255)
        new_surf = pg.Surface((self.width, self.height))
        new_surf.fill(filler)
        Surface.blit(new_surf, (self.x, self.y))
        Surface.blit(OrigSurf, (self.x, self.y))
        #else:
            #raise SMRError('you cannot unshade an unshaded box!')

    def draw(self, surface):
        if self.shaded:
            self.shade(surface)



    def handle(self, event, Surface, OrigSurf, colour='gray'):
        """
        handles an event. chooses to unshade if criteria is met, an all-in-one
        function.
        """
        x, y = event.pos

        if self.collidepoint(x, y) and not self.Shaded:
            self.shade(Surface, colour)
        elif not self.collidepoint(x, y) and self.Shaded:
            self.unshade(Surface, OrigSurf)

    def underline(self, Surface, colour='black'):
        """
        similar to shade, but instead of shading, it
        will underline the rect.
        """
        if self.underlined:  # make sure you are not underling the rect again
            raise SMRError('the rect is already underlined')

        if type(colour) == str:  # same as before
            try:
                Colour = col[colour]  # convert the string to RGB tuple

            except KeyError:
                raise Exception(
                    'The Colour {} could not be found. please specify an RGB tuple instead'.
                    format(Colour))

        self.underlined = True
        pg.draw.line(Surface, Colour, self.bottomright, self.bottomleft)

    def remove_underline(self, Surface):
        """
        appears to remove underline
        by just drawing a blank 
        line over it.
        """
        if not self.underlined:
            raise SMRError('the box is not underlined')

        pg.draw.line(Surface, (255, ) * 3, self.bottomright, self.bottomleft)
        self.underlined = False

    def draw_inside(self, pic, surf):
        """
        draws a picture inside of self.
        sets 2 properties, PicReprInside = repr(pic)
        and PicInside = pic.
        """
        if self.PicReprInside:
            raise SMRError('there is already a picture in this box.')

        _Box((self.width, self.height), self.colour, (self.x, self.y), surf,
             255, pic)
        self.PicReprInside = repr(pic)
        self.PicInside = pic

    def remove_pic(self, surf):
        """
        removes the picture from inside self.
        """
        _Box((self.width, self.height), self.colour, (self.x, self.y), surf)
        self.PicInside = None
        self.PicReprInside = ''


def _Box(size, colour, pos, surface, alpha=None, image=None) -> tuple:
    """
    return a square rectangle, surface pair
    uses MyRect
    """
    print(pos)
    new_surf = pg.surface.Surface(size)
    new_surf.fill(colour)

    if alpha is not None:
        new_surf.set_alpha(alpha)

    surface.blit(new_surf, pos)

    if image is not None:
        surface.blit(image, pos)

    return MyRect(new_surf.get_rect(topleft=pos)), new_surf
import numpy
import timeit

print('hi')

timeit.timeit('''
big_list = [['hi'] * 1000] * 1000
for i in big_list:
    for s in i:
        pass''')
print(time.time(), 'after loops')
"""
progress_bar.py
contains one class, ProgressBar, that is basically,
just a progress bar!"""

import pygame
import math


class ProgressBar:
    """
    makes a progress bar
    example:

    a = ProgressBar(3, (0, 0), (50, 20))
    a.draw(display)
    # makes a 50x20 gray bar in top right corner
    a.increment(1)
    # put it forward once
    """

    def __init__(self, increments_to_full, pos, width, height, alpha=200, righttoleft=True, colour=(211, 211, 211)):
        self.increments_to_full = increments_to_full
        self.pos = pos
        self.width = width
        self.height = height
        self.colour = colour
        self.righttoleft = righttoleft
        self.full = 0

        self.first_surf = pygame.surface.Surface((width, height))
        self.first_surf.set_alpha(alpha)
        self.first_surf.fill(colour)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __gt__(self, other):
        return self.increments_to_full > other.increments_to_full

    def __lt__(self, other):
        return self.increments_to_full < other.increments_to_full

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def draw(self, surface):
        surface.blit(self.first_surf, self.pos)


    def increment(self, surface, increment, auto_update=True):
        """
        increment the progress bar by increment.
        """
        increment_size = (self.width // increment, self.height)
        self.full += increment_size

        if self.increments_to_full - self.full < increment_size[0]:
            self.first_surf = pygame.surface.Surface((self))
            self.
import pygame as pg

try:
    from _internal import PICS
    from sprite import SMRSprite
except ImportError:
    from .sprite import SMRSprite
    from ._internal import PICS

class Projectile(SMRSprite):
    """
    Projectile, is as expected a projectile.
    It is used as a subclass for other types of projectiles.
    """

    def __init__(self, img, motion, colour, pos, main_game_state):
        SMRSprite.__init__(self, main_game_state, None, pos)
        self.img = PICS['Attacks'][img][colour]
        self.motion = motion



    def get_path(self, target, set_property=True):
        if self.motion == ARC:
            path = self.get_parabola(target)
        elif self.motion == STRAIGHT:
            raise NotImplementedError('the method is not implemented')
            # path = self.get_straight_path(target)
        else:
            raise TypeError('%s is not a valid motion argument' % self.motion)

        if set_property:
            self.path = path

        return path

    def get_straight_path(self, target):
        """
        returns a list of a line, similar to 
        get_parabola, but a straight line.
        """
        x1, x2 = self.topleft
        y1, y2 = target
        m = (y2 - y1) / (x - x1)
        

    def get_parabola(self, target):
        """
        finds and returns a parabola,
        in the form of a path, for the projectile to 
        move along.
        """

        pt2 = tarx, tary = target
        pt1 = charx, chary = self.topleft

        array = []
        i = charx

        while i <= 610 and i >= -1000:
            array.append((i, round((chary - tary) / ((charx-tarx)*(charx-tarx)) * pow((i - tarx), 2) + tary)))
            if tarx >= charx:
                i += 1
            else:
                i -= 1

        return array



STRAIGHT = 0
ARC = 1
import random
import copy


class Screen:
    firstrun = True
    """Screen is a piece of a stage.
    each stage can have any number of screens, and must have
    a boss screen.
    all_enemies is a dictionary, with keys of enemies, and values of 
    the amount that enemy shoud spawn. ex:

    {
        SomeEnemy('blue', blablabla, 88): 10
    }

    will spawn 10 of SomeEnemy in this screen.
    """

    def __init__(
            self,
            all_enemies,
            spawn_mode='random',
            # must put Y coordinate for each enemy to spawn
    ):

        # assert len(
        #     all_enemies) == len(num_of_enemies_per_enemy
        #                         ), "the enemies and quantities do not match"

        # self.all_enemies = all_enemies
        # self.num_of_enemies_per_enemy = num_of_enemies_per_enemy

        # if spawn_mode == 'random':
        #     new_spawn_mode = []

        #     for enemy, quantity in zip(all_enemies, num_of_enemies_per_enemy):
        #         for i in range(quantity):
        #             new_spawn_mode.append((0 if enemy.area == 'ground' else
        #                                    random.randint(1, 600), random.randint(1, 600)))
        #     self.spawn_mode = new_spawn_mode

        # else:
        #     self.spawn_mode = spawn_mode

        self.total_enemies = sum(all_enemies.values())
        self.enemies = []

        for i in all_enemies:
            self.enemies += [copy.copy(i) for x in range(all_enemies[i])]

        if spawn_mode == 'random':
            self.spawn_mode = [random.randint(1, 800) \
                               for i in range(self.total_enemies)
                              ]

        else:
            self.spawn_mode = spawn_mode

    def draw(self, game_state):
        """draw enemies on screen."""
        terrain = game_state['_STAGE_DATA']['stage'].terrain

        if self.firstrun:
            game_state['_STAGE_DATA']['enemies'] = []
            for enemy, x in zip(self.enemies, self.spawn_mode):
                ground_level = terrain.get_spawn_point(x, terrain.blocks_to_px(enemy.size))
                enemy.draw((x, ground_level), game_state['MAIN_DISPLAY_SURF'])
                game_state['_STAGE_DATA']['enemies'].append(enemy)

            for player in game_state['PLAYERS']:
                player.spawn_on_screen(game_state)

            self.firstrun = False

        else:
            for enemy in self.enemies:
                enemy.move(game_state["PLAYERS"], game_state["MAIN_DISPLAY_SURF"], game_state['_STAGE_DATA']['stage'].terrain)
                enemy.update(game_state)
            for player in game_state['PLAYERS']:
                player.update(game_state)



class PeacefulScreen(Screen):

    def __init__(self):
        super().__init__((), (), None)
from distutils.core import setup
import py2exe

setup(console=['terrain.py'])
"""smr_error.py- base class for 
stickmanranger errors.
"""


class SMRError(Exception):
    """
    base class for stickmanranger errors
    """
    pass
"""
this is the base class for basically anything
that moves in this game.
"""
__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
__version__ = '0.0'

from queue import Queue
import pprint
import threading

import pygame as pg

try:
    from events import Quit, SayHello
    from terrain import Terrain

except ImportError:
    from .events import Quit, SayHello
    from .terrain import Terrain


class SMRSprite:
    sizey = 0
    sizex = 0
    """
    this is the base class for everything that can move 
    in this game. enemies, attacks, weapons, and projectiles.
    _mainloop does nothing in this base class, it is just there
    because it is called by start_thread.
    """

    def __init__(self, main_game_state, event_queue, pos):
        self.main_game_state = main_game_state
        self.event_queue = event_queue
        self._internal_events = Queue()

        self.topleft = pos
        self.bottomleft = pos[0], pos[1] + self.sizey
        self.topright = pos[0] + self.sizex, pos[1]
        self.bottomright = pos[0] + self.sizex, pos[1] + self.sizey

    def internal_event(self, ev):
        self._internal_events.put(ev)

    @staticmethod
    def find_closest_of(terrain, block, x=0):
        """
        finds the first solid part of terrain, and returns the
        index as a tuple.
        """

        terrain2d = terrain.terrain2dlist_texts[terrain.template]['text']
        if terrain.use_numpy:
            line = terrain2d[:, x]

        else:
            line = [i[0] for i in terrain2d]
        # print(line)

        for iblock, index in zip(line, range(len(line))):
            # this is going the correct way, I believe
            # print(line, block)
            if iblock == block:
                return x, index

        else:
            raise TypeError('there are no %a symbols in %a' % (block, line))

    @classmethod
    def get_topleft_coord(cls, terrain, x, y):
        """
        returns the correct coordinate 
        from terrain, in pixels, rather than blocks.
        """
        template = terrain.terrain2dlist_texts[terrain.template]
        blk_size = template['size']
        x_line_size_pixels = len(
            template['text'][:, x]) * blk_size if terrain.use_numpy else len(
                [i[0] for i in template['text']]) * blk_size
        y_line_size_pixels = len(template['text'][0]) * blk_size
        new_x = x * blk_size
        new_y = y * blk_size
        assert new_x < x_line_size_pixels and new_y < y_line_size_pixels, 'the coordinate is too big for the screen'
        return (new_x - cls.sizex, new_y - cls.sizey)
        # this is all correct so far

    def update_coords(self, pos):
        self.topleft = pos
        self.x, self.y = pos
        self.bottomleft = pos[0], pos[1] + self.sizey
        self.topright = pos[0] + self.sizex, pos[1]
        self.bottomright = pos[0] + self.sizex, pos[1] + self.sizey

    def game_quit(self):
        """
        request a quit from the actual game, if needed.
        """

        self.event_queue.put(Quit())

    def kill_thread(self):
        """
        attempts to kill the current thread, with 
        cleanup (removes character from screen, etc...)
        """
        self._internal_events.put(Quit())

    def start_thread(self, daemon=True):
        """
        starts a new thread and redirects it to _mainloop.
        daemon is default to true.
        """
        self.mainthread = threading.Thread(
            target=self._mainloop, daemon=daemon)
        self.mainthread.start()

    def _mainloop(self):
        while 1:
            if self._internal_events.empty():
                pass
            else:
                self._internal_events.get()()

            # used for debugging
            print(threading.current_thread())


if __name__ == '__main__':
    d = Terrain('dirt', 'test', use_numpy=True)
    # print([i.tolist() for i in d.terrain2dlist_texts['test']['text']])
    s1, s2 = SMRSprite.find_closest_of(d, '#')
    print(s1, s2)

    # print(s1, s2)
    # s = repr(list([list(i) for i in d.terrain2dlist_texts[d.template]['text']]))
    # a = list([list(i) for i in d.terrain2dlist_texts[d.template]['text']])
    # print(a)
    print(SMRSprite.get_topleft_coord(d, s1, s2))
from threading import Thread

from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN
import pygame as pg
import os


WHITE = (255, 255, 255)  # unbeaten
GRAY = (211, 211, 211)  # beaten
TEAL = (0, 128, 128)  # peaceful
YELLOW = (128, 128, 0)
BLACK = (0, 0, 0)
STAGE_SIZE = (15, 15)


class Stage:
    unlocked = False
    beaten = False
    rect_padding = 8
    game_state = {}

    def __init__(
            self,
            name,
            # name to be used by the game
            position_on_map,
            # (x, y) cartesian system
            all_screens,
            # list\tuple of all screens in stage
            boss_screen,
            # the screen of the boss
            terrain,
            # the terrain class
            comes_from,
            # stage that you beat to unlock it (first level is None, shouldn't
            # ned to put None again)
            surface,
            # map that the stage must be drawn on
            peaceful=False,
            # peaceful stage is a shop or of the like
            has_icon=True,
            # False if level shows upon map already, or is secret
            links_to=None,
            # list\tuple of all stages it links to,
            decorations=(),
            # tuple of decorations to be drawn
    ):
        if comes_from is None:
            comes_from = _NullStage

        self.position_on_map = position_on_map
        self.all_screens = all_screens
        self.comes_from = comes_from
        self.drawing_surface = surface
        self.peaceful = peaceful
        self.has_icon = has_icon
        self.links_to = links_to
        self.name = name
        self.terrain = terrain
        self.decorations = decorations
        # print(os.getcwd())
        with open(os.path.join(
            os.getcwd(), 'music', 'smnwgameplay.mp3'
        )):
            print('opened successfully')

        self.music = os.path.join('music', 'smnwgameplay.mp3')

        self.rect = pg.Rect(position_on_map, STAGE_SIZE)

        rect = self.rect
        left, top, width, height = rect.left, rect.top, rect.width, rect.height
        self.box = pg.Rect(left - self.rect_padding, top - self.rect_padding,
                width + (self.rect_padding * 2), height + (self.rect_padding * 2)
            )

    def draw_on_map(self):
        surface = self.drawing_surface

        if self.comes_from.beaten and self.has_icon:
            self.rect = pg.draw.rect(
                surface, WHITE, self.position_on_map + STAGE_SIZE)

        elif self.beaten and self.has_icon:
            self.rect = pg.draw.rect(
                surface, GRAY, self.position_on_map + STAGE_SIZE)

        if self.peaceful and self.has_icon:
            self.rect = pg.draw.rect(
                surface, TEAL, self.position_on_map + STAGE_SIZE)

    def check_hover(self, pos):
        """check to see if the mouse is hovering over. if it is,
        dislpay a box around the level, and a name.
        """

        # print(left, top, width, height)

        if self.box.collidepoint(*pos):
            box = self.box
            pg.draw.rect(self.drawing_surface, YELLOW, box, 1)

            fontobj = pg.font.Font(os.path.join('data', 'MICHAEL`S FONT.ttf'), 20)
            fontobj.set_bold(True)
            surf = fontobj.render(self.name, True, BLACK)
            surfrect = surf.get_rect()
            surfrect.center = pos[0], pos[1] - 40

            self.drawing_surface.blit(surf, surfrect)


     

    def start_music(self):
        """stop old music, play new music."""
        if not self.peaceful:
            # keep the theme music if it is a peaceful screen.
            pg.mixer.music.fadeout(2000)
            print('howdy?')
            pg.mixer.music.load(self.music)
            pg.mixer.music.play(-1)

    def init(self, game_state):
        """run the stage."""
        self.game_state = game_state
        Thread(target=self.start_music).start()
        game_state['_STAGE_DATA'] = {
            'screen_number': 0,
            'screen': self.all_screens[0],
            'stage': self,
        }

    def update(self, events):
        """update the stage, and everything related to it."""
        state = self.game_state

        terrain_surf = self.terrain.build_surface()

        display = state['MAIN_DISPLAY_SURF']

        display.fill((0, 0, 0))

        current_screen = self.all_screens[state['_STAGE_DATA']['screen_number']]

        display.blit(terrain_surf, (0, 0))

        current_screen.draw(state)

        letters = []

        for event in events:
            check_quit(event)

            if event.type == MOUSEBUTTONDOWN:
                state['MOUSEDOWN'] = True

            elif event.type == MOUSEMOTION:
                state['MOUSEDOWN'] = False

            elif event.type == KEYDOWN:
                letters.append(event.unicode)
        
        if letters:
            pass

        if '~' in letters:
            print('open terminal...')




def check_quit(event):
    """check if event is a quit event. if it is, quit."""
    if event.type == QUIT:
        pg.quit()
        raise SystemExit



class _NullStage(Stage):

    def __init__(self):
        pass
    position_on_map = None
    all_screens = None
    comes_from = None
    drawing_surface = None
    peaceful = None
    has_icon = None
    links_to = None
    beaten = True

# d = pg.Surface((100, 100))
# d.fill((255, 255, 255))
# s = Stage(
#     "Test Stage 0.0",
#     position_on_map=(18, 569),
#     all_screens=[PeacefulScreen],
#     boss_screen=None,
#     surface=d,
#     terrain=Terrain('dirt', 'flat'),
#     comes_from=None,
#     peaceful=True,
# )
# s.draw_on_map()
# s.check_hover((100, 100))

# pg.image.save(d, r'C:\Users\Michael\Desktop\test_images\howdy.png')
try:
    from _internal import *

except ImportError:
    from ._internal import *


class StatusAilment:
    def __init__(self, colour):
        self.colour = colour

"""terrain.py
takes all terrain files (terrain/*) and converts them
into stickmanranger terrain objects.
NOTE: may want to run this code in a background thread,
as it will probably take a while and cause graphics
to crash.
"""
__author__ = 'Michael Gill'
__version__ = '0.0'

from pprint import pprint
import os
import sys

from pygame.surface import Surface
from pygame.transform import scale
from pygame.locals import QUIT
import numpy

try:
    from _internal import *
    from smr_error import SMRError
except ImportError:
    from ._internal import *
    from .smr_error import SMRError


VALID_COMMANDS = ('air', 'water', 'size')


# there once was a fellow named finn
# who threw all his legs in a bin
# he realized, at last
# he could not move so fast
# and punched himself right in the chin.


class Terrain:
    top_water = PICS['Other']['top_water']

    surface_symbol = '*'
    ground_symbol = '#'
    water_symbol = '-'
    air_symbol = '~'
    sign_symbol = '^'
    pit_symbol = '_'
    top_water_symbol = '+'

    # alpha values. can be overriden with headers. (see flat.smr-terrain)
    air = 200
    water = 100

    def_air = (0, 0, 0, 200)
    def_water = (0, 50, 200, 100)

    def __init__(self, image, template='flat', block_size=10, use_numpy=True):

        self.image1 = PICS['terrain_templates'][image]['1']
        self.image2 = PICS['terrain_templates'][image]['0']
        self.template = template
        self.size = block_size
        self.use_numpy = use_numpy

        try:
            Terrain.terrain2dlist_texts

        except AttributeError:
            self.load_text()

    def __iter__(self):
        for i in self.terrain2dlist:
            yield i

    def __getitem__(self, pos):
        arr = self.terrain2dlist_texts[self.template]['text']
        return arr[pos[1]][pos[0]]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_solid(self, pos):
        """return true if the block at pos is solid."""
        return self.is_solid(self[pos])

    @staticmethod
    def is_solid(item):
        return item in (Terrain.ground_symbol, Terrain.surface_symbol)

    @staticmethod
    def is_water(item):
        return item in (Terrain.water_symbol, Terrain.top_water_symbol)

    @staticmethod
    def is_pit(item):
        return item == Terrain.pit_symbol

    @staticmethod
    def is_air(item):
        return item == Terrain.air_symbol

    def load_text(self):

        try:
            Terrain.terrain2dlist_texts
        except AttributeError:
            Terrain.terrain2dlist_texts = {}

        all_texts = Terrain.terrain2dlist_texts

        terrain_texts = {}
        terrain2dlist_texts = {}

        for text in os.listdir(TDIR):
            a = text.split('.')[0]
            terrain_texts[a] = open(os.path.join(TDIR, text)).read()

        for terrain, key in zip(terrain_texts.values(), terrain_texts.keys()):
            main_dict = {
                'size': self.size,
                'air': self.def_air,
                'water': self.def_water
            }
            if terrain.startswith('@'):
                # remove @ symbol
                header = terrain.split('\n')[0][1:]
                terrain = '\n'.join(terrain.split('\n')[1:])

                header = header.split('|')

                # remove all whitespace

                header = [part.strip().replace((' '), '')
                          .replace('\n', '')
                          .replace('\r', '')
                          .replace('\t', '')
                          for part in header]

                for command in header:
                    parts = command.split('=')
                    print
                    if not parts[0] in ('air', 'water', 'size'):
                        raise SyntaxError(
                            '%a is not a valid command for header' % parts[0])
                    else:
                        main_dict[parts[0]] = eval(parts[1])

            lines = []
            for line in terrain.split('\n'):
                if ';' in line:
                    line = line.split(';')[0].strip()
                # dont append blank lines!
                if line != '':
                    lines.append(line)

            terrain2dlist = []
            for line in lines:
                chars = []
                for char in line:
                    chars.append(char)
                terrain2dlist.append(chars if not self.use_numpy
                                     else numpy.array(chars))

            main_dict['text'] = terrain2dlist if not self.use_numpy \
                else numpy.array(terrain2dlist)

            terrain2dlist_texts[key] = main_dict

        Terrain.terrain2dlist_texts = terrain2dlist_texts

    def build_surface(self, override=None, display=None):
        """
                builds the terrain image and returns it.
                also sets self.built_image to the surface.
                """

        pit_picture = PICS['Other']['pit']
        sign_picture = PICS['Other']['next']

        # the surface everything will be added to
        big_actual_picture = Surface((800, 400))
        if getattr(self, 'decorations', False):
            self.decorations[0].draw_all()

        # find the 2D list of the specified terrain
        template = self.terrain2dlist_texts[self.template]
        scale(self.image1, (self.size, ) * 2)
        scale(self.image2, (self.size, ) * 2)
        if template['size'] is not None:
            self.size = template['size']

        text = template['text']

        air_picture = Surface((self.size, ) * 2)
        air_picture.fill(template['air'])

        water_picture = Surface((self.size, ) * 2)
        water_picture.fill(template['water'])

        top_water_picture = self.top_water
        _change_colour_surface(top_water_picture, *template['water'][:3])
        try:
            top_water_picture.set_alpha(template['water'][3])

        except IndexError:
            # no alpha has been set
            print('no alpha set')

        for line, index1 in zip(text, range(len(text))):
            for block, index2 in zip(line, range(len(line))):
                # print(block)
                if block == self.ground_symbol:
                    big_actual_picture.blit(
                        self.image1, (index2 * self.size, index1 * self.size))

                elif block == self.surface_symbol:
                    big_actual_picture.blit(
                        air_picture, (index2 * self.size, index1 * self.size))
                    big_actual_picture.blit(
                        self.image2, (index2 * self.size, index1 * self.size))

                elif block == self.air_symbol:
                    big_actual_picture.blit(
                        air_picture, (index2 * self.size, index1 * self.size))

                elif block == self.water_symbol:
                    big_actual_picture.blit(
                        water_picture,
                        (index2 * self.size, index1 * self.size))

                elif block == self.pit_symbol:
                    big_actual_picture.blit(
                        air_picture, (index2 * self.size, index1 * self.size))

                    big_actual_picture.blit(
                        pit_picture, (index2 * self.size, index1 * self.size))

                elif block == self.top_water_symbol:
                    big_actual_picture.blit(
                        air_picture, (index2 * self.size, index1 * self.size))

                    big_actual_picture.blit(
                        top_water_picture,
                        # sign is 30x30 pixels
                        (index2 * self.size, index1 * self.size))

                elif block == self.sign_symbol:
                    big_actual_picture.blit(
                        air_picture, (index2 * self.size, index1 * self.size))

                    big_actual_picture.blit(
                        sign_picture,
                        # sign is 30x30 pixels
                        (index2 * self.size - 20, index1 * self.size - 17))

        self.built_image = big_actual_picture
        scale(big_actual_picture, (800, 400))
        return big_actual_picture

    def save(self, filename):
        if not self.use_numpy:
            raise SMRError('numpy is not in use, no files can be saved')

        self.terrain2dlist_texts[self.template].dump(filename)

    @classmethod
    def save_all(cls, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)
        for file in cls.terrain2dlist_texts:
            cls.terrain2dlist_texts[file]['text'].dump(os.path.join(directory, file + '.bin'))

    def get_last_unsolid(self, x):
        """get the index of the bottommost air or water block."""
        arr = list(self.terrain2dlist_texts[self.template]['text'][:, x - 1])
        arr.reverse()

        not_solid = ['+', '-', '~']

        indices = [arr.index(i) if i in arr else 0 for i in not_solid]

        bottom = len(arr) - min(filter(None, indices)) - 1

        return bottom

    def blocks_to_px(self, blocks):
        """convert the blocks to pixels."""
        return round(blocks * self.terrain2dlist_texts[self.template]['size'])

    def is_on_solid(self, x, y, size_of_obj):
        """ return true if the object is on solid ground. if it is not, return false."""
        arr = self.terrain2dlist_texts[self.template]['text'][:, x]
        bottom = y + size_of_obj
        print(bottom)
        bottom_blocks = self.px_to_blocks(bottom)
        print(self.px_to_blocks(x), bottom_blocks)

        return self.get_solid((self.px_to_blocks(x), bottom_blocks))

    def get_spawn_point(self, x, size_of_obj):
        """get a proper spawn point on Y axis for object.""" 
        blk_size = self.terrain2dlist_texts[self.template]['size']
        last_unsolid = self.blocks_to_px(self.get_last_unsolid(self.px_to_blocks(x)))
        first_solid = last_unsolid + blk_size

        return first_solid - size_of_obj

    def px_to_blocks(self, pixels):
        """convert blocks to pixels"""
        return round(pixels / self.terrain2dlist_texts[self.template]['size'])


def is_in_air(pos, terrain, size):
    """return true if the position is in air. if not, return false."""
    array = terrain.terrain2dlist_texts[terrain.template]['text']
    x, y = pos
    y += size
    try:
        column = array[:, terrain.px_to_blocks(x)]
    except IndexError:
        return False
    block = column[terrain.px_to_blocks(y)]

    return terrain.is_air(block)

def is_underground(pos, terrain, size):
    """return true if any part of the object is underground."""
    array = terrain.terrain2dlist_texts[terrain.template]['text']
    x, y = pos
    y += size
    print(array, 'howdy ho')
    column = array[:, terrain.px_to_blocks(x)]
    block = column[terrain.px_to_blocks(y)]
    return terrain.is_solid(block)




def _change_colour_surface(surface, r, g, b):
    """changes the colour of all parts of a 
    surface except for the transparent parts.
    """
    arr = pg.surfarray.pixels3d(surface)
    arr[:, :, 0] = r
    arr[:, :, 1] = g
    arr[:, :, 2] = b

def saveall():
    Terrain('dirt').save_all('binaries')

def main2():
    t = Terrain('dirt', 'drop')
    t.load_text()
    print(t.terrain2dlist_texts[t.template]['text'][:, 1])
    t.build_surface()

    pg.image.save(t.built_image, "C:\\Users\\Micha\\OneDrive\\Desktop\\hi.png")
    print(is_in_air((100, 315), t, 5))

if __name__ == '__main__':
    main2()
"""
this class is the base class
for all things like enemies, and characters.
"""

import pygame as pg
import threading


class IDontKnowWhatToCallItYet:
    def start_thread(self, **kwargs):
        self.mainthread = threading.Thread(
            target=self.mainloop, daemon=True, **kwargs)
        self.mainthread.start()

    def mainloop(self):
        pass
        # this needs to be figured out yet.
        # i figure i can do that when i get more
        # of the workings figured out

    def kill_thread(self):
        self.
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

    def attack_enemy(self, target):
        self.cooldown = self.attack.cooldown
        target.hit(self.attack)


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
"""
__init__.py- this is the only module that will 
be loaded on calling 'import class_', so i thought
it would be good to bundle everything in here.
it is expected that this will only be called
from .., so this should be fine
"""

try:
    from .screen import Screen, PeacefulScreen
    from .backgroundimage import BackGroundImage
    from .stage import Stage
    from .inventory import InventoryHandler
    from .enemy_head import EnemyHead
    from .my_rect import MyRect
    from .smr_error import SMRError
    from .terrain import Terrain
    from .weapon import *
    from .characters import *
    from .enemies import *
    from .attack import Attack
    import class_.enemies
    import class_.klass

except SystemError:
    from attack import Attack
    from inventory import InventoryHandler
    from screen import Screen, PeacefulScreen
    from backgroundimage import BackGroundImage
    from stage import Stage
    from enemy_head import EnemyHead
    from my_rect import MyRect
    from smr_error import SMRError
    from terrain import Terrain
    from weapon import *
    from characters import *
    from enemies import *
    import enemies
    import klass
import json as _json
import os
import enum

import pygame as _pg

_pg.mixer.pre_init(44100, 16, 2, 4096)
_pg.init()

import save
import levelparser
import class_ as _class_
from class_.sprite import SMRSprite as SpriteUtils

_pg.display.set_caption("Stickman's New World")
_pg.display.set_icon(_pg.image.load(os.path.join('data', 'game_icon.png')))
_pg.mouse.set_visible(False)
SURFACE = _pg.display.set_mode((800, 600))
ALL_LEVELS = levelparser.get_levels(SURFACE)

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

ALL_SCREENS = []

ALL_WEAPONS = []

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# "remember to add a 'Spicy Shot' magic book later." (Alvin Gu, Oct 26, 2018) #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

DEFAULT_WEAPONS = {
    'angel': _class_.Weapon('knife', 'Knife', 'black', 1, _class_.Attack(4, 20), 3),
    'swordsman': _class_.Weapon('sword', 'Sword', 'gray', 1, _class_.Attack(7, 60), 7),
    'spearman': _class_.Weapon('spear', 'Spear', 'gray', 1, _class_.Attack(5, 50), 12),
    'archer': _class_.Weapon('bow', 'Bow', 'brown', 1, _class_.Attack(3, 30), 130),
    'wizard': _class_.Weapon('wand', "Beginner's Spellbook", 'blue', 1, _class_.Attack(15, 120), 70),

}

ALL_COMPOS = []


import picture_collect

PICS = picture_collect.gather_pics('data')

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
        'TERMINAL': None,
        'SETTINGS': SETTINGS,
        'GAME_DATA': _SAVE,
        'INVENTORY': _INV,
        'MAIN_DISPLAY_SURF': SURFACE,
        'CURSOR': PICS['cursor'],
    }
else:
    MAIN_GAME_STATE = {
        'AREA': 0,
        'TERMINAL': None,
        'SETTINGS': SETTINGS,
        'GAME_DATA': {},
        'INVENTORY': {},
        'MAIN_DISPLAY_SURF': SURFACE,
        'CURSOR': PICS['cursor'],
    }
"""
encrypt.py- encrypter for stickmanranger save files.
I want people to be able to mad this game, but i dont 
necessarily want people to be able to change it up 
super easily!"""
from cryptography.fernet import Fernet
from itertools import count
import os
import shutil
import time

if not os.name == 'nt':
    os.getlogin = lambda: __import__('pwd').getpwuid(os.getuid())[0]

CURRENT_TIME = time.asctime()
PATH = {
    'nt': 'C:\\Users\\{}\\.stickman_new_world\\save\\'.format(os.getlogin()),
    'posix': '/home/{}/.stickman_new_world/save/'.format(os.getlogin()),
}[os.name]

PATH_NUMERIC = os.path.join(PATH, '%s') + '\\' if os.name == 'nt' else '/'
print(PATH_NUMERIC)

if not os.path.exists(PATH):
    os.makedirs(PATH)

FILE = PATH + '.smr-save'
print(FILE)


def encrypt(string):
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    prev_key = os.listdir(PATH)
    for f in prev_key:
        if not f in ('.smr-save', 'time'):
            os.remove(PATH + f)

    prev_dir = 0
    for number in count():
        if os.path.exists(PATH_NUMERIC % number):
            prev_dir = number

        else:
            # the system can't find this file, but it will only
            # be the first one it doesnt find.
            prev_dir = number
            break

    def_path = PATH
    # os.mkdir(def_path)

    key = Fernet.generate_key()
    # simply make a file with that name
    with open(def_path + key.decode(), 'w'):
        pass

    encrypter = Fernet(key)
    cipher = encrypter.encrypt(string.encode())

    with open(FILE, 'wb') as cipher_file:
        cipher_file.write(cipher)

    with open((os.path.join(def_path, 'time')), 'w') as time_file:
        time_file.write(CURRENT_TIME)
    return cipher


def decrypt(spec=None):
    prev_dir = spec

    if spec is None:
        prev_dir = 0
        for number in count():
            if os.path.exists(PATH_NUMERIC % number):
                prev_dir = number

            else:
                # the system can't find this file, but it will only
                # be the first one it doesnt find.
                break

    data = open(FILE, 'rb').read()
    key = os.listdir(PATH)
    key.pop(key.index('.smr-save'))
    key.pop(key.index('time'))
    key = key[0].encode()

    encrypter = Fernet(key)
    text = encrypter.decrypt(data).decode()

    saved_time = open(os.path.join(PATH, 'time')).read()

    return text, saved_time


if __name__ == '__main__':
    time = __import__('time').asctime()
    print(encrypt(open('misc\\shello.ini').read()))
    print(decrypt()[0], decrypt()[1], sep='\n\n\n')
"""gameplay.py- main gameplay file.
handle all events in this file, display terrain, handle deaths, 
status effects, etc...
"""

from pygame.locals import QUIT, MOUSEBUTTONDOWN
import pygame as pg

from database import MAIN_GAME_STATE, PICS, ALL_LEVELS, Area

SURFACE = MAIN_GAME_STATE['MAIN_DISPLAY_SURF']

PLAY_AREA = pg.Rect((800, 400), (0, 0))
MENU_AREA = pg.Rect((800, 200), (0, 400))

CLOCK = pg.time.Clock()
FPS = 60

def main():
    """run the game, after the title screen."""
    continue_ = True
    menu = pg.Surface((800, 200))
    menu.fill((0, 255, 0))
    MAIN_GAME_STATE['MOUSEDOWN'] = False

    while continue_:
        MAIN_GAME_STATE['MOUSE_POS'] = pg.mouse.get_pos()
        events = [event for event in pg.event.get()]
        if MAIN_GAME_STATE['AREA'] == Area.MAP:
            draw_map()
            handle_map()

        elif MAIN_GAME_STATE['AREA'] == Area.STAGE:
            MAIN_GAME_STATE['STAGE'].update(events)
        
        
        MAIN_GAME_STATE['MAIN_DISPLAY_SURF'].blit(MAIN_GAME_STATE['CURSOR'], pg.mouse.get_pos())
        # MAIN_GAME_STATE['MAIN_DISPLAY_SURF'].blit(menu, (0, 400))
        pg.display.update()

        CLOCK.tick(FPS)

def draw_map():
    """draw the map to the screen, and all stages."""
    SURFACE.blit(PICS['Maps']['complete'], (0, 0))
    for stage in ALL_LEVELS:
        stage.draw_on_map()

def handle_map():
    pos = pg.mouse.get_pos()
    print(pos)

    for stage in ALL_LEVELS:
        stage.check_hover(pos)

        for event in pg.event.get():
            check_quit(event)

            if event.type == MOUSEBUTTONDOWN and stage.rect.collidepoint(*event.pos):
                stage.init(MAIN_GAME_STATE)
                MAIN_GAME_STATE['STAGE'] = stage
                MAIN_GAME_STATE['AREA'] = Area.STAGE




def check_quit(event):
    """check if event is a quit event. if it is, quit."""
    if event.type == QUIT:
        pg.quit()
        raise SystemExitprint("Hello")
with open('file.txt', 'w') as openfile:
       openfile.write('Hello')
import threading
import tkinter.messagebox
threading.Thread(
    target=lambda: tkinter.messagebox.showmessage('hi', 'hi')).start()
from queue import Queue
Q = Queue()


def p():
    print(Q.get())


t = threading.Thread(target=p)
t.start()
while True:
    Q.put(input('type to send a message to t: '))
"""levelparser: converts a JSON level into a Stage object."""

import json

import pygame

import class_

def get_levels(mainsurf):
	"""parse and return all levels in levels.json."""
	levels = json.load(open("levels.json"))
	print(levels.keys(), levels.values())
	stages = []

	for name, items in zip(levels, levels.values()):
		screens = []
		for obj in items['screens']:
			enemies = {}
			for enemy in obj['enemies']:
				enemy_obj = getattr(class_, enemy['type'])(
							enemy['colour'],
							class_.EnemyHead(*enemy['head']),
							enemy['drops'],
							enemy['droprates'],
							class_.Attack(*enemy['attack']),
							enemy['health'],
							enemy['range'],
							enemy['size'],
						)
				enemies[enemy_obj] = enemy['amount']

					
			screens.append(class_.Screen(enemies))

		print(json.dumps(items, indent=4))
		stage = class_.Stage(
			name,
			position_on_map=tuple(items['position']),
			all_screens=screens,
			boss_screen=items['boss_screen'],
			surface=mainsurf,
			terrain=class_.Terrain(
				items['terrain']['texture'], items['terrain']['template']),
			comes_from=items['comes_from'],
		)
		stages.append(stage)

	return stages
# hi
get_levels(pygame.Surface((1, 1)))#!/usr/bin/python3
# main.py
"""
the main code for the game stickman ranger, a game similar to stick ranger(www.dan-ball.jp/en/javagame/ranger)
the goal is to defeat bosses and not get killed.
project started: oct. 20, 2017. 
first level release goal: march 1, 2018
source code by Michael Gill
original SR by Ha55ii

this game is built on pygame, an excellent game engine for python
thanks to paint.net, which I made the sprites on.

UPDATE: May 18
Oh my goodness i look back at this code after so long of ignoring main.py
i kind of hate this module now.
oh well, it works, i suppose. for now
By the way, i wasnt even close to my intended release date :)
"""

__author__ = 'Michael Gill'
__version__ = '0.0'
__all__ = ['draw_box', 'draw_text', 'terminate', 'main']

import sys
import time

from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
import pygame as pg

# local imports
#import save
import database
import class_
import dicts
from dicts import COLOURS
import check_update

### constant values ###

##### IMPORTANT! REMEMBER CARTESIAN SYSTEM! ######
##### 0 FOR BOTH COORDINATES START IN TOP LEFT ###

NUM_OF_CHARS = 4

###functionality begins here! (YAY! FINALLY)###


def main():
    """
    main functionality begins here
    """
    check_update.main()

    global CLOCK, SURFACE, PICS
    flag = True
    # for stopping the game loop when clicked, stop clutter.

    pg.init()

    PICS = dicts.gather_pics('data')
    print(PICS)
    SURFACE = database.SURFACE
    CLOCK = pg.time.Clock()

    pg.display.set_caption('StickMan Ranger')
    pg.display.set_icon(PICS['game_icon'])

    SURFACE.blit(PICS['Title_Screen'], (0, 0))

    while flag:  # main loop:
        for ev in pg.event.get():
            if ev.type == QUIT:
                terminate()
            elif ev.type == MOUSEBUTTONDOWN:
                cho = choose_game_mode()
                flag = False
        pg.display.update()
    print('main event loop terminated')
    # print functions in this code are for debugging purposes only

    if cho is 0:
        char_list = get_keys_from_pics(get_characters())
        clear_screen()
        char_string = '\n'.join(char_list)
        draw_text(char_string, size=45)
        SURFACE.blit(PICS['Maps']['half_complete'], (0, 0))

        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    terminate()
            pg.display.update()


def choose_game_mode() -> int:
    """
    choose which option the player wants
    return 1 if player chooses new game
    return 2 if player chooses load game
    return 3 if player chooses load a backup.
    """
    print('choose_game_mode called')
    SURFACE.fill(COLOURS['white'])

    # I realize now that Ishould have used a function for the three sections
    # below, but whatever.
    LabelPlay = pg.font.Font('data\\Michael`s Font.ttf', 32)
    PlaySurf = LabelPlay.render('New Game', True, COLOURS['black'],
                                COLOURS['white'])
    PlayRect = class_.MyRect(PlaySurf.get_rect())
    PlayRect.center = ((WIN_X // 2), (WIN_Y // 2) - 50)
    SURFACE.blit(PlaySurf, PlayRect)

    #################################################################

    LabelLoad = pg.font.Font('data\\Michael`s Font.ttf', 32)
    LoadSurf = LabelLoad.render('Load Game', True, COLOURS['black'],
                                COLOURS['white'])
    LoadRect = class_.MyRect(LoadSurf.get_rect())
    LoadRect.center = (WIN_X // 2, WIN_Y // 2)
    SURFACE.blit(LoadSurf, LoadRect)

    #################################################################

    LabelLoadEarlier = pg.font.Font('data\\Michael`s Font.ttf', 32)
    LESurf = LabelLoadEarlier.render('Load Earlier Save', True,
                                     COLOURS['black'], COLOURS['white'])
    LERect = class_.MyRect(LESurf.get_rect())
    LERect.center = (WIN_X // 2, WIN_Y // 2 + 50)
    SURFACE.blit(LESurf, LERect)

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == MOUSEMOTION:
                x, y = event.pos
                for (rect, surf) in ((PlayRect, PlaySurf),
                                     (LoadRect, LoadSurf), (LERect, LESurf)):
                    rect.handle(event, SURFACE, surf)

            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if PlayRect.collidepoint(x, y):
                    print("PlayRect Clicked")
                    return 0  # these return value, and end loop

                elif LoadRect.collidepoint(x, y):
                    print("LoadRect Called")
                    return 1

                elif LERect.collidepoint(x, y):
                    print("LERect called")
                    return 2

            pg.display.update()


def draw_text(
        text,
        size=32,
        cen_of_txt=(WIN_X // 2, WIN_Y // 2),
        colour=(COLOURS['black'], COLOURS['white']),
) -> tuple:
    """
    function for drawing text on SURFACE,
    returns a tuple containing the rect
    of the surface, and the surface 
    itself.
    """
    FontObj = pg.font.Font('data\\Michael`s Font.ttf', size)
    FontSurf = FontObj.render(text, True, *colour)
    Rect = FontSurf.get_rect()
    Rect.center = cen_of_txt
    SURFACE.blit(FontSurf, Rect)
    return class_.MyRect(Rect, colour=COLOURS['white']), FontSurf


def draw_box(size, colour, pos, alpha=None, image=None) -> tuple:
    """
    return a square rectangle, surface pair
    uses MyRect
    """
    print(pos)
    new_surf = pg.surface.Surface(size)
    new_surf.fill(colour)

    if alpha is not None:
        new_surf.set_alpha(alpha)

    SURFACE.blit(new_surf, pos)

    if image is not None:
        SURFACE.blit(image, pos)

    return class_.MyRect(
        new_surf.get_rect(topleft=pos), colour=colour), new_surf


def terminate():
    "end the current pygame program"
    # need to  save the game... put some function call
    pg.quit()
    sys.exit()


def get_characters() -> list:
    """
    starts a new game,
    and lets the player choose
    their characters.
    returns a list of the characters
    the player has chosen.
    """
    SURFACE.fill(COLOURS['white'])

    draw_text(
        'Choose your players:', cen_of_txt=(WIN_X // 2, WIN_Y // 2 - 200))

    texts = {}
    pairs = []
    num = -250  # this is the starting point for the images to appear

    # puts all the characters in a line with their caption beneath
    for string in database.ALL_CLASSES:
        string = string.lower()
        texts[string] = draw_text(
            string, size=20, cen_of_txt=(WIN_X // 2 + num, WIN_Y // 2 + 200))

        pic = PICS['characters'][string]
        SURFACE.blit(pic, (texts[string][0].x + 20, texts[string][0].y + 30))

        pairs.append((string, class_.MyRect(pic.get_rect())))
        num += 100

    del num, string

    box_list = []

    # this loop puts 4 boxes to show which characters the user has chosen
    for i in range(WIN_X // 4, WIN_X // 4 * 3, 100):
        box_list.append((draw_box(
            (25, 25), COLOURS['gray'], (i, WIN_Y // 2), alpha=200),
                         (i, WIN_Y // 2))[0][0])

    del i

    print('pairs: ', *pairs, sep='\n')

    char_list = []
    clicked = 0
    boxes_with_pictures = []
    box_num_pairs = {
        1: box_list[0],
        2: box_list[1],
        3: box_list[2],
        4: box_list[3],
    }
    for key in box_num_pairs:
        print('key: ', key, ' box: ', box_num_pairs[key], sep='')

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == MOUSEMOTION:
                for key in texts:
                    M = texts[key]
                    M[0].handle(event, SURFACE, M[1])

            # this branch controls when a selection box is
            # selected, which one to underline.
            elif event.type == MOUSEBUTTONDOWN:  # if mouse is clicked
                x, y = event.pos

                for key, rect in zip(box_num_pairs.keys(),
                                     box_num_pairs.values()):
                    print(rect is box_num_pairs[key])

                    if rect.collidepoint(x, y):
                        # if click is in 'rect'
                        if not rect.underlined:
                            # only do this is 'rect' is underlined
                            rect.underline(SURFACE)

                        if clicked == key:
                            box_num_pairs[clicked].remove_underline(SURFACE)
                            clicked = 0

                        elif clicked == 0:
                            clicked = key

                        else:
                            box_num_pairs[clicked].remove_underline(SURFACE)
                            clicked = key

                for rect_key, rect in zip(box_num_pairs.keys(),
                                          box_num_pairs.values()):

                    for character_name, rect_surf_pair in zip(
                            texts.keys(), texts.values()):

                        if rect_surf_pair[0].collidepoint(x, y):
                            print('garpenchank')
                            try:
                                box_num_pairs[clicked].draw_inside(
                                    PICS['characters'][character_name],
                                    SURFACE)
                                boxes_with_pictures.append(clicked)

                            except (class_.SMRError, KeyError) as error:
                                print(error)

                            break

                        elif clicked in boxes_with_pictures:
                            print('gud')
                            box_num_pairs[clicked].remove_pic(SURFACE)

                        char_list = [
                            box.PicInside for box in box_num_pairs.values()
                        ]

        pg.display.update()

        if not None in char_list[:2]:
            print('howdy')
            char_list = [box.PicInside for box in box_num_pairs.values()]
        if not None in char_list:
            return char_list


def clear_box(pos):
    """
    clears the box that needs to be cleared.
    """

    print('in the function clear_box')

    draw_box((25, 25), COLOURS['white'], pos)
    draw_box((25, 25), COLOURS['gray'], pos, alpha=100)


def change_colour_surface(surface, r, g, b):
    """changes the colour of all parts of a 
    surface except for the transparent parts.
    """
    arr = pg.surfarray.pixels3d(surface)
    arr[:, :, 0] = r
    arr[:, :, 1] = g
    arr[:, :, 2] = b


def get_keys_from_pics(orig_list):
    """
    returns a dict that has keys of the original
    dict that the pics were contained in. for example:
    get_keys_from_pics(gladiator_pic) 
    will return:
    {'gladiator': <class 'pygame.Surface' object>}
    note: if an item doesnt match, for example a 
    string, or a picture not in data/characters,
    nothing will be done with it.
    """
    pics_dict = PICS['characters']
    new_dict = {}

    for key, value in zip(pics_dict.keys(), pics_dict.values()):
        for picture in orig_list:
            if picture == value:
                new_dict[key] = value

    return new_dict


def clear_screen():
    return SURFACE.fill(COLOURS['white'])


if __name__ == '__main__':
    main()

else:
    print('why on earth are you importing this?\n\
        it is supposed to a main module!')
"""menu.py- handle the menu at the bottom of the screen."""
"""
bugreport.py
this module takes any exception, the app name,
and any other info, and reports it to my email.
"""

import io
import os
import smtplib
from cryptography.fernet import Fernet
import sys
import threading
import traceback
import platform

FYUKYFVKFYVHUFL = b'gAAAAABavaf20Qc-jiOnPXzOsBfr-yhJiVbuBEiyK4cJA3r82f0wXAp5gdgPQ43UxZB7H9O9RgiTCHDb0ngh9CNCRPi03nQssg=='
HIUEFWILEIURFHE = b'_qJoI0kXZlQuHI0-U8BSSKuKQ_Zpp3vQMZGrPKMk8lI='
TMP = os.path.join(
    '/tmp/', 'stderr.tmp') if os.name == 'posix' else os.path.join(os.getenv('TMP'), 'stderr.tmp')


def main(project_name, exception, *other_info):
    """
    main function for sending mail.
    """
    exception.args = [str(arg) for arg in exception.args]
    print(exception.args)
    exception_traceback_details, exception_message = get_details(exception)
    email = build_message(project_name, exception_message,
                          exception_traceback_details, *other_info)
    send_message(email)


def send_message(message):
    """
    sends message to the bug report address
    """
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # i dont want random people just emailing me!!
    decrypter = Fernet(HIUEFWILEIURFHE)
    data = decrypter.decrypt(FYUKYFVKFYVHUFL).decode()
    server.ehlo()
    server.login('bugreporter.smr@gmail.com', data)
    server.sendmail('bugreporter.smr@gmail.com',
                    'bugreporter.smr@gmail.com', message)
    server.close()


def build_message(project, tbmessage, details, *args):
    """
    build and return a email that contains the 
    traceback.
    """

    bottomline = ',\n'.join(args) if len(args) > 0 else 'Nope'
    sender = reciever = 'bugreporter.smr@gmail.com'
    name = os.name
    build = platform.platform()
    email_string = f"""
    From: {sender}
    To: {reciever}
    Subject: bug in {project} on a {name} system :(

    
    platform:
        {build}

    
    details (traceback):
        {details}

    the message (even though it showed up before):
        {tbmessage}

    any extra things?
    
    {bottomline}


    sincerely, automatic message that has no heart :)
    """

    return email_string


def get_details(exception):
    """
    return the details of the traceback
    """

    tbstring = ''.join(traceback.format_exception(
        type(exception), exception, exception.__traceback__))
    tbargs = ', '.join(exception.args)
    return tbstring, tbargs


def default_smr(exception, *args):
    main('stickman\'s new world', exception, *args)


try:
    raise SyntaxError

except BaseException as e:
    main('test', e)
"""
dirtools.py
this modules aim is to do stuff.
"""
import os
import io


def gather_tree(dir='.', inputmethod=io.TextIOWrapper.read, previousdict=None):
    """
    gathers this tree into a dict.
    directories will become sub-dictionaries.
    files will become
import pygame as pg
pg.init()
a = pg.font.Font('freesansbold.ttf', 32)
s = pg.Surface((100, 100))
s.fill((255, 255, 255))
s.blit(a.render('hello', True, (0, 0, 0)), (0, 0))
pg.image.save(s, 'C:\\Users\\michael\\desktop\\s.png')import os
os.chdir(r'C:\Users\Michael\Desktop\stickmanranger')
print(
    'hi! I am formatting your files in your current project, stickmanranger!')
for i in os.listdir():
    try:
        if i.endswith('.py'):
            print('formatting %a' % i)
            os.system('yapf -i %s' % i)
    except:
        pass
print('done!')
import time
time.sleep(1)
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
    main()from multiprocessing import *
import time


def s():
    time.sleep(1)
    print('hi!')


class Main():
    def do(self):
        print('hi!')
        time.sleep(1)

    def start(self):
        def a():
            pass

        self.s = Process(target=a)
        self.s.start()


if __name__ == '__main__':
    Main().start()
    Main().start()
# this is a stupid comment
pass
import sys
import threading

try:
    import chwsuakeuegy

except Exception as l:
    d = l


def raise_d():
    raise d


sys.stderr = open('C:\\users\\michael\\desktop\\stderr.txt', 'w')


def raise_d():
    raise d


raise_d()
print('??')
sys.stderr.close()
import pygame
from pygame.locals import *

# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 430
SCREEN_HEIGHT = 410

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

FPS = 30

# --- classses --- (CamelCase names)

# empty

# --- functions --- (lower_case names)

# empty

# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption(
    "Fracking System (because \"Tracking System\" sounded too wierd")

# - objects -

rectangle = pygame.rect.Rect(0, 0, 30, 30)
rectangle_draging = False

# - mainloop -

clock = pygame.time.Clock()

running = True

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = rectangle.x - mouse_x
                    offset_y = rectangle.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x + offset_x
                rectangle.y = mouse_y + offset_y

    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, rectangle)

    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()
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
"""
request_email.py
requests the user's email address for bug reports.
"""
import tkinter as tk
import os

MESSAGE = '''you can enter your email
address here, and if the game crahses,
it should be reported to me,
and I can get back to you and \ntry and get it fixed!\n
(it is completely optional,\npress \'skip\' to continue)
if you dont get it, it means you didnt enter the correct email address.
contact me at <michaelveenstra12@gmail.com> for help if you do that

you should recieve a confirmation email :)
oh yeah, I wont sell it to anyone either'''

try:
    FILE = os.path.join((os.environ['USERPROFILE'] if os.name ==
                         'nt' else os.environ['']), '.stickman_new_world', 'useremail')
except KeyError:
    wrong_os()


def main():
    print('hi')
    variables = {}

    if os.path.exists(FILE):
        return

    root = tk.Tk()
    root.title('email address')
    root.geometry('250x270')
    root.protocol('WM_DELETE_WINDOW', lambda: exit(variables))

    entry = tk.Entry(root, text='email:')
    entry.place(anchor='center', relx=0.5, rely=0.5)
    entry.pack(fill=None, expand=True)

    label = tk.Label(root, text=MESSAGE)
    label.pack(fill=None, expand=True)

    skip = tk.Button(root, text='skip', command=lambda: exit(variables))
    skip.place(x=220, y=100)
    skip.pack()

    done = tk.Button(root, text='done',
                     command=lambda: get_text(entry, variables))
    done.place(x=200, y=100)
    done.pack()

    while True:
        print('hi')
        if variables.get('quit'):
            return

        elif variables.get('entry_data'):
            remember(variables)
            send_confirm(variables)
            root.destroy()

        root.update()


def get_text(entry, variables):
    print(entry.get())
    variables['entry_data'] = entry.get()


def exit(v):
    v['quit'] = True


def remember(item):
    with open(FILE, 'w') as openfile:
        openfile.write(item['entry_data'])
    exit(item)


def send_confirm(items):
    import smtplib
    import bugreport
    from cryptography.fernet import Fernet

    sender = 'bugreporter.smr@gmail.com'
    reciever = [items['entry_data']]
    message = f'''To: <{reciever}>
From: <{sender}>
Subject: confirmation email


Hi! if you are recieving this email, it means you have successfully
gotten your email address to me. Since you didn't give your password,
you shouldnt have any troubles. I will only use this when I have a very important
thing to tell you, or if the game crashes on your computer, I will be alerted
and try to fix the problem and tell you about it as well. Thanks!

-sincerely, Michael Gill (creater of stickman\'s new world)
'''
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    a = Fernet(bugreport.HIUEFWILEIURFHE).decrypt(
        bugreport.FYUKYFVKFYVHUFL).decode()
    server.ehlo()
    server.login(sender, a)
    server.sendmail(sender, reciever, message)
    server.close()


try:
    main()

except Exception as e:
    import bugreport
    bugreport.default_smr(e, 'in request_email')
import pygame as pg
from pygame.locals import *
from threading import Thread

FPS = 60
SCREEN_X, SCREEN_Y = 800, 600
RECT_X, RECT_Y = 10, 10
RIGHT_CLICK = 1
GREEN = (0, 200, 0)
RED = (200, 0, 0)


def main():
    pg.init()
    global DISPLAY, CLOCK

    DISPLAY = pg.display.set_mode((SCREEN_X, SCREEN_Y))
    CLOCK = pg.time.Clock()

    screen_image = pg.image.load('..\\data\\dash_skeleton.png').convert()
    DISPLAY.blit(screen_image, (0, 0))

    rect1 = Rect(SCREEN_X // 2, SCREEN_Y // 2, RECT_X, RECT_Y)
    drag = False

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                raise SystemExit

            drag_if_supposed_to(rect1, event, drag)

        pg.display.update()
        DISPLAY.blit(screen_image, (0, 0))
        pg.draw.rect(DISPLAY, GREEN, rect1)
        pg.display.flip()
        CLOCK.tick(FPS)


def drag_if_supposed_to(rect, event, drag=False):
    if event.type == MOUSEBUTTONDOWN:
        if event.button == RIGHT_CLICK and rect.collidepoint(event.pos):
            print('boccoloni')
            drag = True
            mouse_x, mouse_y = event.pos
            off_x = rect.x - mouse_x
            off_y = rect.y - mouse_y

    elif event.type == MOUSEBUTTONUP:
        if event.button == RIGHT_CLICK:
            drag = False

    elif event.type == MOUSEMOTION:
        if drag:
            mouse_x, mouse_y = event.pos
            rect.x = mouse_x + off_x
            rect.y = mouse_y + off_y

    return drag


main()
from time import sleep
import os

while True:
    os.system('python format.py')
    sleep(10 * 60)
"""a replacement and better written file than main.py.
for starting the game.
"""

from argparse import Namespace
import copy
import os

# pylint: disable=no-name-in-module

from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION
import pygame as pg

from class_.character_image import CharacterImage
import class_
from database import COLOURS, MAIN_GAME_STATE
import database
import gameplay


# window sizes
WIN_X, WIN_Y = 800, 600
MID_X = WIN_X // 2
MID_Y = WIN_X // 2
CENTRE = MID_X, MID_Y

CENTRE_X, CENTRE_Y = database.SURFACE.get_rect().center

WHITE = COLOURS['white']
BLACK = COLOURS['black']

FPS = 60

PICS = database.PICS

# (:()-|--<
# parts created on computer, assembled in canada.
# NO BATTERIES REQUIRED
# (except in the computer, maybe)


def _border(surf, colour):
    """puts a rectangular border around
    surf's rectangle.
    """
    rect = surf.get_rect()
    bottom = rect.bottomleft, rect.bottomright
    top = rect.topleft, rect.topright
    left = rect.topleft, rect.bottomleft
    right = rect.topright, rect.bottomright

    lines = [(rect.bottomright[0] - 1, rect.bottomright[1] - 1),
             (rect.bottomleft[0], rect.bottomleft[1] - 1),
             (rect.topleft[0], rect.topleft[0]),
             (rect.topright[0] - 1, rect.topright[1])]

    pg.draw.lines(surf, colour, True, lines)


class Box:
    """box that can hold an image."""

    border = True
    selected = False

    def __init__(self,
                 topleft,
                 width,
                 height,
                 colour=BLACK,
                 image=None,
                 onclick=lambda: None,
                 ):
        self.topleft = topleft
        self.colour = colour
        self.image = image
        self.width = width
        self.height = height
        self.onclick = onclick

        top, left = self.topleft

        self.rect = pg.Rect((top, left), (self.width, self.height))

    def draw(self, surf):
        """draw the box to the screen."""

        rect = self.rect

        if self.selected:
            # make the box red instead.
            pg.draw.rect(surf, COLOURS['red'], rect, 1)

        else:
            pg.draw.rect(surf, self.colour, rect, 1)

        if self.image is not None:
            img_rect = self.image.get_rect()
            img_rect.center = rect.center
            surf.blit(self.image, img_rect)

    def handle(self, event, *args, **kwargs):
        """handle the event. if it is clicked on, then call and return
        self.onclick. if not, do nothing.
        """

        try:
            if self.rect.collidepoint(event.pos) and event.type == MOUSEBUTTONDOWN:
                return self.onclick(*args, **kwargs)
        except AttributeError:
            # incorrect event.
            pass


# clock for keeping track of FPS
CLOCK = pg.time.Clock()

# SURFACE is already created in database
SURFACE = database.SURFACE


class ClickableLabel:
    """a label that can be clicked. when it is, then call
    a designated function.
    """
    underlined = False
    shaded = False

    def __init__(self,
                 text,
                 pos,
                 function,
                 forecolour,
                 backcolour=None,
                 shade=True,
                 textsize=16,
                 *args,
                 **kwargs
                 ):
        self.text = text
        self.pos = pos
        self.function = function
        self.shade = shade
        self.textsize = textsize
        self.forecolour = forecolour
        self.backcolour = backcolour
        self.args = args
        self.kwargs = kwargs

    def _shade(self, colour=COLOURS['grey']):
        """shade the current rect."""

        newsurf = pg.Surface((self.rect.width, self.rect.height))
        newsurf.set_alpha(75)
        newsurf.fill(colour)
        self.textsurf.blit(newsurf, (0, 0))

    def draw(self, surface):
        """draw the label to the screen."""
        fontobj = pg.font.Font(
            os.path.join('data', 'Michael`s Font.ttf'),
            self.textsize,
        )
        textsurf = fontobj.render(
            self.text, True, self.forecolour, self.backcolour)
        textrect = textsurf.get_rect()
        textrect.center = self.pos
        self.rect = textrect
        self.textsurf = textsurf

        mouseover = self.rect.collidepoint(
            pg.mouse.get_pos())
        # print(pg.mouse.get_pos())
        #@print(self.rect.topleft)

        if mouseover:
            # print('shading')
            self._shade()
            self.shaded = True

        else:
            self.shaded = False

       # if self.underlined:
        #    start, end = self.rect.bottomleft, self.rect.bottomright
        #    pg.draw.line(surface, self.forecolour, start, end)

        surface.blit(textsurf, textrect)

    def update(self, surface):
        """updates the label."""
        # if self.rect.underlined:
        #     self.rect.underline(surface)

    def handle(self, event, surface):
        if event.type == MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.shaded = True

        elif (event.type == MOUSEBUTTONDOWN and
              self.rect.collidepoint(event.pos)):
            self.underlined = not self.underlined

    def is_selected(self):
        return self.rect.underlined


def main():
    """start the game"""

    # set caption and title screen
    pg.display.set_caption("Stickman's New World")
    pg.display.set_icon(PICS['game_icon'])

    # place starting image on screen
    SURFACE.blit(PICS['title_screen'], (0, 0))
    continue_ = True

    while continue_:
        SURFACE.blit(PICS['title_screen'], (0, 0))
        SURFACE.blit(MAIN_GAME_STATE['CURSOR'], pg.mouse.get_pos())
        for event in pg.event.get():
            check_quit(event)

            if event.type == MOUSEBUTTONDOWN:
                # on to the next loop
                continue_ = not continue_
        pg.display.update()

    func = lambda: None
    continue_ = True
    rects = draw_choices()

    pg.mixer.music.load(os.path.join(
        os.getcwd(), 'music', 'smnwtheme.mp3'
    ))
    pg.mixer.music.play(-1)   # loop forever, until stopped

    while continue_:
        SURFACE.blit(PICS['menu_background'], (0, 0))
        label("Stickman's New World", CENTRE_X, 100, size=60)
        for lbl in rects:
            lbl.draw(SURFACE)
        for event in pg.event.get():
            check_quit(event)

            for lbl in rects:
                lbl.handle(event, SURFACE)

                if event.type == MOUSEBUTTONDOWN and lbl.rect.collidepoint(*event.pos):
                    func = lbl.function
                    continue_ = False

        SURFACE.blit(MAIN_GAME_STATE['CURSOR'], pg.mouse.get_pos())
        pg.display.update()
        CLOCK.tick(FPS)

    func()


def drawopt(text, x, y, func=0):
    """draw text tto the screen at (x, y).
    return class_.MyRect of rectangle."""
    fontobj = pg.font.Font(os.path.join('data', 'Michael`s Font.ttf'), 32)
    textsurf = fontobj.render(text, True, WHITE)
    textrect = textsurf.get_rect()
    textrect.center = (x, y)
    SURFACE.blit(textsurf, textrect)
    return class_.MyRect(textrect), textsurf, func


def check_quit(event):
    """check if event is a quit event. if it is, quit."""
    if event.type == QUIT:
        pg.quit()
        raise SystemExit


def label(text, x, y, size=32, colour=WHITE):
    """draw a static label to the screen."""
    fontobj = pg.font.Font(os.path.join('data', 'Michael`s Font.ttf'), size)
    textsurf = fontobj.render(text, True, colour)
    textrect = textsurf.get_rect()
    textrect.center = (x, y)
    SURFACE.blit(textsurf, textrect)


def draw_choices():
    """draw all the options to click on
    on game start.
    """

    # print(centre_x, centre_y)

    # choices = [
    #     drawopt('New Game', centre_x, centre_y - 50, 1),
    #     drawopt('Load Game', centre_x, centre_y, 2),
    #     drawopt('Settings', centre_x, centre_y + 50, 3)
    # ]

    choices = [
        ClickableLabel("New Game", (CENTRE_X, CENTRE_Y - 100),
                       RECT_FUNCS[1], WHITE, textsize=40),
        ClickableLabel("Load Game", (CENTRE_X, CENTRE_Y),
                       RECT_FUNCS[0], WHITE, textsize=40),
        ClickableLabel("Settings", (CENTRE_X, CENTRE_Y + 100),
                       RECT_FUNCS[2], WHITE, textsize=40),
    ]

    return choices


START_X, START_Y = 100, WIN_Y // 2


def _make_coloured(box):
    if box._colour == 0:
        box._colour = 1
        box.colour = COLOURS['red']
        return box
    else:
        box._colour = 0
        box.colour = COLOURS['white']
        return None


def new_game():

    char_imgs = [
        CharacterImage('swordsman',
                       # fake weapon. only has colour attribute
                       Namespace(colour='grey'),
                       (START_X, START_Y),
                       None,
                       ),
        CharacterImage('angel',
                       Namespace(colour='gold'),
                       (START_X + 150, START_Y),
                       None,
                       ),
        CharacterImage('archer',
                       Namespace(colour='brown'),
                       (START_X + 300, START_Y),
                       None,
                       ),
        CharacterImage('spearman',
                       Namespace(colour='grey'),
                       (START_X + 450, START_Y),
                       None,
                       ),
        CharacterImage('wizard',
                       Namespace(colour='blue'),
                       (START_X + 600, START_Y),
                       None,
                       ),
    ]

    selected_char_imgs = [
        CharacterImage('swordsman',
                       # fake weapon. only has colour attribute
                       Namespace(colour='grey'),
                       (12, 16),
                       None,
                       ),
        CharacterImage('angel',
                       Namespace(colour='gold'),
                       (12, 16),
                       None,
                       ),
        CharacterImage('archer',
                       Namespace(colour='brown'),
                       (12, 16),
                       None, 
                       ),
        CharacterImage('spearman',
                       Namespace(colour='grey'),
                       (12, 16),
                       None, 
                       ),
        CharacterImage('wizard',
                       Namespace(colour='blue'),
                       (12, 16),
                       None, 
                       ),
    ]

    null = lambda: None

    y = WIN_Y // 2 + 30

    char_lbls = [
        ClickableLabel(
            'Swordsman',
            (START_X, y),
            null,
            WHITE,
            textsize=24
        ),
        ClickableLabel(
            'Angel',
            (START_X + 150, y),
            null,
            WHITE,
            textsize=24,
        ),
        ClickableLabel(
            'Archer',
            (START_X + 300, y),
            null,
            WHITE,
            textsize=24,
        ),
        ClickableLabel(
            'Spearman',
            (START_X + 450, y),
            null,
            WHITE,
            textsize=24,
        ),
        ClickableLabel(
            'Wizard',
            (START_X + 600, y),
            null,
            WHITE,
            textsize=24,
        ),
    ]

    # this is a list of four, and contains a box aligned with its image.
    chosen = [(None, None)] * 4

    def set_(box):
        old = get_selected()
        # print(old, 'HoWdY YoU FeLlErS')
        old.selected = False
        box.selected = True

    chosen_boxes = [
        Box((250, 400), 30, 30, WHITE, onclick=lambda: set_(chosen_boxes[0])),
        Box((350, 400), 30, 30, WHITE, onclick=lambda: set_(chosen_boxes[1])),
        Box((450, 400), 30, 30, WHITE, onclick=lambda: set_(chosen_boxes[2])),
        Box((550, 400), 30, 30, WHITE, onclick=lambda: set_(chosen_boxes[3])),
    ]

    chosen_boxes[0].selected = True

    def get_selected():
        """return the selected box."""
        for i in chosen_boxes:
            if i.selected:
                # print(chosen_boxes.index(i))
                return i

    continue_ = True
    num_selected = 0

    next_button = ClickableLabel(
        "Next", (700, 420), lambda: None, WHITE, textsize=50)
    next_button.draw(SURFACE)
    if None not in chosen:
        # fills the next_button.rect spot. will not show up yet
        next_button.draw(SURFACE)
    filled = False

    while continue_:

        SURFACE.blit(PICS['menu_background'], (0, 0))
        if None not in chosen:
            next_button.draw(SURFACE)
            filled = True

        label('Choose your players:', MID_X, 75, 60)
        for box in chosen_boxes:
            box.draw(SURFACE)

        for i in char_imgs:
            i.build_image(SURFACE, COLOURS['beige'], False)

        for i in char_lbls:
            i.draw(SURFACE)
            # if i.underlined:
            # add_chosen(char_lbls, i, char_imgs[char_lbls.index(i)])

        for event in pg.event.get():
            check_quit(event)

            for lbl in char_lbls:
                lbl.handle(event, SURFACE)
                if event.type == MOUSEBUTTONDOWN and lbl.rect.collidepoint(*event.pos):
                    # need to add the character's image to the selected box.
                    item = selected_char_imgs[char_lbls.index(lbl)]
                    box = chosen_boxes.index(get_selected())
                    chosen[box] = (item, get_selected())

                if event.type == MOUSEBUTTONDOWN and \
                        next_button.rect.collidepoint(*event.pos) and \
                        filled:
                    continue_ = False

            for box in chosen_boxes:
                box.handle(event)

        for pair in chosen:
            if pair == (None, None):
                break

            character, box = pair
            coords = box.topleft[0] + 10, box.topleft[1] + 17

            character.update_coords(coords)

            character.build_image(SURFACE, COLOURS['beige'], False)

            # pg.display.update()
        # print((str(num_selected) + "\n") * 10)

        SURFACE.blit(MAIN_GAME_STATE['CURSOR'], pg.mouse.get_pos())
        pg.display.update()
        CLOCK.tick(24)

    continue_ = True
    MAIN_GAME_STATE["AREA"] = database.Area.MAP
    MAIN_GAME_STATE["PLAYERS"] = get_characters_from_images([i[0] for i in chosen])


    gameplay.main()


def get_characters_from_images(images):
    """get and return an actual character type, not
    just an image of it.
    """

    names = [i.type_ for i in images]
    characters = []

    namestotypes = {
        'swordsman': class_.Swordsman,
        'angel': class_.Angel,
        'archer': class_.Archer,
        'spearman': class_.Spearman,
        'wizard': class_.Wizard,
    }

    num = 1

    for name in names:
        characters.append(namestotypes[name](num, MAIN_GAME_STATE, copy.copy(database.DEFAULT_WEAPONS[name])))
        num += 1

    return characters


class FakeWeapon:
    def __init__(self, colour):
        self.colour = colour


RECT_FUNCS = {
    0: lambda: None,
    1: new_game,
    2: lambda: None,
}


if __name__ == '__main__':
    main()
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

from database import ALL, COLOURS

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
import subprocess
import platform
import os

if os.getcwd().endswith('game'):
    os.chdir('..{0}updater'.format('\\' if os.name == 'nt' else '/'))

CMD = {
    'Windows':
    'auto_install.exe'
    if os.path.exists('auto_install.exe') else ' python auto_install.py',
    'Linux':
    'auto_install'
    if os.path.exists('auto_installl') else '/usr/bin/python3 auto_install.py'
}[platform.system()].split()

subprocess.Popen(CMD)
# kill the current process
raise SystemExit
"""
save.py- create game save for stickmans new world.

data: read_file
takes no arguments, and returns a data structure (dict)
of the save, without any of the classes.

write_file(data)
data must be a dict (or dict-like file like IniFile)
and write it to $HOME/.stickman_new_world/save/.smr-save on linux
or %USERPROFILE%/.stickman_new_world/save/.smr-save on windows

convert(data)
convert data from dict of strings to
actual stickman's new world data.
"""

import inifile
import os
import encrypt

from class_.inventory import InventoryHandler


def read_file():
    game_state = {}
    data_text, time = encrypt.decrypt()
    data_file = os.path.join(
        os.getenv('TMP'), '.save.ini') if os.name == 'nt' else '/tmp/.save.cfg'

    with open(data_file, 'w') as open_file:
        open_file.write(data_text)

    ini_file = inifile.IniFile(data_file)
    # print(ini_file.to_dict())

    keys = ini_file.keys()
    values = ini_file.values()

    for key, value in zip(keys, values):
        if '.' in key:
            # value is in a category
            klass, prop = key.split('.')
            #print(klass, prop)
            try:
                game_state[klass]
            except KeyError:
                game_state[klass] = {}

            game_state[klass][prop] = value

        else:
            game_state[key] = value

    return game_state


def write_file(data):
    if isinstance(data, dict):
        data = to_inifile(data)
    encrypt.encrypt(data)


def to_inifile(dict_):
    file_str = ''
    for key in dict_:
        file_str += '[{}]\n'.format(key)
        for i in dict_[key]:
            file_str += '{}={}\n'.format(i, dict_[key][i])
        file_str += '\n'
    return file_str


def make_inventory(dictionary):
    pos = []
    for i in dictionary:
        pos.append(int(i.split('x')[0]))
    maxx = max(pos)
    pos = []
    for i in dictionary:
        pos.append(int(i.split('x')[1]))
    maxy = max(pos)
    inv = InventoryHandler(maxx, maxy)
    inv.sort_dict(dictionary)
    return inv


if __name__ == '__main__':
    write_file(open('misc\\shello.ini').read())
    a = read_file()
    #print(a)
    #print(a['inventory'])
    #print(make_inventory(a['inventory']))
"""settings.py- displays and changes the settings
for stickman's new world.
if the user settings
"""
import tkinter as tk
import os
import json
import platform
try:
    import pwd
except ImportError:
    # the OS is not linux
    pass

__all__ = ['main', 'load_settings', 'save']

if platform.system() == 'Linux':
    os.getlogin = lambda: pwd.getpwuid(os.getuid())[0]

DEF_NAME = 'settings.json'
USR_NAME = '.stickman_new_world{0}user_settings.json'.format(
    '\\' if os.name == 'nt' else '/')
HOME = 'C:\\Users\\{}\\'.format(
    os.getlogin()) if os.name == 'nt' else '/home/{}/'.format(os.getlogin())
print(HOME)
print()

SETTINGS_FILE_PATH = {
    'posix':
    HOME + USR_NAME if os.path.exists(HOME + USR_NAME) else 'settings.json',
    'nt':
    HOME + USR_NAME if os.path.exists(HOME + USR_NAME) else 'settings.json'
}[os.name]

SETTINGS_FILE = open(SETTINGS_FILE_PATH).read()

USR_SAVE_PATH = HOME + '{0}.stickman_new_world{0}'.format(
    '\\' if os.name == 'nt' else '/')
USR_SAVE_FILE = HOME + USR_NAME

print(USR_SAVE_PATH)
print(SETTINGS_FILE_PATH)


def load_settings():
    settings = json.JSONDecoder().decode(SETTINGS_FILE)
    return settings


def main():
    root = tk.Tk()
    root.geometry('300x200')
    root.title('settings')
    root.protocol('WM_DELETE_WINDOW', lambda: save(usr_settings, root))

    settings = load_settings()
    settings_ = {}
    print(settings)
    for key, value in zip(settings, settings.values()):
        if isinstance(value, bool):
            settings_[key] = value
    settings = settings_
    print(settings)
    usr_settings = settings.copy()

    for i in usr_settings:
        var = tk.IntVar()
        var.set(usr_settings[i])
        usr_settings[i] = var

    for key, value, num in zip(settings, settings.values(), range(
            len(settings))):
        print(key, value, usr_settings)
        tk.Checkbutton(
            root, text=key, variable=usr_settings[key]).grid(
                row=num, sticky=tk.W)

    tk.mainloop()


def save(settings, win):

    for i in settings:
        # the settings are still IntVars
        var = bool(settings[i].get())
        # change them to normal ints
        settings[i] = var

    win.destroy()

    if not os.path.exists(USR_SAVE_PATH):
        os.mkdir(USR_SAVE_PATH)

    # i like having an indent, for when i look at it :)
    json_settings = json.dumps(settings, indent=4)

    with open(USR_SAVE_FILE, 'w') as settings_file:
        settings_file.write(json_settings)


main()
from pygame.locals import *
import pygame
import class_
import random


def closest(me, others):
    possible_destinations = others
    possible_destinations = [
        abs(me - destination) for destination in possible_destinations
    ]
    destination = min(possible_destinations)

    return others[possible_destinations.index(destination)]


print(
    closest(
        int(input('number: ')),
        eval(input('enter numbers to be closest to seperated by ,: '))))
from class_.events import *


def put_all(main_game_state, event):
    for sprite in main_game_state.sprites():
        sprite.internal_event(event)


def quit_all(main_game_state):
    put_all(main_game_state, Quit())
with open('../stickmanranger.log') as o:
    p = o.readlines()[-1]

with open('changes.html', 'r+') as o:
    d = o.readlines()
    import pprint
    pprint.pprint(d)
    index = d.index(
        '       </div> <!-- this is a comment just for automation.-->\n')
    #d.insert(index, '<br/>hiiiiiiii\n')
    d.insert(index, ''.join(('        <br>', p, '\n')))
    o.seek(0)
    o.write(''.join(d))
    o.truncate()
# -*- coding: utf-8 -*-
"""
auto_installer.py
this file downloads the new version of stickmanranger and installs it
"""
__author__ = 'Michael Gill'
__version__ = '0.0'

from queue import Queue
from platform import system
import tkinter as tk
import threading
import json
import ctypes
import sys
import urllib.request
import shutil
import tarfile
import os

Q = Queue()
PRINT_LOCK = threading.Lock()


class InstallWindow(tk.Frame):
    destroyed = False

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.protocol("WM_DELETE_WINDOW", self.cancel_install)
        self.master = master
        master.title('auto-updater')
        self.but = tk.Button(
            master, text='cancel', command=self.cancel_install)
        self.but.pack()
        self.but.place(relx=0.4, rely=0.7)
        self.pack()

    def cancel_install(self):
        self.destroyed = True
        self.master.destroy()

    def check_queue(self):
        if Q.empty():
            return False

        data = Q.get()
        # the versions have been loaded
        print('is "data" a dict?:', isinstance(data, dict))
        print('data:', data)
        if data is None:
            self.label = tk.Label(self.master, text='No updates available')
            self.label.pack()
            self.label.place(relx=0.0, rely=0.1)
            self.but.destroy()
            close_but = tk.Button(
                self.master, text='close', command=self.cancel_install)
            close_but.pack()
            close_but.place(relx=0.4, rely=0.7)

        if isinstance(data, dict):
            data_string = 'current version: {current version} available version: {available version}'.format(
                **data)
            print('before tk.Label')
            self.label = tk.Label(self.master, text=data_string)
            print('after tk.Label')
            self.label.pack()
            self.label.place(relx=0.0, rely=0.1)
            print('hello')
            self.install_but = tk.Button(
                self.master, text='install', command=lambda: run(self))
            print('helo again')
            self.install_but.pack()
            self.install_but.place(relx=0.2, rely=0.7)
            print('howdy')

        elif isinstance(data, str):
            self.label.destroy()
            self.label = tk.Label(self.master, text=data)
            self.label.pack()
            self.label.place(relx=0.0, rely=0.1)


if system() not in ('Linux', 'Windows'):
    raise TypeError('Not made for this %a' % system())

VER_URL = "https://drive.google.com/uc?export=download&id=17KGPTgF6xWKH3dk7Sd74niL548WU6Tts"
ARCHIVE_URL = "https://github.com/Michael78912/smnw-archives/blob/master/stickman's%20new%20world.tar.gz"
# temporary directory. use os.environ because it changes in windows
TEMP_PATH = '/tmp' if system() == 'Linux' else os.environ['TMP']
INSTALL_PATH = os.path.join(
    os.environ['HOME'], '.stickman\'s new world/') if system(
    ) == 'Linux' else "C:\\Program Files (x86)\\stickman\'s new world\\"


def run(obj):
    obj.install_but.destroy()
    obj.but.destroy()
    threading.Thread(target=main, daemon=True).start()


def main():

    Q.put('fetching stickmanranger.tar.gz...')
    with urllib.request.urlopen(ARCHIVE_URL,) as response, \
     open(os.path.join(TEMP_PATH, 'stickmanranger.tmp.tar.gz'), 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    if os.path.exists(INSTALL_PATH + 'game'):
        Q.put('removing previous installation')
        shutil.rmtree(INSTALL_PATH + 'game')

# extract all contents to the path
    Q.put('extracting contents')
    tarfile.open(os.path.join(
        TEMP_PATH,
        'stickmanranger.tmp.tar.gz')).extractall(INSTALL_PATH + 'game')
    Q.put('installation complete\nplease restart stickmans new world.')


def check():
    data = {}
    # VER_URL is a shared google drive link that has the current version of stickmanranger
    with urllib.request.urlopen(VER_URL) as response:
        version = response.read().decode()
    # decode the current version from "settings.json"
    current_version = json.JSONDecoder().decode(
        open('..{0}game{0}config{0}linux_config.json'.format(
            '\\' if os.name == 'nt' else '/')).read())['version']
    # if the version is the same
    with PRINT_LOCK:
        print(current_version, version)
    data['current version'] = current_version
    data['available version'] = version

    if data['current version'] == data['available version']:
        Q.put(None)
    else:
        Q.put(data)

    if current_version == version:
        with PRINT_LOCK:
            print('no new updates')
        return False


def start_thread():
    """
	starts the thread for the actual installation,
	and use main thread for window.
	"""
    root = tk.Tk()
    root.geometry('300x200')
    window = InstallWindow(root)
    # create thread for window, as mainloop cannot run other code at the same time
    install_thread = threading.Thread(target=check, daemon=True)
    install_thread.start()
    while not window.destroyed:
        try:
            window.check_queue()
        except:  # 'cancel' button has been clicked, continue
            ...
        if not window.destroyed: root.update()


def is_admin():
    """
	return true if the program was run as an  administrator
	code not by me. thanks Martín De la Fuente!
	https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
	"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def name_main(started_from_main_=False):
    global started_from_main
    started_from_main = started_from_main_
    if __name__ == '__main__':
        if system() == 'Windows':
            if is_admin():
                start_thread()

            else:
                # Re-run the program with admin rightsos.getlogin = lambda: pwd.getpwuid(os.getuid())[0]
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, __file__, None, 1)
        if system() == 'Linux':
            start_thread()


name_main()
