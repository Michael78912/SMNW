"""gameplay.py- main gameplay file.
handle all events in this file, display terrain, handle deaths, 
status effects, etc...
"""

from pygame.locals import QUIT, MOUSEBUTTONDOWN
import pygame as pg

from database import MAIN_GAME_STATE, PICS, ALL_LEVELS, Area

SURFACE = MAIN_GAME_STATE['MAIN_DISPLAY_SURF']

PLAY_AREA = pg.Rect((800, 400), (0, 0))
MENU_AREA = pg.Rect((800, 200), (0, 400))

CLOCK = pg.time.Clock()
FPS = 60

def main():
    """run the game, after the title screen."""
    continue_ = True
    menu = pg.Surface((800, 200))
    menu.fill((0, 255, 0))
    MAIN_GAME_STATE['MOUSEDOWN'] = False

    while continue_:
        MAIN_GAME_STATE['MOUSE_POS'] = pg.mouse.get_pos()
        events = [event for event in pg.event.get()]
        if MAIN_GAME_STATE['AREA'] == Area.MAP:
            draw_map()
            handle_map()

        elif MAIN_GAME_STATE['AREA'] == Area.STAGE:
            MAIN_GAME_STATE['STAGE'].update(events)
        
        MAIN_GAME_STATE['MAIN_DISPLAY_SURF'].blit(MAIN_GAME_STATE['CURSOR'], pg.mouse.get_pos())
        # MAIN_GAME_STATE['MAIN_DISPLAY_SURF'].blit(menu, (0, 400))
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