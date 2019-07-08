"""item.py- this class has the base class for every item."""

import lzma
import enum
import json

try:
    from ._internal import PICS

except ImportError:
    from _internal import PICS


class ItemFlag(enum.Enum):
    """flags for the items."""
    NULL_ITEM = 0
    WEAPON = 1
    COMPO = 2
    MATERIAL = 3
    FOOD = 4
    ARMOUR = 5

    # not sure if I'm going to implement elite items
    ELITE = 5

    NOT_TRADEABLE = 6


def get_flags(data):
    """return the flags of the item just given the data."""
    raw = lzma.decompress(data).decode()
    return [ItemFlag(i) for i in raw.split('}\x00')[-1].encode()]


class Item:
    """base class for all items."""

    def __init__(self, *flags, **kwargs):
        self.attrs = kwargs
        self.flags = flags
        self._licon = kwargs['licon']
        self._sicon = kwargs['sicon']

    def __str__(self):
        return "Item({}, {}) with {}, {}".format(self._sicon, self._licon, self.attrs, self._get_flagstr())

    @property
    def sicon(self):
        """get the smallicon itself."""
        keys = self._sicon.split('/')
        obj = PICS
        for key in keys:
            obj = obj[key]

        return obj

    @property
    def licon(self):
        """get the actual icon surface"""
        keys = self._licon.split('/')
        obj = PICS
        for key in keys:
            obj = obj[key]

        return obj

    def _get_flagstr(self):
        """get a string representing all flags given."""
        string = ""
        for item in self.flags:
            string += ItemFlag(item).name + ", "
        return string

    def dumps(self):
        """get data representing the item"""
        return lzma.compress(json.dumps(
            {**self.attrs, 'licon': self._licon, 'sicon': self._sicon}
        ).encode() + b'\x00' + b''.join([
            flag.value.to_bytes(1, 'little') for flag in self.flags
        ]))

    def dump(self, file):
        """write data to file."""
        file.write(self.dumps())

    @classmethod
    def from_data(cls, data):
        """load an item from binary data."""
        raw = lzma.decompress(data).decode()
        flags = [i for i in raw.split('}\x00')[-1].encode()]
        data = json.loads(raw.split('\x00')[0])
        print(data)
        inst = cls(**data)
        inst.flags = flags
        return inst

    def draw(self, surface, pos, stage):
        """draw the item to surface. if stage is 1, it will
        draw the small icon. if stage is 0, it will draw the large icon.
        """
        surface.blit(self.sicon if stage else self.licon,
                     pos)


class NullItem(Item):
    """this item is just a placeholder, similar to None."""

    def __init__(self):
        super().__init__(ItemFlag.NULL_ITEM, licon=None, sicon=None)


NULL = NullItem()

if __name__ == "__main__":
    d = Item(ItemFlag.WEAPON, ItemFlag.FOOD, thing=1, howdy=5)
    print(d)
    import pprint
    pprint.pprint(PICS)
    with open('data.bin', 'wb') as f:
        d.dump(f)

    f = open('data.bin', 'rb').read()
    t = Item.from_data(f)
    print(t)

    print(get_flags(f))
