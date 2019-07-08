"""entities are pretty nifty things.
(Ok i did take this idea pretty much directly from minecraft)
almost anything that does anything inside the game screen is an entity,
except for characters and enemies (they probably would be but I made them before
this and I don't really feel like changing everything at the moment).
"""

import pygame


class Entity:
    """base class for all things in the game (bullets, residues, items, etc...)
    If I feel like introducing siege weapons they will be entities too
    """
    live = False
    hitbox = pygame.Rect((0, 0), (0, 0))

    def add_to_queue(self, game_state):
        """add this entity to the game's entity queue to be updated
        every frame.
        """
        game_state['ENTITIES'].append(self)

    def update(self, game_state):
        """to be overridden, but STILL CALL THIS EVERY TIME. it is important"""
        if not self.live:
            # if the entity is now dead, remove it.
            game_state['ENTITIES'].remove(self)

        for character in game_state['PLAYERS']:
            if character.rect.colliderect(self.hitbox):
                self._charcollide(character)

        for enemy in game_state['_STAGE_DATA']['ENEMIES']:
            if enemy.hitbox.colliderect(self.hitbox):
                self._enemycollide(enemy)

    def _charcollide(self, _):
        """at this point just kill the entity. override it if you
        want to do something else. same goes with enemy.
        """
        self.live = False

    def _enemycollide(self, _):
        self.live = False
