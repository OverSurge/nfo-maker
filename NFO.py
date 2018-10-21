from pathlib import Path

from Category import Category


class NFO:
    def __init__(self, name: str, ctgs=None):
        self.name = 'Unnamed NFO' if name == '' else name
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
        for ctg in self.ctgs:
            res += str(ctg)
        return res

    def add_ctg(self, ctg: Category):
        self.ctgs.append(ctg)

    def del_ctg(self, index: int):
        if 1 <= index <= len(self.ctgs):
            name = self.ctgs[index-1].name
            if input('Are you sure to delete category "{}" ? (Y/n)\n> '.format(name)).lower() == 'y':
                self.ctgs.pop(index-1)
                print('Deleted category "{}"'.format(name))
            else:
                print('Canceled deletion.')
        else:
            raise IndexError

    def ren_ctg(self, index: int, new_name: str=''):
        if 1 <= index <= len(self.ctgs):
            name = self.ctgs[index-1].name
            if new_name == '':
                self.ctgs[index-1].name = input('Enter a new name for category "{}" :\n> '.format(name))
            else:
                self.ctgs[index].name = new_name
        else:
            raise IndexError

    def is_valid(self):
        if len(self.ctgs) > 0:
            return True
        else:
            raise Exception('NoCtg')

    def list_ctgs(self):
        res = ''
        for i in range(len(self.ctgs)):
            res += '{}: {}\n'.format(str(i+1).rjust(2), str(self.ctgs[i]).split('\n', 1)[0])
        return res

    def move_ctg(self, ctg: Category, direction: str):
        i = self.ctgs.index(ctg)
        if direction == 'up' and i != 0:
            self.ctgs[i], self.ctgs[i+1] = self.ctgs[i+1], self.ctgs[i]

    def save(self):
        out = open(self.path, 'w+')
        out.write(str(self))
        out.close()
        print('.nfo written at {}'.format(self.path))