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

        self.total_enemies = sum(all_enemies.values())
        self.enemies = []

        for i in all_enemies:
            self.enemies += [copy.copy(i) for x in range(all_enemies[i])]

        if spawn_mode == 'random':
            self.spawn_mode = [random.randint(1, 775) \
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
                ground_level = terrain.get_spawn_point(x) - enemy.size_px
                enemy.draw((x , ground_level), game_state['MAIN_DISPLAY_SURF'])
                game_state['_STAGE_DATA']['enemies'].append(enemy)

            for player in game_state['PLAYERS']:
                player.spawn_on_screen(game_state)

            self.firstrun = False

        else:
            for enemy in self.enemies:
                enemy.move(game_state["PLAYERS"], game_state["MAIN_DISPLAY_SURF"], game_state['_STAGE_DATA']['stage'].terrain)
                enemy.update(game_state)
            for player in game_state['PLAYERS']:
                player.update(game_state)



class PeacefulScreen(Screen):

    def __init__(self):
        super().__init__((), (), None)
