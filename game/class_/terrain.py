
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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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
                        (index2 * self.size - 20, index1 * self.size - 10))

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
# !w/ np- 66.2 seconds


def _main(image='dirt', template='flat'):
    terrain = Terrain(image=image, template=template, use_numpy=1)
    print(Terrain.terrain2dlist_texts)
    print(Terrain.terrain2dlist_texts[template])
    pic = terrain.build_surface()

    import pygame
    a = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('terrain viewer')
    pygame.display.set_icon(PICS['Other']['next'])
    a.blit(pic, (0, 0))
    print('\n' * 100)
    # for i in range(1000):
    # 	for a in terrain.terrain2dlist_texts['flat']['text']:
    # 		for i in a:
    # 			print(i)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.stdout.close()
                sys.stderr.close()
                raise SystemExit
        pygame.display.update()


def proc(args):
    file = args[1].split('.')[0].split('\\' if os.name == 'nt' else '/')[-1]
    print(file)
    try:
        opt = args[2]

    except IndexError:
        opt = 'stone'

    _main(template=file, image=opt)


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

if __name__ == '__main__':
    if len(sys.argv) != 1:
        proc(sys.argv)
    else:
        saveall()
