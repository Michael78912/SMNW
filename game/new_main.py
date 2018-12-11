"""a replacement and better written file than main.py.
for starting the game.
"""

from argparse import Namespace
import copy
import logging
import os

# pylint: disable=no-name-in-module

from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION
import pygame as pg

import logs
from class_.character_image import CharacterImage
import class_
from database import COLOURS, MAIN_GAME_STATE, Area
import database
import gameplay
import terminal


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
    logging.debug('starting game')

    while continue_:
        if MAIN_GAME_STATE.get('TERMINAL') is not None:
            MAIN_GAME_STATE['TERMINAL'].threaded_update()
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
        
        if MAIN_GAME_STATE.get('TERMINAL') is not None:
            MAIN_GAME_STATE['TERMINAL'].threaded_update()

        if MAIN_GAME_STATE['AREA'] == Area.MAP:
            gameplay.main()
            continue_ = False

        label("Stickman's New World", CENTRE_X, 100, size=60)

        for lbl in rects:
            lbl.draw(SURFACE)
        for event in pg.event.get():
            check_quit(event)
            terminal.handle(event)

            for lbl in rects:
                lbl.handle(event, SURFACE)

                if event.type == MOUSEBUTTONDOWN and lbl.rect.collidepoint(*event.pos):
                    func = lbl.function
                    continue_ = False

        if MAIN_GAME_STATE.get('TERMINAL') is not None:
            MAIN_GAME_STATE['TERMINAL'].threaded_update()

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
        if MAIN_GAME_STATE['AREA'] != Area.TITLE:
            gameplay.main()
            continue_ = False
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

        for event in pg.event.get():
            check_quit(event)
            terminal.handle(event)

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

        if MAIN_GAME_STATE.get('TERMINAL') is not None:
            MAIN_GAME_STATE['TERMINAL'].threaded_update()
        
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
    try:
        main()
    except Exception:
        logging.exception("Exception Encountered")
        logging.debug('exiting game.')
        raise
    except SystemExit:
        logging.debug('exiting game.')
