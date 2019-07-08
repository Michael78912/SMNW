from pprint import pprint
import warnings

import pygame as pg

try:
    from _internal import COLOURS
except ImportError:
    from ._internal import COLOURS


LARGEICONSIZE = 10

warnings.warn("This Inventory module is DEPRECATED. please use the better one", DeprecationWarning)

class InventoryHandler:
    def __init__(self, sizex, sizey):
        self.datas = [[None for i in range(sizey)] for i in range(sizex)]
        #print(self.datas)

        #print(self.datas)

    def sort_dict(self, dictionary):
        """
        sorts dictionary shaped like: {'1x2': whatever} and puts it into 
        the internal 2d list.
        """
        #print(self.datas)
        for indexes in sorted(dictionary):
            x = int(indexes.split('x')[0])
            y = int(indexes.split('x')[1])
            # print(x, y)
            # print("self.datas[{}][{}] = dictionary['{}']".format(
            #     x - 1, y - 1, indexes))
            self.datas[x - 1][y - 1] = dictionary[indexes]
            #print(self.datas)

    def build(self, surf=None, topright=(0, 0), gap=7, bgcolour=COLOURS['black'], padding=2):
        """
        creates the surface of the inventory image
        :param surf: pass a surface if you want the image to be appended to the surface
        :param topright:the topright corner for the blitting to start
        :param gap: gap between blocks
        :param bgcolour: the background colour of the blocks
        :param padding: the padding on the edge of the surface
        :return: the new/appended surface
        """
        lengthx, lengthy = 0, 0
        blacksurf = pg.Surface((LARGEICONSIZE, LARGEICONSIZE))
        blacksurf.fill(bgcolour)

        # need to calculate dimensions of surface

        lenarry = len(self.datas)
        lenarrx = len(self.datas[0])    # length of the first element == all the others

        for i in range(lenarrx):
            lengthx += (gap + LARGEICONSIZE)
        lengthx += (padding * 2)   # the padding must be multiplied by 2, for both sides
        lengthx -= (LARGEICONSIZE - (padding + 1))

        for i in range(lenarry):
            lengthy += (gap + LARGEICONSIZE)
        lengthy += (padding * 2)
        lengthy -= (LARGEICONSIZE - (padding + 1))

        if surf is None:
            surf = pg.Surface((lengthx, lengthy))
            surf.fill((255, 255, 255))

        where_to_blit = list(map(lambda x: padding + x, topright))

        for x in range(lenarry):
            for i in range(lenarrx):
                # print('where to blit:', where_to_blit)
                surf.blit(blacksurf, where_to_blit)
                where_to_blit[0] += (LARGEICONSIZE + gap)
            where_to_blit[0] = (padding + topright[0])    # reset X coordinates
            where_to_blit[1] += (LARGEICONSIZE + gap)

        return surf



if __name__ == '__main__':
    a = InventoryHandler(2, 3)
    s = {
        '1x1': '0',
        '1x2': '1',
        '1x3': '2',
        '2x1': '3',
        '2x2': '4',
        '2x3': '5',
    }
    a.sort_dict(s)
    # pprint(a.datas)
    pg.image.save(a.build(), r'C:\Users\Michael\Desktop\image.png')
