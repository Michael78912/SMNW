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
