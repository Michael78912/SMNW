import itertools
import math

import pygame

"""paths.py
classes for generating projectile paths, given two points.
"""

def _undefined_line(pt):
    """use for an undefined line (m=undefined)."""
    x, y = pt
    while True:
        yield (x, y)
        y += 1
    



def _line(pt1, pt2):
    x1, y1, x2, y2 = pt1 + pt2

    try:
        m = (y2 - y1) / (x2 - x1)
    except ZeroDivisionError:
        # division by zero. use a special function for this purpose only.
        yield from _undefined_line(pt1)
        return
    backwards = x1 > x2
    x_generator = _count(x1, backwards)

    pts = []
    prev_y = y1

    for x in x_generator:
        y = round(m * (x - x1) + y1)
        for new_y in range(prev_y, y):
            yield (x, new_y)
        yield (x, y)
        prev_y = y

def _count(start=0, down=False):
    """start at start, and constantly count.
    normally, go up, unless down is true.
    """
    def countdown():
        x = start
        while True:
            yield x
            x -= 1
    
    def countup():
        x = start
        while True:
            yield x
            x += 1
    
    yield from (countdown() if down else countup())


class Line:
    """draws a straight line."""
    last_pt = (0, 0)
    second_last_pt = (0, 0)
    def __init__(self, pt1, pt2):
        """initiate line"""
        self.x1, self.y1, self.x2, self.y1 = pt1 + pt2
        self.pt1 = pt1
        self.pt2 = pt2
        self.line = _line(pt1, pt2)
    
    def __next__(self):
        return next(self.line)
    
    def __iter__(self):
        """yield the lines, using _line.
        hold on to the previous points.
        """

        yield from self.line
    
    def _slope(self) -> float:
        """get and return the slope."""
        #     y2 - y1
        # m = -------
        #     x2 - x1
        return (self.y2 - self.y1) / (self.x2 - self.x1)
    
    def get_angle(self) -> float:
        """calculate and return the angle of inclination."""
        return math.atan(self._slope())

    


pts = []

display = pygame.display.set_mode((1000, 800))
display.fill((255, 255, 255))
while True:
    if len(pts) == 2: break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pts.append(event.pos)
    
    pygame.display.update()

d = Line(*pts)
c = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
    pygame.display.update()
    # c.tick(60)
    display.set_at(next(d), (0, 0, 0))