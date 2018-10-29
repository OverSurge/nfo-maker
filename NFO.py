# NFO Maker
# Copyright (C) 2018  OverSurge
#
# NFO Maker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NFO Maker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NFO Maker.  If not, see <https://www.gnu.org/licenses/>.

import re
import typing
from pathlib import Path
from Category import Category
from Line import Line


class MetaNFO(type):
    def __repr__(cls) -> str:
        res = NFO.name
        for ctg in NFO.ctgs:
            res = res + '\n\n' + str(ctg)
        return res + '\n'


class NFO(metaclass=MetaNFO):
    name = None
    ctgs = None
    __path = None

    @classmethod
    def __init__(cls, name: str=None, ctgs: typing.List[Category]=None) -> None:
        if name is None:
            name = input('Enter a title (name) for your .nfo\n> ')
            cls.name = 'Unnamed NFO' if name == '' else name
        else:
            cls.name = name

        if ctgs is None:
            cls.ctgs = []
        elif isinstance(ctgs, list):
            cls.ctgs = ctgs
        elif isinstance(ctgs, Category):
            cls.ctgs = [ctgs]
        else:
            raise TypeError

        cls.__path = None

    @classmethod
    def load(cls, path: Path=None) -> None:
        if path is None:
            folder = None
            while folder is None:
                folder = input('Enter the file\'s folder path (leave empty to search in {})\n> '.format(Path().absolute()))
                folder = folder if folder != '' and Path(folder).is_dir() else '.'
                folder += '\\' if folder[-1:] == ':' else ''
                nfo_files = [x for x in Path.iterdir(Path(folder)) if x.suffix == '.nfo']
                if len(nfo_files) == 0:
                    folder = None
                    if input('There is no .nfo file in this directory, continue ? (Y/n)\n> ').upper() != 'Y':
                        return
                else:
                    choices = '\n'
                    for i in range(len(nfo_files)):
                        choices += '{}: {}\n'.format(str(i + 1).rjust(2), str(nfo_files[i].absolute()))
                    print(choices)
                    index = int(input('Enter the file\'s number\n> '))
                    if 1 <= index <= len(nfo_files):
                        path = nfo_files[index - 1]
                        path.absolute()
                    else:
                        raise IndexError
        if path.is_file():
            if len(NFO.ctgs) > 0:
                if input('All unsaved changes will be lost if you load a new .nfo.\n'
                         'Do you still want to load {} ? (Y/n)\n> '.format(path.absolute())).upper() != 'Y':
                    print('Cancelled load.')
                    return
            cls.parse(open(str(path.absolute()), 'r'))
        else:
            raise FileNotFoundError

    @classmethod
    def parse(cls, file: typing.TextIO) -> None:
        nfo = None
        tmp_ctg = None
        for line in file:
            if nfo is None:
                nfo = NFO(line[:-1])
            elif line == '\n' and tmp_ctg is not None:
                NFO.add_ctg(tmp_ctg)
                tmp_ctg = None
            elif line[0] == '=':
                tmp_ctg = Category(re.findall(r"=* (.*) =*", line)[0])
            elif re.match(r".* : .*", line):
                name, value = re.findall(r"(.*) : (.*)", line)[0]
                tmp_ctg.add_line(Line(name, value))
        if tmp_ctg is not None:
            NFO.add_ctg(tmp_ctg)

    @classmethod
    def rename(cls, name: str=None) -> None:
        if name is None:
            name = input('Enter a new .nfo name\n> ')
            cls.name = name if name != '' else cls.name
        else:
            cls.name = name

    @classmethod
    def save(cls) -> None:
        if cls.__path is None:
            if not cls.set_path():
                print('Canceled writing.')
                return
        elif input('Do you want to save at {} ? (Y/n)\n> '.format(cls.__path)).upper() != 'Y':
            if not cls.set_path():
                print('Canceled writing.')
                return
        out = open(str(cls.__path.absolute()), 'w+')
        out.write(str(cls))
        out.close()
        print('.nfo written at {}'.format(cls.__path))

    @classmethod
    def set_path(cls, path: Path=None) -> bool:
        if path is None:
            folder = input('Enter a folder path (leave empty to save in {})\n> '.format(Path().absolute()))
            folder = folder if folder != '' and Path(folder).is_dir() else '.'
            folder += '\\' if folder[-1:] == ':' else ''
            filename = input('Enter a filename (leave empty to save as {})\n> '.format(cls.name + '.nfo'))
            if filename == '':
                filename = cls.name + '.nfo'
            else:
                filename += '.nfo' if filename[-4:] != '.nfo' else ''
            path = Path(folder + '/' + filename).absolute()
            if input('{}\nIs this path right ? (Y/n)\n> '.format(path)).upper() == 'Y':
                cls.__path = path
                return True
            else:
                return False
        elif path.is_file():
            cls.__path = path
            return True
        else:
            raise FileNotFoundError

    @classmethod
    def width(cls) -> int:
        return max([len(x) for x in cls.ctgs])

    @classmethod
    def add_ctg(cls, ctg: Category=None) -> None:
        if ctg is None:
            cls.ctgs.append(Category(input('Enter the new category\'s name\n> ')))
        elif isinstance(ctg, Category):
            cls.ctgs.append(ctg)
        elif isinstance(ctg, str):
            cls.ctgs.append(Category(ctg))
        else:
            raise TypeError

    @classmethod
    def del_ctg(cls, index: int=None) -> None:
        if index is None:
            index = cls.sel_ctg()
        name = cls.ctgs[index].name
        if input('Are you sure to delete category "{}" ? (Y/n)\n> '.format(name)).upper() == 'Y':
            cls.ctgs.pop(index)
            print('Deleted category "{}"'.format(name))
        else:
            print('Canceled deletion.')

    @classmethod
    def list_ctgs(cls, ctgs_list: typing.List[Category]=None) -> str:
        res = ''
        if ctgs_list is None:
            for i in range(len(cls.ctgs)):
                res += '{}: {}\n'.format(str(i + 1).rjust(2), str(cls.ctgs[i]).split('\n', 1)[0])
        else:
            for i in range(len(ctgs_list)):
                res += '{}: {}\n'.format(str(i + 1).rjust(2), str(ctgs_list[i]).split('\n', 1)[0])
        return res

    @classmethod
    def move_ctg(cls, index: int=None, direction: str=None) -> None:
        if len(cls.ctgs) == 2:
            cls.ctgs[0], cls.ctgs[1] = cls.ctgs[1], cls.ctgs[0]
        else:
            index = cls.sel_ctg() if index is None else index
            if direction is None:
                while direction != 'up' and direction != 'down':
                    direction = input('Enter "up" or "down" to move category\n> ')
            if direction == 'up':
                if index == 0:
                    cls.ctgs.append(cls.ctgs[0])
                    cls.ctgs.pop(0)
                else:
                    cls.ctgs[index-1], cls.ctgs[index] = cls.ctgs[index], cls.ctgs[index-1]
            elif direction == 'down':
                if index == len(cls.ctgs) - 1:
                    cls.ctgs.insert(0, cls.ctgs[-1])
                    cls.ctgs.pop()
                else:
                    cls.ctgs[index], cls.ctgs[index+1] = cls.ctgs[index+1], cls.ctgs[index]
            else:
                raise ValueError

    @classmethod
    def ren_ctg(cls, index: int=None, new_name: str=None) -> None:
        if index is None:
            index = cls.sel_ctg()
        name = cls.ctgs[index].name
        if new_name is None:
            new_name = input('Enter a new name for category "{}"\n> '.format(name))
            if new_name != '':
                cls.ctgs[index].name = new_name
        else:
            cls.ctgs[index].name = new_name

    @classmethod
    def sel_ctg(cls, contains_line: bool=False, exclude: typing.List[Category]=()) -> int:
        ctgs_list = [x for x in cls.ctgs if x not in exclude]
        if len(ctgs_list) == 1:
            return cls.ctgs.index(ctgs_list[0])
        if contains_line:
            ctgs_list = [x for x in cls.ctgs if x.contains_line() and x not in exclude]
            if len(ctgs_list) == 1:
                return 0
        print(cls.list_ctgs(ctgs_list))
        index = int(input('Enter category number\n> '))
        if 1 <= index <= len(ctgs_list):
            return cls.ctgs.index(ctgs_list[index-1])
        else:
            raise IndexError

    @classmethod
    def add_line(cls, index: int=None, line: Line=None) -> None:
        if index is None:
            index = cls.sel_ctg()
        cls.ctgs[index].add_line(line)

    @classmethod
    def contains_line(cls) -> bool:
        for ctg in cls.ctgs:
            if ctg.contains_line():
                return True
        return False

    @classmethod
    def del_line(cls, ctg_index: int=None, line_index: int=None) -> None:
        if ctg_index is None:
            ctg_index = cls.sel_ctg()
        cls.ctgs[ctg_index].del_line(line_index)

    @classmethod
    def move_line(cls, ctg_index: int=None, line_index: int=None, direction: str=None) -> None:
        if ctg_index is None:
            ctg_index = cls.sel_ctg(True, [x for x in cls.ctgs if len(x.lines) < 2])
        cls.ctgs[ctg_index].move_line(line_index, direction)

    @classmethod
    def move_line_to_ctg(cls, src_ctg_index: int=None, line_index: int=None, out_ctg_index: int=None) -> None:
        if src_ctg_index is None or line_index is None or out_ctg_index is None:
            cls.list_ctgs([x for x in cls.ctgs if x.contains_line()])
            src_ctg_index = cls.sel_ctg(True, [x for x in cls.ctgs if not x.contains_line()])
            line_index = cls.ctgs[src_ctg_index].sel_line()
            out_ctg_index = cls.sel_ctg(False, [cls.ctgs[src_ctg_index]])
        cls.ctgs[out_ctg_index].add_line(cls.ctgs[src_ctg_index].lines[line_index])
        cls.ctgs[src_ctg_index].del_line(line_index, True)

    @classmethod
    def ren_line(cls, ctg_index: int=None, line_index: int=None, new_name: str=None, new_value: str=None) -> None:
        if ctg_index is None:
            ctg_index = cls.sel_ctg()
        cls.ctgs[ctg_index].ren_line(line_index, new_name, new_value)
