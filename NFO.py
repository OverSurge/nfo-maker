import os

from pathlib import Path

from Category import Category


class NFO:
    def __init__(self, name: str='Unnamed', ctgs=None):
        self.name = name
        if ctgs is None:
            self.ctgs = []
        elif isinstance(ctgs, list):
            self.ctgs = ctgs
        else:
            self.ctgs = [ctgs]

    def __repr__(self):
        res = self.name + '\n\n'
        for cat in self.ctgs:
            res += str(cat)
        return res

    def add_ctg(self, ctg: Category):
        self.ctgs.append(ctg)

    def write(self, path=None):
        if path is None:
            path = Path('.' + '/' + self.name + '.nfo').absolute()
        elif path[-4:] != '.nfo':
            path += '.nfo'
        out = open(path, 'w+')
        out.write(str(self))
        out.close()
        return '.nfo written at {}'.format(path)

    def move_ctg(self, ctg: Category, direction: str):
        i = self.ctgs.index(ctg)
        if direction == 'up' and i != 0:
            self.ctgs[i], self.ctgs[i+1] = self.ctgs[i+1], self.ctgs[i]
