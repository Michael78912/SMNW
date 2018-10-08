class Screen:
    """Screen is a piece of a stage.
    each stage can have any number of screens, and must have
    a boss screen.
    Note: num_of_enemies_per_enemy must be same length as all_enemies.
    if you put (enemy1, enemy2, enemy3) for all enemies,
    and (3, 23, 12) for num_of_enemies_per_enemy, there would be
    3 of enemy one, 23 of enemy2, and 12 of enemy3. [a crazy stage :)]
    spawn_mode: 'random' makes a random position for each enemy, and if
    you don't want random, you must put a Y coordinate for each enemy.
    (that is, a tuple with subtuples for every enemy)
    """

    def __init__(
            self,
            all_enemies,
            num_of_enemies_per_enemy,
            spawn_mode='random',
            # must put Y coordinate for each enemy to spawn
    ):

        assert len(
            all_enemies) == len(num_of_enemies_per_enemy
                                ), "the enemies and quantities do not match"

        self.all_enemies = all_enemies
        self.num_of_enemies_per_enemy = num_of_enemies_per_enemy

        if spawn_mode == 'random':
            new_spawn_mode = []

            for enemy, quantity in zip(all_enemies, num_of_enemies_per_enemy):
                for i in range(quantity):
                    new_spawn_mode.append((0 if enemy.area == 'ground' else
                                           random.randint(1, 600), random.randint(1, 600)))
            self.spawn_mode = new_spawn_mode

        else:
            self.spawn_mode = spawn_mode

    def start(self):
        raise NotImplementedError


class PeacefulScreen(Screen):
    def __init__(self):
        super().__init__((), (), None)
