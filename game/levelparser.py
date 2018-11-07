"""levelparser: converts a JSON level into a Stage object."""

import json

def get_levels():
	"""parse and return all levels in levels.json."""
	levels = json.load(open("levels.json"))
	print(levels)

get_levels()