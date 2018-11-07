import random

from .character_image import CharacterImage
from .smr_error import SMRError


BEIGE = (232, 202, 145)

class FakeWeapon:

    def __init__(self, colour):
        self.colour = colour


class Class:
    """
    base class for stickman ranger classes.
    """

    attack_radius = 0
    chance_of_motion = 4
    max_motion = 3
    _chance_of_update = 2

    def __init__(
            self,
            type,
            PlayerNum,
            weapon,
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
        self.weapon = weapon
        self.image = CharacterImage(
            type, weapon, (0, 0), main_game_state)
        self.type_ = type
        self.spec = spec

    def hit(self, damage):
        'takes damage by specified amount'
        self.health -= damage

    def heal(self, damage):
        'heals by specified amount'
        self.health += damage

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

        y = terrain.get_spawn_point(x, self.image.sizey)
        self.image.update_coords((x, y))
        self.image.build_image(display, BEIGE)

    def update(self, game_state):
        """attempt to move, and attack."""
        screen = game_state['_STAGE_DATA']['screen']
        terrain = game_state['_STAGE_DATA']['stage'].terrain
        enemies = game_state['_STAGE_DATA']['enemies']
        self.weapon.update()



        motion_target = get_closest_enemy(game_state, self.image.topright[0])
        target_x = motion_target.pos[0]

        x = self.image.topright[0]

        distance = target_x - x if target_x >= x else x - target_x

        if distance <= self.weapon.range:
            # self.weapon.attack_enemy(motion_target)
            self.attack(motion_target)

        if random.randint(0, self.chance_of_motion) == 1 \
            and ((self.image.topright[0] - target_x)
                 if self.image.topright[0] > target_x else
                 (target_x - self.image.topright[0])) and \
            distance >= self.weapon.range:

            self.image.move_to_x(self.image.topright[0] + self.max_motion,
                                 game_state['MAIN_DISPLAY_SURF'],
                                 pixels=random.randint(1, self.max_motion))

        if game_state['MOUSEDOWN']:
            if self.image.rect.collidepoint(game_state['MOUSE_POS']):
                self.image.update_coords(game_state['MOUSE_POS'])


        # game_state['MAIN_DISPLAY_SURF'].blit(self.picture, self.image.topright)

        update = random.randint(0, self._chance_of_update) == 1
        if distance <= self.weapon.range:
            update = False

        if not self.image.has_drawn:
            #  needs to draw at least once. override.
            update = True


        self.image.build_image(game_state['MAIN_DISPLAY_SURF'], BEIGE, rebuild=update)

    def attack(self, target):
        """attack the target enemy."""
        if self.weapon.can_attack():
            self.weapon.attack_enemy(target)


def get_closest_enemy(game_state, pos):
    """get and return the closest enemy to pos."""
    possible_destinations = [enemy.pos[0]
                             for enemy in game_state['_STAGE_DATA']['enemies']]
    print(possible_destinations)

    distances = [pos - i if i <= pos else i -
                 pos for i in possible_destinations]

    distance = min(distances)

    return game_state['_STAGE_DATA']['enemies'][distances.index(distance)]
