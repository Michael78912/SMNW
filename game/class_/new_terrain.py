"""an improvement to the deprecated "terrain" module.
it uses the Block class rather than just strings, which are
now mutable, and easier to use, and change. it also uses blocks based
off of real materials; for example if the template is "sand" it will
actually use a block called "Sand". (Mostly inspired by Minecraft's block system)
"""

__all__ = ['Terrain']

import re
import time

import numpy
import pygame
from lark import Lark, Transformer

import block

# screen size for actual gameplay
X, Y = 800, 400

HEADER_GRAMAMAR = r"""
?start : header

number : NUMBER

?header : "@" [assignment ("|" assignment)*]
?assignment : assignment_air | assignment_water | assignment_size
assignment_water : "water"i "=" colour
assignment_size : "size"i "=" number
assignment_air : "air"i "=" colour

colour : "(" [number "," number "," number ("," number)?] ")"

NUMBER : /[0-9]/+

COMMENT : ";" /[^\n]/*


%import common.WS
%ignore WS
%ignore COMMENT
"""


class Terrain:
    """default handler for terrain in SMNW."""
    raw = ''
    file = ''
    grid = None
    size = 10
    air = (0, 0, 0)
    water = (0, 0, 128)

    def check_validity(self):
        """check the validity of all given data so far"""
        # check to make sure aall blocks will fit on the screen
        assert X % self.size == 0 and Y % self.size == 0, "Block size is not valid"
        # check to see if any colours exceed valid range
        assert any(not (x > 255 or x < 0) for x in self.air + self.water), \
            "Invalid colour given. air: {} water: {}".format(
                self.air, self.water)

    def __init__(self):
        pass

    def __repr__(self):
        return "Terrain With {.size = {size},\
         .air = {air}, .water = {water}, .file = {file}}".format(**self.__dict__)

    def __str__(self):
        # basically just return the terrain file (stripped of comments)
        return self.raw

    def __getitem__(self, key):
        # take a block ID or position, and return the block with that ID
        pass

    def __setitem__(self, pos, value):
        # take a position and set it to a new block
        pass

    def load(self, file, template):
        """load from file. create an array that contains
        as many blocks as nessecary.
        """

        self.file = file

        # large chunk of data
        data = file.read()

        # create parser used for pulling data from the header.
        header_parser = Lark(HEADER_GRAMAMAR)

        # find the header, and create an AST from the found header.
        header = re.search(r'@.*', data)
        tree = header_parser.parse(header.group(0))

        # use the data from the header to transform the terrain object
        # accordingly.
        HeaderTransformer(self).transform(tree)

        # make sure al data is OK.
        self.check_validity()

        # create new array for containing the blocks.
        y = 0
        self.grid = numpy.empty(shape=(Y // self.size, X //
                                       self.size), dtype=block.Block)

        airsurf = pygame.Surface((10, 10))
        airsurf.fill(self.air)

        watersurf = pygame.Surface((10, 10))
        watersurf.fill(self.water)

        # iterate through all lines.
        for line in data.split('\n'):
            x = 0
            if line.startswith((';', '@')):
                # entire comment/header line. continue
                continue

            # remove a comment if there is one
            line = line.split(';')[0].strip()
            if not line:
                # blank line
                continue

            # iterate through each character in the line
            for item in line:
                self.raw += line + '\n'
                try:
                    self.grid[y][x] = block.block(
                        item, template, airsurf, watersurf, (x, y))
                except AssertionError:
                    # not implemented, replace a pit/sign with air for now.
                    self.grid[y][x] = block.Air((x, y), airsurf)
                x += 1
            y += 1

    def build(self):
        """build surface"""
        image = pygame.Surface((X, Y))

        time1 = time.time()
        for y in range(0, Y // self.size):
            for x in range(0, X // self.size):
                current_block = self.grid[y][x]
                image.blit(current_block.image,
                           current_block.get_rect(self.size))

        time2 = time.time()
        print('took', time2 - time1, 'seconds to build')

        return image


class HeaderTransformer(Transformer):
    """transforms tokens into an actual terrain object"""

    colour = tuple

    def __init__(self, terrain_obj):
        super().__init__()
        self.terrain = terrain_obj

    def assignment_air(self, args):
        """get air colours"""
        self.terrain.air = args[0]

    def assignment_water(self, args):
        """get  water colours"""
        self.terrain.water = args[0]

    def assignment_size(self, args):
        """get size"""
        self.terrain.size = args[0]

    @staticmethod
    def number(val):
        """convert colour list to tuple"""
        return int(val[0])


def main():
    """test function"""
    terrain = Terrain()
    terrain.load(open('terrains\\flattish.smr-terrain'), 'dirt')
    pygame.image.save(terrain.build(), "howdy.png")


if __name__ == "__main__":
    main()
