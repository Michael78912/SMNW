"""levelparser: converts a JSON level into a Stage object."""

import json

import pygame

import class_

def get_levels(mainsurf):
	"""parse and return all levels in levels.json."""
	levels = json.load(open("levels.json"))
	print(levels.keys(), levels.values())
	stages = []

	for name, items in zip(levels, levels.values()):
		screens = []
		for obj in items['screens']:
			enemies = {}
			for enemy in obj['enemies']:
				enemy_obj = getattr(class_, enemy['type'])(
							enemy['colour'],
							class_.EnemyHead(*enemy['head']),
							enemy['drops'],
							enemy['droprates'],
							class_.Attack(*enemy['attack']),
							enemy['health'],
							enemy['range'],
							enemy['size'],
						)
				enemies[enemy_obj] = enemy['amount']

					
			screens.append(class_.Screen(enemies))

		print(json.dumps(items, indent=4))
		stage = class_.Stage(
			name,
			position_on_map=tuple(items['position']),
			all_screens=screens,
			boss_screen=items['boss_screen'],
			surface=mainsurf,
			terrain=class_.Terrain(
				items['terrain']['texture'], items['terrain']['template']),
			comes_from=items['comes_from'],
		)
		stages.append(stage)

	return stages
# hi
get_levels(pygame.Surface((1, 1)))