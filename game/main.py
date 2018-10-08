#!/usr/bin/python3
# main.py
"""
the main code for the game stickman ranger, a game similar to stick ranger(www.dan-ball.jp/en/javagame/ranger)
the goal is to defeat bosses and not get killed.
project started: oct. 20, 2017. 
first level release goal: march 1, 2018
source code by Michael Gill
original SR by Ha55ii

this game is built on pygame, an excellent game engine for python
thanks to paint.net, which I made the sprites on.

UPDATE: May 18
Oh my goodness i look back at this code after so long of ignoring main.py
i kind of hate this module now.
oh well, it works, i suppose. for now
By the way, i wasnt even close to my intended release date :)
"""

__author__ = 'Michael Gill'
__version__ = '0.0'
__all__ = ['draw_box', 'draw_text', 'terminate', 'main']

import sys
import time

from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
import pygame as pg

# local imports
#import save
import database
import class_
import dicts
from dicts import COLOURS
import check_update

### constant values ###

##### IMPORTANT! REMEMBER CARTESIAN SYSTEM! ######
##### 0 FOR BOTH COORDINATES START IN TOP LEFT ###

NUM_OF_CHARS = 4

###functionality begins here! (YAY! FINALLY)###


def main():
    """
    main functionality begins here
    """
    check_update.main()

    global CLOCK, SURFACE, PICS
    flag = True
    # for stopping the game loop when clicked, stop clutter.

    pg.init()

    PICS = dicts.gather_pics('data')
    print(PICS)
    SURFACE = database.SURFACE
    CLOCK = pg.time.Clock()

    pg.display.set_caption('StickMan Ranger')
    pg.display.set_icon(PICS['game_icon'])

    SURFACE.blit(PICS['Title_Screen'], (0, 0))

    while flag:  # main loop:
        for ev in pg.event.get():
            if ev.type == QUIT:
                terminate()
            elif ev.type == MOUSEBUTTONDOWN:
                cho = choose_game_mode()
                flag = False
        pg.display.update()
    print('main event loop terminated')
    # print functions in this code are for debugging purposes only

    if cho is 0:
        char_list = get_keys_from_pics(get_characters())
        clear_screen()
        char_string = '\n'.join(char_list)
        draw_text(char_string, size=45)
        SURFACE.blit(PICS['Maps']['half_complete'], (0, 0))

        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    terminate()
            pg.display.update()


