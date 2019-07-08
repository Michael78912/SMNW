"""this is sort of a container class for an item. you put an :"Item" inside a
a "Drop". this way, the drop can control the way the item drops from the enemy.
"""

import random

from .entity import Entity

# 180 px/s is probably a good speed
GRAVITY = 2


class Drop(Entity):
    """drop an item."""
    pos = (0, 0)   # for now
    live = False   # not a live entity to begin with
    surf = None
    floor_level = 0

    def __init__(self, item, chance):
        self.item = item
        self.icon = item.sicon
        self.chance = chance

    def get_drop(self):
        """return true if we want to actually drop the item."""
        # WORKS PERFECTLY FINE NOT TOO SIMPLE DONT CHANGE
        return random.random() <= self.chance

    def drop(self, surface, floor_level, pos, game_state):
        """drop the item on the floor. make the user of this function
        give the floor level because I'm too lazy to calculate it here (it
        will be faster too and efficiency is key)
        """
        self.add_to_queue(game_state)
        self.item.draw(surface, pos)
        self.pos = pos
        self.floor_level = floor_level - self.item.sicon.get_rect().height
        self.surf = surface
        self.live = True

    def update(self, game_state):
        """override Entity's update, fall a bit if necessary."""
        if self.pos[1] <= self.floor_level:
            self.pos = self.pos[0], self.pos.y + GRAVITY

        self.item.draw(self.surf, self.pos)
        # still need super for collision detection and checking to remove from the entity queue
        super().update(game_state)

    def _charcollide(self, char):
        # if it collides with thecharacter, the character "picks it up." this means
        # the entity will die, and the character will gain the item self is holding.
        self.live = False
        char.inventory.add(self.item)

    def _enemycollide(self, _):
        # do nothing at the moment, the enemy can't pick up the item
        pass


def test(vartouse=True):
    d = Drop(None, 0.90)
    percents = [d.get_drop() for _ in range(100)]
    falses = percents.count(False)
    trues = percents.count(True)
    return trues if vartouse else falses


if __name__ == "__main__":
    # testing 100,000 times is probably a little excessive, but at least it's 90 every time
    percentages = sum([test() for _ in range(1000)])
    print(percentages // 1000)
