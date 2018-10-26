import typing
from pathlib import Path
from Category import Category
from Line import Line

filler = '='
nfo = None


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class NFO:
    def __init__(self, name: str=None, ctgs: typing.List[Category]=None) -> None:
        global nfo
        if name is None:
            name = input('Enter a title (name) for your .nfo :\n> ')
            self.name = 'Unnamed NFO' if name == '' else name
        if ctgs is None:
            self.ctgs = []
        elif isinstance(ctgs, list):
            self.ctgs = ctgs
        elif isinstance(ctgs, Category):
            self.ctgs = [ctgs]
        else:
            raise TypeError
        self._path = None
        nfo = self

    def __repr__(self) -> str:
        res = self.name
        for ctg in self.ctgs:
            res = res + '\n\n' + str(ctg)
        return res + '\n'

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path) -> None:
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
            index = self.sel_ctg()
        name = self.ctgs[index].name
        if input('Are you sure to delete category "{}" ? (Y/n)\n> '.format(name)).upper() == 'Y':
            self.ctgs.pop(index)
            print('Deleted category "{}"'.format(name))
        else:
            print('Canceled deletion.')

    def list_ctgs(self, ctgs_list: typing.List[Category]=None) -> str:
        res = ''
        if ctgs_list is None:
            for i in range(len(self.ctgs)):
                res += '{}: {}\n'.format(str(i + 1).rjust(2), str(self.ctgs[i]).split('\n', 1)[0])
        else:
            for i in range(len(ctgs_list)):
                res += '{}: {}\n'.format(str(i + 1).rjust(2), str(ctgs_list[i]).split('\n', 1)[0])
        return res

    def move_ctg(self, index: int=None, direction: str=None) -> None:
        if len(self.ctgs) == 2:
            self.ctgs[0], self.ctgs[1] = self.ctgs[1], self.ctgs[0]
        else:
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
                raise ValueError

    def ren_ctg(self, index: int=None, new_name: str=None) -> None:
        if index is None:
            index = self.sel_ctg()
        name = self.ctgs[index].name
        if new_name is None:
            new_name = input('Enter a new name for category "{}" :\n> '.format(name))
            if new_name != '':
                self.ctgs[index].name = new_name
        else:
            self.ctgs[index].name = new_name

    def sel_ctg(self, contains_line: bool=False, exclude: typing.List[Category]=()) -> int:
        ctgs_list = [x for x in self.ctgs if x not in exclude]
        if len(ctgs_list) == 1:
            return self.ctgs.index(ctgs_list[0])
        if contains_line:
            ctgs_list = [x for x in self.ctgs if x.contains_line() and x not in exclude]
            if len(ctgs_list) == 1:
                return 0
        print(self.list_ctgs(ctgs_list))
        index = int(input('Enter category number :\n> '))
        if 1 <= index <= len(ctgs_list):
            return self.ctgs.index(ctgs_list[index-1])
        else:
            raise IndexError

    def add_line(self, index: int=None, line: Line=None) -> None:
        if index is None:
            index = self.sel_ctg()
        self.ctgs[index].add_line(line)

    def contains_line(self) -> bool:
        for ctg in self.ctgs:
            if ctg.contains_line():
                return True
        return False

    def del_line(self, ctg_index: int=None, line_index: int=None) -> None:
        if ctg_index is None:
            ctg_index = self.sel_ctg()
        self.ctgs[ctg_index].del_line(line_index)

    def move_line(self, ctg_index: int=None, line_index: int=None, direction: str=None) -> None:
        if ctg_index is None:
            ctg_index = self.sel_ctg(True, [x for x in self.ctgs if len(x.lines) < 2])
        self.ctgs[ctg_index].move_line(line_index, direction)

    def move_line_to_ctg(self, src_ctg_index: int=None, line_index: int=None, out_ctg_index: int=None) -> None:
        if src_ctg_index is None or line_index is None or out_ctg_index is None:
            self.list_ctgs([x for x in self.ctgs if x.contains_line()])
            src_ctg_index = self.sel_ctg(True, [x for x in self.ctgs if not x.contains_line()])
            line_index = self.ctgs[src_ctg_index].sel_line()
            out_ctg_index = self.sel_ctg(False, [self.ctgs[src_ctg_index]])
        self.ctgs[out_ctg_index].add_line(self.ctgs[src_ctg_index].lines[line_index])
        self.ctgs[src_ctg_index].del_line(line_index, True)

    def ren_line(self, ctg_index: int=None, line_index: int=None, new_name: str=None, new_value: str=None) -> None:
        if ctg_index is None:
            ctg_index = self.sel_ctg()
        self.ctgs[ctg_index].ren_line(line_index, new_name, new_value)

    def rename(self, name: str=None) -> None:
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

    def width(self) -> int:
        return max([len(x) for x in self.ctgs])
