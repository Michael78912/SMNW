"""
paritcles that exist for a certain amount of time, and follow a certain path.
"""

class Particle:
    def __init__(self, colour, path_factory, lifespan):
        """
        create and return a new particle object.
        """
        self.colour = colour
        self.path_factory = path_factory
        self.lifespan = lifespan
        self.pos = next(path_factory)
    
    def draw(self, surf):
        """draw the particle to surface."""
        if self.lifespan == 0:
            return
        surf.set_at(self.pos, self.colour)
        self.pos = next(self.path_factory)
        self.lifespan -= 1
    
    def __repr__(self):
        """return a nicely formatted string"""
        return "Particle at {}".format(self.pos)
    
    @staticmethod
    def default_path(pos):
        """a default path. simply drops a pixel every frame."""
        x, y = pos
        while True:
            yield (x, int(y))
            y -= .5
    
