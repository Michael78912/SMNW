"""a replacement and better written file than main.py.
for starting the game.
"""

from argparse import Namespace
import enum
import os


from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION
import pygame as pg

from class_.character_image import CharacterImage
from database import COLOURS
import database
import class_
import picture_collect

# window sizes
WIN_X, WIN_Y = 800, 600
MID_X = WIN_X // 2
MID_Y = WIN_X // 2
CENTRE = MID_X, MID_Y

WHITE = COLOURS['white']
BLACK = COLOURS['black']

FPS = 60

PICS = picture_collect.gather_pics('data')


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

s = pg.Surface((100, 100))
d = pg.Surface((10, 10))
d.fill(BLACK)
_border(d, WHITE)
# pg.image.save(d, r'C:\Users\Michael\Desktop\test_images\howdy.png')

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

    def draw(self, surf):
        """draw the box to the screen."""

        top, left = self.topleft
        rect = pg.Rect((top, left), (self.width, self.height))

        


        

        if self.selected:
            # make the box red instead.
            pg.draw.rect(surf, COLOURS['red'], rect, 1)

        else:
            pg.draw.rect(surf, self.colour, rect, 1)

        if self.image is not None:
            img_rect = self.image.get_rect()
            img_rect.center = rect.center

    def handle(self, event, *args, **kwargs):
        """handle the event. if it is clicked on, then call and return
        self.onclick. if not, do nothing.
        """

        return self.onclick(*args, **kwargs)




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
        print(pg.mouse.get_pos())
        print(self.rect.topleft)

        if mouseover:
            print('shading')
            self._shade()
            self.shaded = True

        else:
            self.shaded = False

        if self.underlined:
            start, end = self.rect.bottomleft, self.rect.bottomright
            pg.draw.line(surface, self.forecolour, start, end)

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
        for event in pg.event.get():
            check_quit(event)

            if event.type == MOUSEBUTTONDOWN:
                # on to the next loop
                continue_ = not continue_
        pg.display.update()

    func = lambda: None
    continue_ = True

    while continue_:
        SURFACE.blit(PICS['menu_background'], (0, 0))
        rects = draw_choices()
        for event in pg.event.get():
            check_quit(event)

            if event.type == MOUSEBUTTONDOWN:
                # mouse clicked
                for rect, _, num in rects:
                    # if the rect was clicked on
                    if rect.collidepoint(*event.pos):
                        # set func to proper function
                        func = RECT_FUNCS[num]
                        # stop while loop
                        continue_ = not continue_

            elif event.type == MOUSEMOTION:
                # mouse moved
                for rect, surf, num in rects:
                    # handle shading of rectangle hovered over
                    rect.handle(event, SURFACE, surf)
            # update display. needs to be in the for loop to avoid
            
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

    centre_x, centre_y = SURFACE.get_rect().center
    print(centre_x, centre_y)

    label("Stickman's New World", centre_x, 100, size=60)

    choices = [
        drawopt('New Game', centre_x, centre_y - 50, 1),
        drawopt('Load Game', centre_x, centre_y, 2),
        drawopt('Settings', centre_x, centre_y + 50, 3)
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
                       None, None
                       ),
        CharacterImage('angel',
                       Namespace(colour='gold'),
                       (START_X + 150, START_Y),
                       None, None
                       ),
        CharacterImage('archer',
                       Namespace(colour='brown'),
                       (START_X + 300, START_Y),
                       None, None,
                       ),
        CharacterImage('spearman',
                       Namespace(colour='grey'),
                       (START_X + 450, START_Y),
                       None, None,
                       ),
        CharacterImage('wizard',
                       Namespace(colour='blue'),
                       (START_X + 600, START_Y),
                       None, None,
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

    chosen = []

    def set_(box):
        box.selected = not box.selected

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
            if i.selected: return i

    continue_ = True
    num_selected = 0

    while continue_:
        SURFACE.blit(PICS['menu_background'], (0, 0))
        label('Choose your players:', MID_X, 75, 60)
        for box in chosen_boxes:
            box.draw(SURFACE)

        for i in char_imgs:
            i.build_image(SURFACE)

        for i in char_lbls:
            i.draw(SURFACE)
            if i.underlined:
                add_chosen(char_lbls, i, char_imgs[char_lbls.index(i)])

        for event in pg.event.get():
            check_quit(event)

            for lbl in char_lbls:
                lbl.handle(event, SURFACE)
                # label.update(SURFACE)

            # pg.display.update()
        print((str(num_selected) + "\n") * 10)

        pg.display.update()
        CLOCK.tick(30)


def add_chosen(box, character):
    """add a chosen player to the selected boxes."""


class MutableCarrier:
    """can carry an object, and have it be changed."""
    def __init__(self, item):
        self.item = item


RECT_FUNCS = {
    0: lambda: None,
    1: new_game,

}


if __name__ == '__main__':
    main()
