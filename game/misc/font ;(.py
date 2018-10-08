import pygame as pg
pg.init()
a = pg.font.Font('freesansbold.ttf', 32)
s = pg.Surface((100, 100))
s.fill((255, 255, 255))
s.blit(a.render('hello', True, (0, 0, 0)), (0, 0))
pg.image.save(s, 'C:\\Users\\michael\\desktop\\s.png')