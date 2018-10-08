import pygame as pg
from pygame.locals import *
from threading import Thread

FPS = 60
SCREEN_X, SCREEN_Y = 800, 600
RECT_X, RECT_Y = 10, 10
RIGHT_CLICK = 1
GREEN = (0, 200, 0)
RED = (200, 0, 0)


def main():
    pg.init()
    global DISPLAY, CLOCK

    DISPLAY = pg.display.set_mode((SCREEN_X, SCREEN_Y))
    CLOCK = pg.time.Clock()

    screen_image = pg.image.load('..\\data\\dash_skeleton.png').convert()
    DISPLAY.blit(screen_image, (0, 0))

    rect1 = Rect(SCREEN_X // 2, SCREEN_Y // 2, RECT_X, RECT_Y)
    drag = False

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                raise SystemExit

            drag_if_supposed_to(rect1, event, drag)

        pg.display.update()
        DISPLAY.blit(screen_image, (0, 0))
        pg.draw.rect(DISPLAY, GREEN, rect1)
        pg.display.flip()
        CLOCK.tick(FPS)


def drag_if_supposed_to(rect, event, drag=False):
    if event.type == MOUSEBUTTONDOWN:
        if event.button == RIGHT_CLICK and rect.collidepoint(event.pos):
            print('boccoloni')
            drag = True
            mouse_x, mouse_y = event.pos
            off_x = rect.x - mouse_x
            off_y = rect.y - mouse_y

    elif event.type == MOUSEBUTTONUP:
        if event.button == RIGHT_CLICK:
            drag = False

    elif event.type == MOUSEMOTION:
        if drag:
            mouse_x, mouse_y = event.pos
            rect.x = mouse_x + off_x
            rect.y = mouse_y + off_y

    return drag


main()
