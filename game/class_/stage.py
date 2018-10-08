import pygame as pg
import os

WHITE = (255, 255, 255)  # unbeaten
GRAY = (211, 211, 211)  # beaten
TEAL = (0, 128, 128)  # peaceful
STAGE_SIZE = (10, 10)


class Stage:
    unlocked = False
    beaten = False

    def __init__(
            self,
            position_on_map,
            # (x, y) cartesian system
            all_screens,
            # list\tuple of all screens in stage
            boss_screen,
            # the screen of the boss
            terrain,
            # the terrain class
            comes_from,
            # stage that you beat to unlock it (first level is None, shouldn't
            # ned to put None again)
            surface,
            # map that the stage must be drawn on
            peaceful=False,
            # peaceful stage is a shop or of the like
            has_icon=True,
            # False if level shows upon map already, or is secret
            links_to=None,
            # list\tuple of all stages it links to,
            decorations=(),
            # tuple of decorations to be drawn
    ):
        if comes_from is None:
            comes_from = _NullStage

        self.position_on_map = position_on_map
        self.all_screens = all_screens
        self.comes_from = comes_from
        self.drawing_surface = surface
        self.peaceful = peaceful
        self.has_icon = has_icon
        self.links_to = links_to
        self.terrain = terrain
        self.decorations = decorations
        # print(os.getcwd())
        with open(os.path.join(
            os.getcwd(), 'music', 'smnwgameplay.mp3'
        )):
            print('opened successfully')
        self.music = os.path.join('music', 'smnwgameplay.mp3')

        if comes_from.beaten and has_icon:
            pg.draw.rect(surface, WHITE, position_on_map + STAGE_SIZE)

        elif self.beaten and has_icon:
            pg.draw.rect(surface, GRAY, position_on_map + STAGE_SIZE)

        elif peaceful and has_icon:
            pg.draw.rect(surface, TEAL, position_on_map + STAGE_SIZE)

    def start(self):
        pg.music.stop()
        pg.music.load(self.music)
        pg.music.play()


class _NullStage:
    position_on_map = None
    all_screens = None
    comes_from = None
    drawing_surface = None
    peaceful = None
    has_icon = None
    links_to = None
    beaten = True
