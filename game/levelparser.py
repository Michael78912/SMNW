"""levelparser: converts a JSON level into a Stage object."""

import json
import os

import class_


def get_levels(mainsurf):
    """parse and return all levels in levels.json."""
    levels = json.load(open("levels.json"))
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
                    class_.MeleeAttack(*enemy['attack']),
                    enemy['health'],
                    enemy['range'],
                    enemy['size'],
                )
                enemies[enemy_obj] = enemy['amount']

            screens.append(class_.Screen(enemies))

            terrain = class_.new_terrain.Terrain()
            file = os.path.join(
                'terrains', items['terrain']['template']) + '.smr-terrain'
            terrain.load(open(file), items['terrain']['texture'])
        stage = class_.Stage(
            name,
            position_on_map=tuple(items['position']),
            all_screens=screens,
            boss_screen=items['boss_screen'],
            surface=mainsurf,
            terrain=terrain,
            comes_from=items['comes_from'],
        )
        stages.append(stage)

    return stages
# hi
print(get_levels(__import__('pygame').Surface((10, 10))))
