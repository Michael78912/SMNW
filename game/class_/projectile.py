"""class for representing a projectiile.
It is up to the class using the projectile to
stop it.
"""

import math
import pygame


class Projectile:
    """represents a projectile"""

    path = None
    dead = False
    pt1 = (0, 0)
    pt2 = (0, 0)
    slope = 0
    pos = (-1, -1)

    def __init__(self, image, path_factory, lifespan=1000):
        """if lifespan is -1, it can last forever."""
        self.image = image
        self.lifespan = lifespan
        self.path_factory = path_factory
        # self.pos = next(path_factory)

    def start(self, pt1, pt2):
        """start the projectile"""
        self.path = self.path_factory(pt1, pt2)
        self.pos = next(self.path)
        self.pt1 = pt1
        self.pt2 = pt2

        # m = y2 - y1 / x2 - x1
        try:
            self.slope = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
        except ZeroDivisionError:
            # undefined
            self.slope = None

    def draw(self, surf):
        """draw the projectile to surf"""
        if self.lifespan == 0:
            self.dead = True
            return
        self.lifespan -= 1
        surf.blit(self.image() if callable(
            self.image) else self.image, self.pos)
        self.pos = next(self.path)


class Arrow(Projectile):
    """class for an arrow shot from a bow."""
    _image = None

    @property
    def image(self):
        """get the image based on the angle of inclination."""
        return pygame.transform.rotate(
            self._image,
            math.degrees(math.atan(self.slope)),
        )

    @image.setter
    def image(self, value):
        """set _image instead of image."""
        self._image = value
