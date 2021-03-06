import pygame

try:
    from _internal import *
except ImportError:
    from ._internal import *

DEF_SIZE = 1


class EnemyHead:
    cached_colours = {}
    def __init__(self, type_str, colour, size=DEF_SIZE):
        print(size)
        self.type_str = type_str
        self.colour = colour
        self.size_px = size * 10
        img = PICS['heads'][type_str][colour].copy()
        self.head = pygame.transform.scale(img, (size * 10, size * 10))
        print({100: COLOURS[' '.join(('light', colour))]})
        change_alpha_to_colour(self.head, {100: COLOURS['light ' + colour]})
        self.name = colour + '_' + type_str
        self.pretty_name = ' '.join((colour, type_str)).title()

    def get_image(self, colour_override=None):
        if colour_override is None:
            return self.head

        # return a copy of the overridden image.
        pic = PICS['heads'][self.type_str][colour_override].copy()
        change_alpha_to_colour(pic, {100: COLOURS['light ' + colour_override]})
        pic = pygame.transform.scale(pic, (self.size_px, self.size_px))
        return pic


def main():
    import pygame
    image = pygame.image.load('happy.png')
    pygame.image.save(image, 'purplehappy.png')

if __name__ == '__main__':
    s = EnemyHead('happy', 'green')
    print(vars(s))
    import pygame
    pygame.image.save(s.head, 'C:\\Users\\Michael\\Desktop\\head.png')
    a = pygame.display.set_mode((1000, 1000))
    a.fill(COLOURS['white'])
    s.head.set_alpha(100)
    #change_alpha_to_colour(s.head, {100: (255, 0, 0)})
    a.blit(s.head, (0, 0))
    pygame.display.update()
    while True:
        for i in pygame.event.get():
            if i.type == 12:
                raise SystemExit
