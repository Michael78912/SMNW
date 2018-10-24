"""gameplay.py- main gameplay file.
handle all events in this file, display terrain, handle deaths, 
status effects, etc...
"""

from pygame.locals import QUIT, MOUSEBUTTONDOWN
import pygame as pg

from database import MAIN_GAME_STATE, PICS, ALL_LEVELS, Area

SURFACE = MAIN_GAME_STATE['MAIN_DISPLAY_SURF']

CLOCK = pg.time.Clock()
FPS = 30

def main():
    """run the game, after the title screen."""
    continue_ = True

    while continue_:
        if MAIN_GAME_STATE['AREA'] == Area.MAP:
            draw_map()
            handle_map()

        elif MAIN_GAME_STATE['AREA'] == Area.STAGE:
            print('moving onto the stage')
            MAIN_GAME_STATE['STAGE'].update()
        
        pg.display.update()

        CLOCK.tick(FPS)

def draw_map():
    """draw the map to the screen, and all stages."""
    SURFACE.blit(PICS['Maps']['complete'], (0, 0))
    for stage in ALL_LEVELS:
        stage.draw_on_map()

def handle_map():
    pos = pg.mouse.get_pos()
    print(pos)

    for stage in ALL_LEVELS:
        stage.check_hover(pos)

        for event in pg.event.get():
            check_quit(event)

            if event.type == MOUSEBUTTONDOWN and stage.rect.collidepoint(*event.pos):
                stage.init(MAIN_GAME_STATE)
                MAIN_GAME_STATE['STAGE'] = stage
                MAIN_GAME_STATE['AREA'] = Area.STAGE




def check_quit(event):
    """check if event is a quit event. if it is, quit."""
    if event.type == QUIT:
        pg.quit()
        raise SystemExit