def choose_game_mode() -> int:
    """
    choose which option the player wants
    return 1 if player chooses new game
    return 2 if player chooses load game
    return 3 if player chooses load a backup.
    """
    print('choose_game_mode called')
    SURFACE.fill(COLOURS['white'])

    # I realize now that Ishould have used a function for the three sections
    # below, but whatever.
    LabelPlay = pg.font.Font('data\\Michael`s Font.ttf', 32)
    PlaySurf = LabelPlay.render('New Game', True, COLOURS['black'],
                                COLOURS['white'])
    PlayRect = class_.MyRect(PlaySurf.get_rect())
    PlayRect.center = ((WIN_X // 2), (WIN_Y // 2) - 50)
    SURFACE.blit(PlaySurf, PlayRect)

    #################################################################

    LabelLoad = pg.font.Font('data\\Michael`s Font.ttf', 32)
    LoadSurf = LabelLoad.render('Load Game', True, COLOURS['black'],
                                COLOURS['white'])
    LoadRect = class_.MyRect(LoadSurf.get_rect())
    LoadRect.center = (WIN_X // 2, WIN_Y // 2)
    SURFACE.blit(LoadSurf, LoadRect)

    #################################################################

    LabelLoadEarlier = pg.font.Font('data\\Michael`s Font.ttf', 32)
    LESurf = LabelLoadEarlier.render('Load Earlier Save', True,
                                     COLOURS['black'], COLOURS['white'])
    LERect = class_.MyRect(LESurf.get_rect())
    LERect.center = (WIN_X // 2, WIN_Y // 2 + 50)
    SURFACE.blit(LESurf, LERect)

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == MOUSEMOTION:
                x, y = event.pos
                for (rect, surf) in ((PlayRect, PlaySurf),
                                     (LoadRect, LoadSurf), (LERect, LESurf)):
                    rect.handle(event, SURFACE, surf)

            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if PlayRect.collidepoint(x, y):
                    print("PlayRect Clicked")
                    return 0  # these return value, and end loop

                elif LoadRect.collidepoint(x, y):
                    print("LoadRect Called")
                    return 1

                elif LERect.collidepoint(x, y):
                    print("LERect called")
                    return 2

            pg.display.update()


def draw_text(
        text,
        size=32,
        cen_of_txt=(WIN_X // 2, WIN_Y // 2),
        colour=(COLOURS['black'], COLOURS['white']),
) -> tuple:
    """
    function for drawing text on SURFACE,
    returns a tuple containing the rect
    of the surface, and the surface 
    itself.
    """
    FontObj = pg.font.Font('data\\Michael`s Font.ttf', size)
    FontSurf = FontObj.render(text, True, *colour)
    Rect = FontSurf.get_rect()
    Rect.center = cen_of_txt
    SURFACE.blit(FontSurf, Rect)
    return class_.MyRect(Rect, colour=COLOURS['white']), FontSurf


def draw_box(size, colour, pos, alpha=None, image=None) -> tuple:
    """
    return a square rectangle, surface pair
    uses MyRect
    """
    print(pos)
    new_surf = pg.surface.Surface(size)
    new_surf.fill(colour)

    if alpha is not None:
        new_surf.set_alpha(alpha)

    SURFACE.blit(new_surf, pos)

    if image is not None:
        SURFACE.blit(image, pos)

    return class_.MyRect(
        new_surf.get_rect(topleft=pos), colour=colour), new_surf


def terminate():
    "end the current pygame program"
    # need to  save the game... put some function call
    pg.quit()
    sys.exit()


def get_characters() -> list:
    """
    starts a new game,
    and lets the player choose
    their characters.
    returns a list of the characters
    the player has chosen.
    """
    SURFACE.fill(COLOURS['white'])

    draw_text(
        'Choose your players:', cen_of_txt=(WIN_X // 2, WIN_Y // 2 - 200))

    texts = {}
    pairs = []
    num = -250  # this is the starting point for the images to appear

    # puts all the characters in a line with their caption beneath
    for string in database.ALL_CLASSES:
        string = string.lower()
        texts[string] = draw_text(
            string, size=20, cen_of_txt=(WIN_X // 2 + num, WIN_Y // 2 + 200))

        pic = PICS['characters'][string]
        SURFACE.blit(pic, (texts[string][0].x + 20, texts[string][0].y + 30))

        pairs.append((string, class_.MyRect(pic.get_rect())))
        num += 100

    del num, string

    box_list = []

    # this loop puts 4 boxes to show which characters the user has chosen
    for i in range(WIN_X // 4, WIN_X // 4 * 3, 100):
        box_list.append((draw_box(
            (25, 25), COLOURS['gray'], (i, WIN_Y // 2), alpha=200),
                         (i, WIN_Y // 2))[0][0])

    del i

    print('pairs: ', *pairs, sep='\n')

    char_list = []
    clicked = 0
    boxes_with_pictures = []
    box_num_pairs = {
        1: box_list[0],
        2: box_list[1],
        3: box_list[2],
        4: box_list[3],
    }
    for key in box_num_pairs:
        print('key: ', key, ' box: ', box_num_pairs[key], sep='')

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == MOUSEMOTION:
                for key in texts:
                    M = texts[key]
                    M[0].handle(event, SURFACE, M[1])

            # this branch controls when a selection box is
            # selected, which one to underline.
            elif event.type == MOUSEBUTTONDOWN:  # if mouse is clicked
                x, y = event.pos

                for key, rect in zip(box_num_pairs.keys(),
                                     box_num_pairs.values()):
                    print(rect is box_num_pairs[key])

                    if rect.collidepoint(x, y):
                        # if click is in 'rect'
                        if not rect.underlined:
                            # only do this is 'rect' is underlined
                            rect.underline(SURFACE)

                        if clicked == key:
                            box_num_pairs[clicked].remove_underline(SURFACE)
                            clicked = 0

                        elif clicked == 0:
                            clicked = key

                        else:
                            box_num_pairs[clicked].remove_underline(SURFACE)
                            clicked = key

                for rect_key, rect in zip(box_num_pairs.keys(),
                                          box_num_pairs.values()):

                    for character_name, rect_surf_pair in zip(
                            texts.keys(), texts.values()):

                        if rect_surf_pair[0].collidepoint(x, y):
                            print('garpenchank')
                            try:
                                box_num_pairs[clicked].draw_inside(
                                    PICS['characters'][character_name],
                                    SURFACE)
                                boxes_with_pictures.append(clicked)

                            except (class_.SMRError, KeyError) as error:
                                print(error)

                            break

                        elif clicked in boxes_with_pictures:
                            print('gud')
                            box_num_pairs[clicked].remove_pic(SURFACE)

                        char_list = [
                            box.PicInside for box in box_num_pairs.values()
                        ]

        pg.display.update()

        if not None in char_list[:2]:
            print('howdy')
            char_list = [box.PicInside for box in box_num_pairs.values()]
        if not None in char_list:
            return char_list


def clear_box(pos):
    """
    clears the box that needs to be cleared.
    """

    print('in the function clear_box')

    draw_box((25, 25), COLOURS['white'], pos)
    draw_box((25, 25), COLOURS['gray'], pos, alpha=100)


def change_colour_surface(surface, r, g, b):
    """changes the colour of all parts of a 
    surface except for the transparent parts.
    """
    arr = pg.surfarray.pixels3d(surface)
    arr[:, :, 0] = r
    arr[:, :, 1] = g
    arr[:, :, 2] = b


def get_keys_from_pics(orig_list):
    """
    returns a dict that has keys of the original
    dict that the pics were contained in. for example:
    get_keys_from_pics(gladiator_pic) 
    will return:
    {'gladiator': <class 'pygame.Surface' object>}
    note: if an item doesnt match, for example a 
    string, or a picture not in data/characters,
    nothing will be done with it.
    """
    pics_dict = PICS['characters']
    new_dict = {}

    for key, value in zip(pics_dict.keys(), pics_dict.values()):
        for picture in orig_list:
            if picture == value:
                new_dict[key] = value

    return new_dict


def clear_screen():
    return SURFACE.fill(COLOURS['white'])


if __name__ == '__main__':
    main()

else:
    print('why on earth are you importing this?\n\
        it is supposed to a main module!')
