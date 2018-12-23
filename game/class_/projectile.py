"""class for representing a projectiile.
It is up to the class using the projectile to
stop it.
"""

class Projectile:
    """represents a projectile"""

    path = None
    pos = (-1, -1)

    def __init__(self, image, path_factory, lifespan=-1):
        """if lifespan is -1, it can last forever."""
        self.image = image
        self.path_factory = path_factory
        # self.pos = next(path_factory)
    
    def start(self, pt1, pt2):
        """start the projectile"""
        self.path = self.path_factory(pt1, pt2)
        self.pos = next(self.path)
    
    def draw(self, surf):
        """draw the projectile to surf"""
        surf.blit(self.image() if callable(self.image) else self.image, self.pos)
        self.pos = next(self.path)
    