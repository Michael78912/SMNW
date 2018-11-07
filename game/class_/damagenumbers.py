"""damagenumbers- an enemy will have a list of damage numbers.
it will display them all over time.
"""
import os
import random

import pygame as pg
GRAY = (220, 220, 220)

class DamageNumber:
	"""display as a number coming from the enemy"""
	lifespan = 60
	dead = False
	font = pg.font.Font(os.path.join('data', 'Roboto-Regular.ttf'), 9)

	def __init__(self, enemy, damage):
		"""initiate instance>"""
		self.surf = self.font.render(str(damage), False, GRAY)
		self.rect = self.surf.get_rect()
		self.rect.center = (enemy.pos[0] + enemy.size_px // 2) + random.randint(-3, 3), enemy.pos[1] - 10

	def update(self, surface):
		"""update and draw to surface"""
		if self.lifespan == 0:
			self.dead = True
		if not self.dead:
			surface.blit(self.surf, self.rect)
			self.rect.y = self.rect.y - 1
			self.lifespan -= 1