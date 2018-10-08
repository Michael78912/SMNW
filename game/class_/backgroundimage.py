try:
    from _internal import PICS
except ImportError:
    from ._internal import PICS


class BackGroundImage:
    """
    this has no effect on the stage itself, 
    but is just for decoration.
    """

    def __init__(self, name, topright, priority=1, put_on_terrain=None):
        self.toprgight = topright
        self.image = PICS['backgrounds'][name]
        self.priority = priority
        try:
            self.__class__.instances.append(self)
        except AttributeError:
            # this is the first instance
            self.__class__.instances = [self]

    def __del__(self):
        # must remove the current instance from instances
        self.__class__.instances.pop(self.__class__.instances.index(self))

    def draw(self, surf):
        """
        draw the image to surf
        """
        surf.blit(self.image, self.topright)

    @classmethod
    def draw_all(cls, surf):
        """
        draw all of the current instances to surf
        """
        orderedpairs = sorted(
            [(ins.priority, ins) for ins in cls.instances], key=lambda x: x[0])

        for pair in orderedpairs:
            pair[1].draw(surf)


if __name__ == '__main__':
    print(BackGroundImage('hut', (0, 0)).instances)
