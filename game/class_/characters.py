"""characters.py- a module of subclasses
each of these classes is a class of stickman from 
stickmanranger.
"""
try:
    from _internal import *
    from character import Character

except ImportError:
    from ._internal import *
    from .character import Character

__all__ = ['Swordsman', 'Angel', 'Archer', 'Spearman', 'Wizard']

DEFAULT_STATS = (50, 0, 0, 0, 0)


class Swordsman(Character):
    image = PICS['characters']['swordsman']

    def __init__(self, player_num, stats=DEFAULT_STATS):
        Character.__init__(self, 'swordsman', stats)


class Angel(Character):
    image = PICS['characters']['angel']

    def __init__(self, player_num, stats=DEFAULT_STATS):
        Character.__init__(self, 'angel', stats)


class Archer(Character):
    image = PICS['characters']['archer']

    def __init__(self, player_num, stats=DEFAULT_STATS):
        Character.__init__(self, player_num, stats)


class Spearman(Character):
    image = PICS['characters']['spearman']

    def __init__(self, player_num, stats=DEFAULT_STATS):
        Character.__init__(self, player_num, stats)


class Wizard(Character):
    image = PICS['characters']['wizard']

    def __init__(self, player_num, stats=DEFAULT_STATS):
        Character.__init__(self, player_num, stats)
