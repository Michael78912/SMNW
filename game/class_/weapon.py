"""file that contians the weapon class"""
import pygame

try:
    from _internal import PICS, change_alpha_to_colour, COLOURS
    from item import Item, ItemFlag
    from attack import Attack

except ImportError:
    from ._internal import PICS, change_alpha_to_colour, COLOURS
    from .item import Item, ItemFlag
    from .attack import Attack

__all__ = ['Weapon']


def create_weapon(**kwargs):
    """create a weapon from args and kwargs."""
    return Weapon(**kwargs)


class Weapon(Item):
    """Base class for all SMNW weapons. derived from Item."""
    cooldown = 0

    def __init__(self, klass, name, colour, level, attack, range_, alphatocolour=None, **_):
        # largeicon = PICS['weapons']['large_icon'][klass][repr(level)][
        #     colour]
        # smallicon = PICS['weapons']['small_icon'][klass][repr(level)][
        #     colour]

        if isinstance(attack, dict):
            # we got an instance from loading a json file. convert the 
            # attack here.
            attack = Attack(**attack)

        self.klass = klass
        self.name = name
        self.colour = colour
        self.level = level
        self.attack = attack
        self.range_ = range_

        licon = '/'.join(('weapons', 'large_icon', klass, str(level), colour))
        sicon = '/'.join(('weapons', 'small_icon', klass, str(level), colour))

        largeicon = '/'.join((klass, str(level)))
        smallicon = largeicon
        if alphatocolour is not None:
            change_alpha_to_colour(largeicon, alphatocolour)
            change_alpha_to_colour(smallicon, alphatocolour)

        self.largeicon_surf = PICS['weapons']['large_icon'][klass][str(
            level)][colour]

        rect = self.largeicon_surf.get_rect()
        pos = rect.bottomright[0] - 4, rect.bottomright[1] - 9
        font = pygame.font.Font('freesansbold.ttf', 8)
        surf = font.render(repr(level), True, COLOURS['black'])
        self.largeicon_surf.blit(surf, pos)

        self.smallicon_surf = PICS['weapons']['small_icon'][klass][str(
            level)][colour]

        super().__init__(
            ItemFlag.WEAPON,
            name=name,
            klass=klass,
            colour=colour,
            level=level,
            attack=attack,
            range_=range_,
            alphatocolour=alphatocolour,
            licon=licon,
            sicon=sicon,
        )

    def can_attack(self):
        """return true if the weapon is able to attack."""
        return self.cooldown == 0

    def __str__(self):
        return '"{}": lvl {}'.format(self.name, self.level)

    def __repr__(self):
        return str(self)

    def update(self):
        """see if it is OK to use again."""
        if self.cooldown != 0:
            self.cooldown -= 1

    def attack_enemy(self, origin, target, game_state):
        """attack the target."""
        self.cooldown = self.attack.cooldown
        self.attack.attack(origin, target, game_state)
