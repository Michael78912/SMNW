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
