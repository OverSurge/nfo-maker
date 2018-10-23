from pathlib import Path
from Category import Category
from Line import Line


class NFO:
    def __init__(self, name: str=None, ctgs: Category=None):
        if name is None:
            name = input('Enter a title (name) for your .nfo :\n> ')
            self.name = 'Unnamed NFO' if name == '' else name
        if ctgs is None:
            self.ctgs = []
        elif isinstance(ctgs, list):
            self.ctgs = ctgs
        else:
            self.ctgs = [ctgs]
        self._path = None

    def __repr__(self):
        res = self.name
        for ctg in self.ctgs:
            res = res + '\n\n' + str(ctg)
        return res

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

    def add_ctg(self, ctg=None) -> None:
        if ctg is None:
            self.ctgs.append(Category(input('Enter the new category\'s name :\n> ')))
        elif isinstance(ctg, Category):
            self.ctgs.append(ctg)
        elif isinstance(ctg, str):
            self.ctgs.append(Category(ctg))
        else:
            raise TypeError

    def del_ctg(self, index: int=None) -> None:
        if index is None:
            index = self.sel_ctg() if len(self.ctgs) != 1 else 0
        name = self.ctgs[index].name
        if input('Are you sure to delete category "{}" ? (Y/n)\n> '.format(name)).lower() == 'y':
            self.ctgs.pop(index)
            print('Deleted category "{}"'.format(name))
        else:
            print('Canceled deletion.')

    def list_ctgs(self) -> str:
        res = ''
        for i in range(len(self.ctgs)):
            res += '{}: {}\n'.format(str(i + 1).rjust(2), str(self.ctgs[i]).split('\n', 1)[0])
        return res

    def move_ctg(self, index: int=None, direction: str=None) -> None:
        index = self.sel_ctg() if index is None else index
        if direction is None:
            while direction != 'up' and direction != 'down':
                direction = input('Enter "up" or "down" to move category :\n> ')
        if direction == 'up':
            if index == 0:
                self.ctgs.append(self.ctgs[0])
                self.ctgs.pop(0)
            else:
                self.ctgs[index-1], self.ctgs[index] = self.ctgs[index], self.ctgs[index-1]
        elif direction == 'down':
            if index == len(self.ctgs) - 1:
                self.ctgs.insert(0, self.ctgs[-1])
                self.ctgs.pop()
            else:
                self.ctgs[index], self.ctgs[index+1] = self.ctgs[index+1], self.ctgs[index]
        else:
            raise IndexError

    def ren_ctg(self, index: int=None, new_name: str=None) -> None:
        if index is None:
            index = self.sel_ctg() if len(self.ctgs) != 1 else 0
        name = self.ctgs[index].name
        if new_name is None:
            self.ctgs[index].name = input('Enter a new name for category "{}" :\n> '.format(name))
        else:
            self.ctgs[index].name = new_name

    def sel_ctg(self) -> int:
        print(self.list_ctgs())
        index = int(input('Enter category number :\n> '))
        if 1 <= index <= len(self.ctgs):
            return index - 1
        else:
            raise IndexError

    def add_line(self, index: int=None, line: Line=None):
        if index is None:
            index = self.sel_ctg() if len(self.ctgs) != 1 else 0
        self.ctgs[index].add_line(line)

    def contains_line(self):
        for ctg in self.ctgs:
            if len(ctg.lines) > 0:
                return True
        return False

    def is_valid(self) -> bool:
        if len(self.ctgs) > 0:
            return True
        else:
            raise Exception('NoCtg')

    def rename(self, name: str=None):
        if name is None:
            name = input('Enter a new .nfo name :\n> ')
            self.name = 'Unnamed NFO' if name == '' else name
        else:
            self.name = name

    def save(self) -> None:
        out = open(self.path, 'w+')
        out.write(str(self))
        out.close()
        print('.nfo written at {}'.format(self.path))
