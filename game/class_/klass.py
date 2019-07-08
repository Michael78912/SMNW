"""klass.py (I know it's spelt wrong, OK)?
base class for all character classes in SMNW. handles
image generation, spawning, and default movement, and attacking.
"""
import random

from . import new_terrain
from .block import Block
from .character_image import CharacterImage
from .smr_error import SMRError

BEIGE = (232, 202, 145)


class Class:
    """
    base class for stickman ranger classes.
    """

    # I, personally think that a character class in a reasonably large
    # game should be allowed to have at least a few more attributes than
    # seven. I am so, so, sorry if you hate me, pylint.
    # and too many arguments to __init__? whats that about?

    # pylint: disable=too-many-instance-attributes, too-many-arguments

    attack_radius = 0
    chance_of_motion = 4
    max_motion = 3
    jump_height = 10
    _chance_of_update = 2

    def __init__(
            self,
            type_,
            player_num,
            weapon,
            main_game_state,
            inventory,
            stats=(50, 0, 0, 0, 0),
            spec=None,
    ):

        # the following two lines of code may seem redundant, but for a reason.
        try:
            self.health, self.str_, self.dex, self.mag, self.spd = stats
        except ValueError:
            raise SMRError('invalid length of tuple "stat" argument')
        self.stats = stats
        self.player_num = player_num
        self.weapon = weapon
        self.image = CharacterImage(
            type_, weapon, (0, 0), main_game_state)
        self.type_ = type_
        self.spec = spec
        self.inventory = inventory

    def __repr__(self):
        return """character number {} type {}""".format(self.player_num, self.type_)

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

        display = game_state['MAIN_DISPLAY_SURF']

        x = 15    # we always want to spawn characters at x=15.

        y = game_state['_STAGE_DATA']['stage'].terrain.get_spawn_point(x)
        self.image.update_coords((x, y - 10))
        self.image.build_image(display, BEIGE)

    def update(self, game_state):
        # tell our weapon that another frame has passed, so it may now be able to attack
        self.weapon.update()
        # the terrain object currently in use.
        terrain: new_terrain.Terrain = game_state['_STAGE_DATA']['stage'].terrain

        # position of the feet. (can be a little off, you can sink into
        # the ground a bit)
        footpos = self.image.topleft[0], self.image.topleft[1] + 10

        # indexes of blocks on both axes.
        current_block_x, current_block_y = terrain.px_pos_to_blocks(
            footpos
        )

        # block we are currently standing on.
        block: Block = terrain[current_block_x, current_block_y]

        # check to see if we're underground (it happens)
        if block.solid == 0:
            self.image.update_coords((self.image.topleft[0], self.image.topleft[1] - 2))

        # enemy we are moving toward, and will also attempt to attack later on
        try:
            enemy = get_closest_enemy(game_state, self.image.topleft[0])
        except ValueError:
            # no more enemies remaining.
            enemy = None

        # we may need to fall a little bit
        self.image.update_coords(
            (self.image.topleft[0], self.image.topleft[1] + block.solid))

        # characters are more smart than blobs, so they always know the right way to go.
        distance = self.image.topleft[0] - enemy.pos[0]
        # choose the offset. negative to move to the left, positive to the right
        offset = -2 if distance > 0 else 2

        # select the proposed position. now we need to see if we can move there.
        proposed_pos = self.image.topright[0] + offset, self.image.topright[1]

        # this is the column we will be moving towards, need to check it.
        column = terrain.grid[:, terrain.px_to_blocks(
            proposed_pos[0]
        )]

        # get the top levels in the next column
        top_levels = {i for i,
                      obj in enumerate(column) if obj.top}

        # the X-position of the enemy we are going towards
        target_x = enemy.pos[0]

        # boolean to see if we can move or not
        can_move = True

        if top_levels:
            # get how far they would have to move.

            distance = terrain.blocks_to_px(
                min([current_block_y - i for i in top_levels]))

            if 0 < distance <= self.jump_height:
                # we need to jump, since there we can go that high.
                self.image.update_coords((self.image.x, self.image.y - self.jump_height))

            elif distance > self.jump_height:
                # can not jump, and can not move. stay still.
                can_move = False

        x = self.image.topleft[0]
        distance = target_x - x if target_x >= x else x - target_x

        # if we are going to attack, don't move.
        can_move = can_move and distance >= self.weapon.attrs['range_']
        if distance <= self.weapon.attrs['range_']:
            # self.weapon.attack_enemy(motion_target)
            self.attack(enemy, game_state)
        if can_move:
            print(self, "moving...")

            self.image.move_to_x(self.image.topright[0] + self.max_motion,
                                 game_state['MAIN_DISPLAY_SURF'],
                                 pixels=random.randint(1, self.max_motion))

        update = random.randint(0, self._chance_of_update) == 1
        if distance <= self.weapon.attrs['range_']:
            update = False

        if not self.image.has_drawn:
            #  needs to draw at least once. override.
            update = True

        self.image.build_image(
            game_state['MAIN_DISPLAY_SURF'], BEIGE, rebuild=update)

    # def update(self, game_state):
    #     """attempt to move, and attack."""
    #     terrain_obj = game_state['_STAGE_DATA']['stage'].terrain
    #     self.weapon.update()

    #     current_block_x, current_block_y = terrain_obj.px_pos_to_blocks(
    #         self.image.bottomleft
    #     )

    #     next_column = list(
    #         terrain_obj.grid[:, current_block_x + 1])
    #     top_levels = {i if obj.top else None for i,
    #                   obj in enumerate(next_column)}
    #     top_levels.remove(None)

    #     can_move = True

    #     if top_levels:
    #         # get how far they would have to move.

    #         distance = terrain_obj.blocks_to_px(
    #             min([current_block_y - i for i in top_levels]) + 1)

    #         if 0 < distance <= self.jump_height:
    #             # 10 pixels is the maximum a player can climb, without any sort of tool.
    #             self.image.update_coords((self.image.x, self.image.y - 12))

    #         elif distance > self.jump_height:
    #             # can not jump, and can not move. stay still.
    #             can_move = False

    #     in_air = terrain_obj[terrain_obj.px_pos_to_blocks(
    #         self.image.topleft
    #     )].solid != 0
    #     if in_air:
    #         self.image.update_coords(
    #             (self.image.topleft[0], self.image.topleft[1] + 1))

    #     try:
    #         motion_target = get_closest_enemy(
    #             game_state, self.image.topright[0])
    #     except ValueError:
    #         # no more enemies remaining, `min` will raise a ValueError.
    #         return
    #     target_x = motion_target.pos[0]

    #     x = self.image.topright[0]

    #     distance = target_x - x if target_x >= x else x - target_x

    #
    #     print(((self.image.topright[0] - target_x) if self.image.topright[0] > target_x else (target_x - self.image.topright[0])))

    #     can_move = random.randint(0, self.chance_of_motion) == 1 and can_move
    #     # can_move = can_move and ((self.image.topright[0] - target_x) if self.image.topright[0] > target_x else (target_x - self.image.topright[0]))
    #     can_move = can_move and distance >= self.weapon.attrs['range']

    #     if can_move:
    #         print(self, "moving...")

    #         self.image.move_to_x(self.image.topright[0] + self.max_motion,
    #                              game_state['MAIN_DISPLAY_SURF'],
    #                              pixels=random.randint(1, self.max_motion))

    #     if game_state['MOUSEDOWN']:
    #         if self.image.rect.collidepoint(game_state['MOUSE_POS']):
    #             self.image.update_coords(game_state['MOUSE_POS'])

    #     # game_state['MAIN_DISPLAY_SURF'].blit(self.picture, self.image.topright)

    #     update = random.randint(0, self._chance_of_update) == 1
    #     if distance <= self.weapon.attrs['range']:
    #         update = False

    #     if not self.image.has_drawn:
    #         #  needs to draw at least once. override.
    #         update = True

    #     self.image.build_image(
    #         game_state['MAIN_DISPLAY_SURF'], BEIGE, rebuild=update)

    def attack(self, target, game_state):
        """attack the target enemy."""
        if self.weapon.can_attack():
            self.weapon.attack_enemy(self.image.topright, target, game_state)


def get_closest_enemy(game_state, pos):
    """get and return the closest enemy to pos."""
    possible_destinations = [enemy.pos[0]
                             for enemy in game_state['_STAGE_DATA']['enemies']]
    print(possible_destinations)

    distances = [pos - i if i <= pos else i -
                 pos for i in possible_destinations]

    distance = min(distances)

    return game_state['_STAGE_DATA']['enemies'][distances.index(distance)]
