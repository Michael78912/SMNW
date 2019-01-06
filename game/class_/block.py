"""a block is a segment of the terrain grid in SMNWself.
they can be indestructible, or take damage in the same way enemies do.
the possibilities are endless with blocks!
"""

import collections
import logging
import warnings

import pygame

try:
    from ._internal import PICS, change_colour_surface
except ImportError:
    from _internal import PICS, change_colour_surface


def block(string, template, airsurf, watersurf, pos):
    """return the proper block given template
    and string.
    """
    top = '*'
    # we can use this to determine simple blocks.
    # it will give None if it is something else.
    obj = collections.defaultdict(
        lambda: lambda: None,
        {
            '~': lambda: Air(pos, airsurf),
            '-': lambda: Water(pos, watersurf),
            '+': lambda: TopWater(pos, watersurf.get_at((0, 0))[0:-1], airsurf),
        }
    )[string]()

    if obj is None:
        # the string should be '#' or '*'.
        assert string in '*#', "This should be either * (top) or # (ground)"
        # return the proper block based on the template.
        # if string is top then use top = true
        return TEMPLATES[template](pos, string == top)
    return obj


class Block:
    """base class for all blocks in SMNW."""
    image = None
    solid = 0
    top = False
    # equivalent to "health" on enemies/characters. set to -1 to be indestructible.
    hardness = 30

    def __init__(self, pos):
        self.pos = pos

    def size_image(self, size):
        """get and return the proper size of image."""
        # always scale to a square
        return pygame.transform.scale(self.image, (size, size))

    def get_rect(self, size):
        """get and return a pygame.Rect object representing
        the block.
        """
        return pygame.Rect(self.pos[0] * size, self.pos[1] * size, size, size)

    def __repr__(self):
        return "{}(top={})".format(self.__class__.__name__, self.top)


class SolidBlock(Block):
    """ all solid blocks (* or #) will be devied from this class.
    image will return different if it is top or not, so set _image instead
    of image.
    """
    _image = {'0': None, '1': None}

    def __init__(self, pos, top=False):
        super().__init__(pos)
        self.top = top

    # we need to use a property to choose the right image.
    @property
    def image(self):
        """return top image if it is top, else the normal one."""
        if self.top:
            return self._image['0']
        return self._image['1']


class Air(Block):
    """air is a transparent, unbreakable block present in the absence of others."""
    solid = 2
    hardness = -1

    def __init__(self, pos, image):
        super().__init__(pos)
        self.image = image


class Water(Block):
    """half-solid, unbreakable liquid. essential to all life on earth."""
    solid = 0.5
    hardness = -1

    def __init__(self, pos, image):
        super().__init__(pos)
        self.image = image


class TopWater(Water):
    """exactly the same as its normal couterpart, except slightly more
    stupid looking.
    """
    top = True

    def __init__(self, pos, colour, air_surface):
        super().__init__(pos, change_colour_surface(
            PICS['Other']['top_water'].copy(),
            *colour,
        ))
        image = air_surface.copy()
        image.blit(self.image, (0, 0))
        self.image = image


class Stone(SolidBlock):
    """tough boi"""
    hardness = 100
    _image = PICS['terrain_templates']['stone']


class Dirt(SolidBlock):
    """don't let it get on your shirt!"""
    _image = PICS['terrain_templates']['dirt']


class Dirt2(Dirt):
    """a slightly-less dirty dirt."""
    _image = PICS['terrain_templates']['light_dirt']


class HellStone(SolidBlock):
    """a very hell-like stone."""
    _image = PICS['terrain_templates']['hellstone']

class Sand(SolidBlock):
    """
    Warning: do not take your camera to the beach.

    ##############################################
    #             Dramatic Flashback             #
    ##############################################
    July 2018, Ocean Shores, WA.
    A lovely family holiday we were taking. straight from Kelowna
    to Victoria, then down to the states for a bit. We stopped in a nice
    town called Ocean Shores. It had some nice beaches. One day, we decided
    to walk on a beach. I brought my camera, and took some really nice pictures,
    of the waves, the gulls, and the shells. It was a windy day, and the sand was
    spraying all around us. unbeknownst to me, some insidious sand found its way into
    my poor camera's lens, and disabled it for life. I now have no camera. :(
    """

    def __init__(self, pos, top=False, camera=False):
        super().__init__(pos, top)
        if camera:
            warnings.warn(
                "NOOOOOOOOOOOOOOOOOO DON'T BRING YOUR CAMERA TO THE BEACH")
            logging.warning(
                "I'M TELLING YOU YOU'RE GOING TO BREAK YOUR CAMERA")

    _image = PICS['terrain_templates']['sand']


TEMPLATES = {
    'sand': Sand,
    'dirt': Dirt,
    'light_dirt': Dirt2,
    'stone': Stone,
    'hellstone': HellStone,
}


if __name__ == "__main__":
    pass
