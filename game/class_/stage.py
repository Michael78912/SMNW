from threading import Thread

from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN
import pygame as pg
import os

from . import screen


WHITE = (255, 255, 255)  # unbeaten
GRAY = (211, 211, 211)  # beaten
TEAL = (0, 128, 128)  # peaceful
YELLOW = (128, 128, 0)
BLACK = (0, 0, 0)
STAGE_SIZE = (15, 15)


class Stage:
    unlocked = False
    beaten = False
    rect_padding = 8
    game_state = {}

    def __init__(
            self,
            name,
            # name to be used by the game
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
        self.name = name
        self.terrain = terrain
        self.decorations = decorations
        # print(os.getcwd())
        with open(os.path.join(
            os.getcwd(), 'music', 'smnwgameplay.mp3'
        )):
            print('opened successfully')

        self.music = os.path.join('music', 'smnwgameplay.mp3')

        self.rect = pg.Rect(position_on_map, STAGE_SIZE)

        rect = self.rect
        left, top, width, height = rect.left, rect.top, rect.width, rect.height
        self.box = pg.Rect(left - self.rect_padding, top - self.rect_padding,
                width + (self.rect_padding * 2), height + (self.rect_padding * 2)
            )

    def draw_on_map(self):
        surface = self.drawing_surface

        if self.comes_from.beaten and self.has_icon:
            self.rect = pg.draw.rect(
                surface, WHITE, self.position_on_map + STAGE_SIZE)

        elif self.beaten and self.has_icon:
            self.rect = pg.draw.rect(
                surface, GRAY, self.position_on_map + STAGE_SIZE)

        if self.peaceful and self.has_icon:
            self.rect = pg.draw.rect(
                surface, TEAL, self.position_on_map + STAGE_SIZE)

    def check_hover(self, pos):
        """check to see if the mouse is hovering over. if it is,
        dislpay a box around the level, and a name.
        """

        # print(left, top, width, height)

        if self.box.collidepoint(*pos):
            box = self.box
            pg.draw.rect(self.drawing_surface, YELLOW, box, 1)

            fontobj = pg.font.Font(os.path.join('data', 'MICHAEL`S FONT.ttf'), 20)
            fontobj.set_bold(True)
            surf = fontobj.render(self.name, True, BLACK)
            surfrect = surf.get_rect()
            surfrect.center = pos[0], pos[1] - 40

            self.drawing_surface.blit(surf, surfrect)


     

    def start_music(self):
        """stop old music, play new music."""
        if not self.peaceful:
            # keep the theme music if it is a peaceful screen.
            pg.mixer.music.fadeout(2000)
            print('howdy?')
            pg.mixer.music.load(self.music)
            pg.mixer.music.play(-1)

    def init(self, game_state):
        """run the stage."""
        self.game_state = game_state
        Thread(target=self.start_music).start()
        game_state['_STAGE_DATA'] = {
            'screen_number': 0,
            'screen': self.all_screens[0],
            'stage': self,
        }

    def update(self, events):
        """update the stage, and everything related to it."""
        state = self.game_state

        terrain_surf = self.terrain.built_image if self.terrain.built_image is not None else self.terrain.build()
        

        display = state['MAIN_DISPLAY_SURF']

        display.fill((0, 0, 0))

        current_screen: screen.Screen = self.all_screens[state['_STAGE_DATA']['screen_number']]

        display.blit(terrain_surf, (0, 0))

        current_screen.draw(state)

        letters = []

        for particle in state['PARTICLES']:
            particle.draw(display)
        
        for projectile in state['PROJECTILES']:
            projectile.draw(display)

        for event in events:
            check_quit(event)

            if event.type == MOUSEBUTTONDOWN:
                state['MOUSEDOWN'] = True

            elif event.type == MOUSEMOTION:
                state['MOUSEDOWN'] = False

            elif event.type == KEYDOWN:
                letters.append(event.unicode)
        
        if letters:
            pass

        if '~' in letters:
            print('open terminal...')




def check_quit(event):
    """check if event is a quit event. if it is, quit."""
    if event.type == QUIT:
        pg.quit()
        raise SystemExit



class _NullStage(Stage):

    def __init__(self):
        pass
    position_on_map = None
    all_screens = None
    comes_from = None
    drawing_surface = None
    peaceful = None
    has_icon = None
    links_to = None
    beaten = True

# d = pg.Surface((100, 100))
# d.fill((255, 255, 255))
# s = Stage(
#     "Test Stage 0.0",
#     position_on_map=(18, 569),
#     all_screens=[PeacefulScreen],
#     boss_screen=None,
#     surface=d,
#     terrain=Terrain('dirt', 'flat'),
#     comes_from=None,
#     peaceful=True,
# )
# s.draw_on_map()
# s.check_hover((100, 100))

# pg.image.save(d, r'C:\Users\Michael\Desktop\test_images\howdy.png')
