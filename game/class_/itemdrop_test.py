# oi we are just going to try and drop an item

import pygame

from weapon import Weapon

WEAPON = Weapon('sword', 'Sword', 'blue', 1, 10, 10)
SURF = pygame.display.set_mode((800, 600))
GROUND_LVL = 390
GRAVITY = 2
AIR = pygame.surface.Surface((800, 800 - GROUND_LVL))
AIR.fill((0, 0, 0))
GROUND = pygame.surface.Surface((800, GROUND_LVL))
GROUND.fill((0, 200, 0))

def main():
    clock = pygame.time.Clock()
    pos = 0
    while True:
        SURF.blit(AIR, (0, 0))
        SURF.blit(GROUND, (0, GROUND_LVL))
        
        if pos <= GROUND_LVL - WEAPON.sicon.get_rect().height:
            pos += GRAVITY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        WEAPON.draw(SURF, (200, round(pos)), 1)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

