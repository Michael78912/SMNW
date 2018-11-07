import random
import copy


class Screen:
    firstrun = True
    """Screen is a piece of a stage.
    each stage can have any number of screens, and must have
    a boss screen.
    all_enemies is a dictionary, with keys of enemies, and values of 
    the amount that enemy shoud spawn. ex:

    {
        SomeEnemy('blue', blablabla, 88): 10
    }

    will spawn 10 of SomeEnemy in this screen.
    """

    def __init__(
            self,
            all_enemies,
            spawn_mode='random',
            # must put Y coordinate for each enemy to spawn
    ):

        # assert len(
        #     all_enemies) == len(num_of_enemies_per_enemy
        #                         ), "the enemies and quantities do not match"

        # self.all_enemies = all_enemies
        # self.num_of_enemies_per_enemy = num_of_enemies_per_enemy

        # if spawn_mode == 'random':
        #     new_spawn_mode = []

        #     for enemy, quantity in zip(all_enemies, num_of_enemies_per_enemy):
        #         for i in range(quantity):
        #             new_spawn_mode.append((0 if enemy.area == 'ground' else
        #                                    random.randint(1, 600), random.randint(1, 600)))
        #     self.spawn_mode = new_spawn_mode

        # else:
        #     self.spawn_mode = spawn_mode

        self.total_enemies = sum(all_enemies.values())
        self.enemies = []

        for i in all_enemies:
            self.enemies += [copy.copy(i) for x in range(all_enemies[i])]

        if spawn_mode == 'random':
            self.spawn_mode = [random.randint(1, 800) \
                               for i in range(self.total_enemies)
                              ]

        else:
            self.spawn_mode = spawn_mode

    def draw(self, game_state):
        """draw enemies on screen."""
        terrain = game_state['_STAGE_DATA']['stage'].terrain

        if self.firstrun:
            game_state['_STAGE_DATA']['enemies'] = []
            for enemy, x in zip(self.enemies, self.spawn_mode):
                print(terrain.blocks_to_px(enemy.size), enemy)
                ground_level = terrain.get_spawn_point(x, terrain.blocks_to_px(enemy.size))
                enemy.draw((x, ground_level), game_state['MAIN_DISPLAY_SURF'])
                game_state['_STAGE_DATA']['enemies'].append(enemy)

            for player in game_state['PLAYERS']:
                player.spawn_on_screen(game_state)

            self.firstrun = False
            print('done spawning.')

        else:
            for enemy in self.enemies:
                enemy.move(game_state["PLAYERS"], game_state["MAIN_DISPLAY_SURF"])
                enemy.update(game_state)
                print([e.id for e in game_state['_STAGE_DATA']['enemies']])
            for player in game_state['PLAYERS']:
                player.update(game_state)



class PeacefulScreen(Screen):

    def __init__(self):
        super().__init__((), (), None)
