import random

from .character_image import CharacterImage
from .smr_error import SMRError


class FakeWeapon:

    def __init__(self, colour):
        self.colour = colour


class Class:
    """
    base class for stickman ranger classes.
    """

    attack_radius = 0
    chance_of_motion = 4
    _chance_of_update = 5

    def __init__(
            self,
            type,
            PlayerNum,
            main_game_state,
            stats=(50, 0, 0, 0, 0),
            spec=None,
    ):

        # the following two lines of code may seem redundant, but for a reason.
        try:
            self.health, self.str_, self.dex, self.mag, self.spd = stats
        except ValueError:
            raise SMRError('invalid length of tuple "stat" argument')
        self.stats = stats
        self.image = CharacterImage(
            type, FakeWeapon('green'), (0, 0), main_game_state)
        self.type_ = type
        self.spec = spec

    def hit(self, damage):
        'takes damage by specified amount'
        self.health -= damage

    def heal(self, damage):
        'heals by specified amount'
        self.health += damage

    @staticmethod  # self argument not needed
    def attack(damage, enemy):
        'lowers the enemy`s health by damage'
        enemy.health -= damage

    def level_up(self, *args):
        'raises characters stats by specified amount'
        assert len(args) > 6, 'Too many stats to raise'
        if self.spec is None:
            if not None in args:
                self.spec = args[-1]
            else:
                raise TypeError(
                    'Cannot assign a special value to class, cannot support special value.'
                )
        # add stats
        for index in enumerate(args):
            self.stats[index] += args[index]

    def spawn_on_screen(self, game_state):
        """adds the character to the screen, the very beginning,
        on the top, but not above or underground.
        """
        # surface.blit(self.image, surface.terrain.array[0])

        terrain = game_state['_STAGE_DATA']['stage'].terrain
        display = game_state['MAIN_DISPLAY_SURF']

        x = 15    # we always want to spawn characters at x=15.

        y = round(terrain.get_spawn_point(terrain.get_last_unsolid(
            round(terrain.px_to_blocks(x))), self.image.sizey / 10))
        print(x, y, "howdy fellers")
        self.image.update_coords((x, y))
        print(self.image.type_)
        self.image.build_image(display)


    def update(self, game_state):
        """attempt to move, and attack."""
        screen = game_state['_STAGE_DATA']['screen']
        terrain = game_state['_STAGE_DATA']['stage'].terrain
        enemies = game_state['_STAGE_DATA']['enemies']

        if random.randint(0, self.chance_of_motion) == 1:
            self.image.move_to_x(self.image.topright[0] + 1,
                                 game_state['MAIN_DISPLAY_SURF'])

        # game_state['MAIN_DISPLAY_SURF'].blit(self.picture, self.image.topright)

        update = random.randint(0, self._chance_of_update) == 1

        if not self.image.has_drawn:
            #  needs to draw at least once. override.
            update = True

        self.image.build_image(game_state['MAIN_DISPLAY_SURF'], update)


