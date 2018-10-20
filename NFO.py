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
        self._path = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        if path is not None:
            if isinstance(path, Path):
                self._path = path
            elif isinstance(path, str):
                self._path = Path(path)

    def __repr__(self):
        res = self.name + '\n\n'
        for cat in self.ctgs:
            res += str(cat)
        return res

    def add_ctg(self, ctg: Category):
        self.ctgs.append(ctg)

    def is_valid(self):
        if len(self.ctgs) > 0:
            return True
        else:
            raise Exception('NoCtg')

    def move_ctg(self, ctg: Category, direction: str):
        i = self.ctgs.index(ctg)
        if direction == 'up' and i != 0:
            self.ctgs[i], self.ctgs[i+1] = self.ctgs[i+1], self.ctgs[i]

    def save(self):
        out = open(self.path, 'w+')
        out.write(str(self))
        out.close()
        print('.nfo written at {}'.format(self.path))
