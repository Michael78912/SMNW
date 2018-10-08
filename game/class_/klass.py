class Class:
    """
    base class for stickman ranger classes.
    """

    def __init__(
            self,
            type,
            PlayerNum,
            stats=(50, 0, 0, 0, 0),
            spec=None,
    ):

        # the following two lines of code may seem redundant, but for a reason.
        try:
            self.health, self.str_, self.dex, self.mag, self.spd = stats
        except ValueError:
            raise SMRError('invalid length of tuple "stat" argument')
        self.stats = stats

        self.type_ = type_
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
        for index in range(len(args)):
            self.stats[index] += args[index]

    def spawn_on_screen(self, surface, screen):
        """adds the character to the screen, the very beginning,
        on the top, but not above or underground.
        """
        surface.blit(self.image, surface.terrain.array[0])
