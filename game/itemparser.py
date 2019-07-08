"""this file is similar to levelparser.py, as in it parses a json file and
makes it into something recognizable by the game. 
"""

import json
import pprint

import class_

def _get_subroot(item_list, list_name, exceptions):
    # here we can return the sub-root area of lists. for example the list of all
    # the weapons available in the game.

    # we need to copy the exceptions
    for key, val in exceptions.keys(), exceptions.values():
        item_list[val] = item_list[key]

    # new list of items
    smnw_items = []

    # this is the class we need to use to generate the items,
    # it is the same as the list's name in the data structure.
    item_type = getattr(class_, list_name)

    # create the new items, with the data given from the json ones.
    for item in item_list:
        smnw_items.append(
            item_type(
                # if there is a sub-dictionary (eg. attack for weapon)
                # the constructor MUST be able to handle it.
                **item
            )
        )
    print(smnw_items)


def get_items():
    """get and return the game's items."""
    root_json = json.load(open('drops.json'))
    root_py = {}

    # we need to completely convert root_json to the python version

    # get all the semi-root objects into the dictionry
    for subkey in root_json:
        # turn the array of json objects into a list of actual SMNW Item objects
        root_py[subkey] = _get_subroot(root_json[subkey], subkey)

if __name__ == "__main__":
    get_items()