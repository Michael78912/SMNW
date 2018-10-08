
import threading
import os

import pygame as pg

try:
    from enemy_head import EnemyHead
    from sprite import SMRSprite
except ImportError:
    from .sprite import SMRSprite
    from .enemy_head import EnemyHead

FPS = 50
CLOCK = pg.time.Clock()


class EnemyImage(SMRSprite):
    def __init__(self, pos, size, colour, head_type, main_game_state,
                 event_queue):
        SMRSprite.__init__(self, main_game_state, event_queue, pos)
        head = EnemyHead(head_type, colour, size)
        head_rect = head.head.get_rect()
        body_size = self.get_body_size()
        head_width = head_rect.width
        head_height = head_rect.height
        body_width = body_size.width
        body_height = body_size.height
        print('!!!!!!!!', colour, head)
        print(locals())

        real_width = body_width if body_width > head_width else head_width
        real_height = body_height if body_height > head_width else head_width
        self.size = (real_width, real_height)
        self.update_coords(pos)
        self.head = head
        self.main_game_state = main_game_state
        self.event_queue = event_queue

    def move_to_x(self, pos, surf, pixels=1):
        current = self.topleft[0]
        dest = current - pixels if pos < current else current + pixels
        self.update_coords((dest, self.topleft[1]))
        self.draw(surf)

    def draw(self, surf):
        """
        since the basic class, just 
        blits the head to the screen.
        """

        surf.blit(self.head.head, self.topleft)

    def start_thread(self, surf, pos):
        self.mainthread = threading.Thread(
            target=self._mainloop,
            args=(surf, pos),
        )
        self.mainthread.start()

    def _mainloop(self, pos, surf):
        at_pos = False
        while True:
            if at_pos:
                continue

            self.move_to_x(pos, surf)

            if self.topleft == pos:
                at_pos = True

            CLOCK.tick(FPS)

    @staticmethod
    def get_body_size():
        return pg.Rect((0, 0), (0, 0))


if __name__ == '__main__':
    d = EnemyImage((0, 0), 2, 'green', 'happy', {}, {})
    s = pg.Surface((10, 10))
    s.fill((255, 255, 255))
    d.draw(s)
    pg.image.save(s, r'C:\Users\Michael\Desktop\s.png')

    s = pg.display.set_mode((500, 500))
    d.start_thread(10, s)

    while True:
        for e in pg.event.get():
            if e.type == 12:
                os._exit(0)
        pg.display.update()
        s.fill((0, 0, 0))
        CLOCK.tick(FPS)
