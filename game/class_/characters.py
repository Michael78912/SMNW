"""characters.py- a module of subclasses
each of these classes is a class of stickman from 
stickmanranger.
"""
try:
    from _internal import *
    from klass import Class

except ImportError:
    from ._internal import *
    from .klass import Class

__all__ = ['Swordsman', 'Angel', 'Archer', 'Spearman', 'Wizard']

DEFAULT_STATS = (50, 0, 0, 0, 0)


class Swordsman(Class):
    image = PICS['characters']['swordsman']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'swordsman', player_num, weapon, main_game_state, stats)


class Angel(Class):
    image = PICS['characters']['angel']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'angel', player_num, weapon, main_game_state, stats)


class Archer(Class):
    image = PICS['characters']['archer']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'archer', player_num, weapon, main_game_state, stats)


class Spearman(Class):
    image = PICS['characters']['spearman']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'spearman', player_num, weapon, main_game_state, stats)


class Wizard(Class):
    image = PICS['characters']['wizard']

    def __init__(self, player_num, main_game_state, weapon, stats=DEFAULT_STATS):
        Class.__init__(self, 'wizard', player_num, weapon, main_game_state, stats)
