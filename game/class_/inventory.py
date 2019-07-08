"""this module is responsible for all doings with the inventory.
all enemies and players may have an inventory, as well as the "Main"
inventory. the "Main" inventory is a way of getting some things you
may want to grab quickly.
"""

try:
    from .item import Item, ItemFlag, get_flags, NULL
    from .weapon import Weapon
except ImportError:
    from item import Item, ItemFlag, get_flags, NULL
    from weapon import Weapon

FLAG_MAPPING = {
    ItemFlag.WEAPON: Weapon,
    ItemFlag.FOOD: Item,
    ItemFlag.COMPO: Item,
    ItemFlag.MATERIAL: Item,
    ItemFlag.NULL_ITEM: NULL,
}

FORMAT_VER = 0
HEAD_LENGTH = 8
FORMAT_LEN = 3
LENGTH_LEN = 2


def get_item(data_chunk):
    """get a proper item, even with the proper class, from a chunk of data."""
    types = [FLAG_MAPPING.get(flag) for flag in get_flags(
        data_chunk) if flag]
    while True:
        try:
            types.remove(None)
        except ValueError:
            break
    assert len(types) == 1, "Error: More than one type given ({})".format(types)
    if types[0] is NULL:
        return NULL
    return types[0].from_data(data_chunk)


def _null_pad(lst, amount):
    """pad the list to length <amount> with None."""
    assert len(lst) <= amount, "you can not pad a list to less than its length"
    while len(lst) != amount:
        lst.append(NULL)


class Inventory:
    """class for holding items. that's all this will do."""

    def __init__(self, limit, items=None):
        if items is None:
            self.items = [NULL for _ in range(limit)]
        else:
            self.items = items
            _null_pad(items, limit)

        self.limit = limit

        if len(self.items) > limit:
            raise ValueError('The given items exceeds the limit.')

    def __getitem__(self, i):
        # get the item at index i
        return self.items[i]

    def __setitem__(self, i, val):
        # set the item at i to val.
        self.items[i] = val

    def dumps(self):
        """return all items as binary data."""
        header = b"INV" + FORMAT_VER.to_bytes(FORMAT_LEN, 'big') \
            + self.limit.to_bytes(LENGTH_LEN, 'big')
        items = [item.dumps() for item in self.items]
        data = b"\xff\xff\xff\xff".join(items)
        return header + data

    def dump(self, file):
        """write the contents to a file."""
        file.write(self.dumps())

    def _find_empty_slot(self):
        for i, item in enumerate(self.items):
            if item is NULL:
                return i

        # no empty slot, raise an error for now
        raise ValueError("No empty slots available")

    def add(self, item):
        """add an item to the closest empty slot."""
        slot = self._find_empty_slot()
        self[slot] = item

    @classmethod
    def from_data(cls, data):
        """read the data, and make a new Inventory object from it."""
        print(data)
        head = data[:HEAD_LENGTH]
        version = int.from_bytes(head[3:3 + FORMAT_LEN], 'big')
        length = int.from_bytes(head[3 + FORMAT_LEN:HEAD_LENGTH], 'big')
        item_data = data[HEAD_LENGTH:]
        items = [get_item(chunk)
                 for chunk in item_data.split(b"\xff\xff\xff\xff")]
        return cls(length, items)

    @classmethod
    def from_file(cls, file):
        """read the file and return a Inventory object from it."""
        return cls.from_data(file.read())

    def __str__(self):
        return str(self.items)


def _main():
    from weapon import Weapon
    i = Inventory(10, [
        Item(ItemFlag.FOOD, health=12, licon="Nothing", sicon="Nothing"),
        Item(ItemFlag.COMPO, ItemFlag.ELITE, licon="Newton", sicon="Fig"),
        Weapon('sword', 'Sword', 'blue', 1, 10, 10),
    ])
    with open('inventory.smr-inv', 'wb') as file:
        i.dump(file)
    with open('inventory.smr-inv', 'rb') as file:
        i = Inventory.from_file(file)

    print(i)


# print(get_item(open('data.bin', 'rb').read()))
if __name__ == "__main__":
    _main()
