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
