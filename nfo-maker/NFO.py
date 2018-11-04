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
    """Metaclass used by NFO in order to have class __getitem__, __iter__ and __repr__."""
    def __getitem__(cls, item):
        return NFO.categories[item]

    def __iter__(cls):
        return NFO.categories.__iter__()

    def __repr__(cls) -> str:
        res = NFO.name
        for ctg in NFO:
            res = res + '\n\n' + str(ctg)
        return res + '\n'


class NFO(metaclass=MetaNFO):
    """The representation of the structure of a .nfo file."""
    name: str = None
    categories: typing.List[Category] = None
    max_width: int = 80
    __path: Path = None

    @classmethod
    def __init__(cls, name: str=None, categories: typing.List[Category]=None) -> None:
        """There is only one NFO stored at the same time."""
        if name is None:
            name = input('Enter a title (name) for your .nfo\n> ')
            cls.name = 'Unnamed NFO' if name == '' else name
        else:
            cls.name = name

        if categories is None:
            cls.categories = []
        elif isinstance(categories, list):
            cls.categories = categories
        elif isinstance(categories, Category):
            cls.categories = [categories]
        else:
            raise TypeError

        cls.__path = None

    @classmethod
    def load(cls, path: Path=None) -> None:
        """Load the .nfo file located at path.

        :param path: If empty, the user will have to enter the path of a folder containing at least 1 .nfo
        and choose which .nfo in the directory he wants to open
        """
        if path is None:
            folder = None
            if cls.__path is not None:
                if input('Do you want to load {} ? (Y/n)\n> '.format(cls.__path.absolute())).upper() == 'Y':
                    folder = True
                    path = cls.__path
            while folder is None:
                folder = input('Enter the file\'s folder path (leave empty to search in {})\n> '
                               .format(Path().absolute()))
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
            if NFO.categories is not None and len(NFO.categories) > 0:
                if input('All unsaved changes will be lost if you load a new .nfo.\n'
                         'Do you still want to load {} ? (Y/n)\n> '.format(path.absolute())).upper() != 'Y':
                    print('Cancelled load.')
                    return
            cls.parse(path)
        else:
            raise FileNotFoundError

    @classmethod
    def parse(cls, path: Path) -> None:
        """Parse the file located at path to load its structure in NFO Maker.
        The operation can fail if the file hasn't been generated with NFO Maker.
        If a line is only made of the same character, then it does not give any information, so it is ignored,
        except if it's made of '=', then it is considered as a new unnamed Category.
        """
        file = open(str(path.absolute()), 'r', encoding='utf8')
        nfo = None
        tmp_ctg = None
        for line in file:
            if not (len(line.strip()) > 0 and line.strip() == len(line.strip()) * line.strip()[0]):
                if nfo is None:
                    nfo = NFO(line[:-1].strip())
                    NFO.set_path(path)
                elif re.match(r".*=+ .* =+.*", line):
                    if tmp_ctg is not None:
                        NFO.add_ctg(tmp_ctg)
                    tmp_ctg = Category(re.findall(r".*=+ (.*) =+.*", line)[0])
                elif re.match(r".* : .*", line):
                    name, value = re.findall(r"(.*) : (.*)", line)[0]
                    name = name.rstrip()
                    value = value.lstrip()
                    tmp_ctg.add_line(Line(tmp_ctg, name, value))
                elif line.strip() != '' and tmp_ctg is not None and tmp_ctg.contains_line():
                    tmp_ctg[-1].value += ' ' + line[:-1]
            elif len(line.strip()) > 0 and line.strip() == len(line.strip()) * '=':
                if tmp_ctg is not None:
                    NFO.add_ctg(tmp_ctg)
                tmp_ctg = Category(None)
        if tmp_ctg is not None:
            NFO.add_ctg(tmp_ctg)

    @classmethod
    def rename(cls, name: str=None) -> None:
        """Rename the NFO."""
        if name is None:
            name = input('Enter a new .nfo name\n> ')
            cls.name = name if name != '' else cls.name
        else:
            cls.name = name

    @classmethod
    def save(cls, path: Path=None) -> None:
        """Save the NFO into a file."""
        if path is None:
            if cls.__path is None:
                if not cls.set_path():
                    print('Canceled writing.')
                    return
            elif input('Do you want to save at {} ? (Y/n)\n> '.format(cls.__path.absolute())).upper() != 'Y':
                if not cls.set_path():
                    print('Canceled writing.')
                    return
        else:
            if path.is_dir():
                raise FileNotFoundError
            path += '.nfo' if path[-4:] != '.nfo' else ''
            cls.__path = path
        if cls.__path.is_file() and input('This file exists, overwrite ? (Y/n)\n> ').upper() != 'Y':
            raise FileExistsError
        try:
            out = open(str(cls.__path.absolute()), 'w+', encoding='utf8')
            out.write(str(cls))
            out.close()
        except PermissionError:
            print('This file is protected, writing cancelled !')
        else:
            print('.nfo written at {}'.format(cls.__path))

    @classmethod
    def set_max_width(cls, width: int=None) -> None:
        """Set the max width of the current NFO."""
        if width is None:
            width = int(input('Enter the new width (60 - 120) of this .nfo ({} before)\n> '.format(cls.max_width)))
        if 60 < width < 120:
            cls.max_width = width
        else:
            print('Out of range (60 - 120).')

    @classmethod
    def set_path(cls, path: Path=None) -> bool:
        """Set the path where the current NFO is located."""
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
        """Return the width of the NFO, determined by the largest Category in the NFO."""
        if len(cls.categories) == 0:
            return len(cls.name)
        return max([len(x) for x in cls])

    @classmethod
    def add_ctg(cls, category: Category=None) -> None:
        """Add a Category to the NFO."""
        if category is None:
            cls.categories.append(Category(input('Enter the new category\'s name\n> ')))
        else:
            cls.categories.append(category)

    @classmethod
    def del_ctg(cls, index: int=None) -> None:
        """Delete a Category from the NFO.

        :param index: The index of the Category in the NFO
        """
        if index is None:
            index = cls.sel_ctg()
        name = cls[index].name
        if input('Are you sure to delete category "{}" ? (Y/n)\n> '.format(name)).upper() == 'Y':
            cls.categories.pop(index)
            print('Deleted category "{}"'.format(name))
        else:
            print('Canceled deletion.')

    @classmethod
    def list_categories(cls, categories: typing.List[Category]=None) -> str:
        """Return a string containing the list of all categories in the NFO, numbered from 1 for readability."""
        res = ''
        if categories is None:
            for i in range(len(cls.categories)):
                res += '{}: {}\n'.format(str(i + 1).rjust(2), str(cls[i]).split('\n', 1)[0])
        else:
            for i in range(len(categories)):
                res += '{}: {}\n'.format(str(i + 1).rjust(2), str(categories[i]).split('\n', 1)[0])
        return res

    @classmethod
    def move_ctg(cls, index: int=None, direction: str=None) -> None:
        """Move a Category upwards or downwards inside the NFO. It can move from top to bottom and vice versa.

        :param index: The index of the Category in the NFO
        :param direction: "up" or "down"
        """
        if len(cls.categories) == 2:
            cls[0], cls[1] = cls[1], cls[0]
        else:
            index = cls.sel_ctg() if index is None else index
            if direction is None:
                while direction != 'up' and direction != 'down':
                    direction = input('Enter "up" or "down" to move category\n> ')
            if direction == 'up':
                if index == 0:
                    cls.categories.append(cls[0])
                    cls.categories.pop(0)
                else:
                    cls[index - 1], cls[index] = cls[index], cls[index - 1]
            elif direction == 'down':
                if index == len(cls.categories) - 1:
                    cls.categories.insert(0, cls[-1])
                    cls.categories.pop()
                else:
                    cls[index], cls[index + 1] = cls[index + 1], cls[index]
            else:
                raise ValueError

    @classmethod
    def ren_ctg(cls, index: int=None, new_name: str=None) -> None:
        """Rename a Category in the NFO.

        :param index: The index of the Category in the NFO
        :param new_name:
        """
        if index is None:
            index = cls.sel_ctg()
        cls[index].set_name(new_name)

    @classmethod
    def sel_ctg(cls, contains_line: bool=False, exclude: typing.List[Category]=()) -> int:
        """Print all categories in the NFO and return the index of the Category the user chose.
        If there is only 1 Category, return 0."""
        categories = [x for x in cls if x not in exclude]
        if len(categories) == 1:
            return cls.categories.index(categories[0])
        if contains_line:
            categories = [x for x in cls if x.contains_line() and x not in exclude]
            if len(categories) == 1:
                return 0
        print(cls.list_categories(categories))
        index = int(input('Enter category number\n> '))
        if 1 <= index <= len(categories):
            return cls.categories.index(categories[index - 1])
        else:
            raise IndexError

    @classmethod
    def add_line(cls, index: int=None, line: Line=None) -> None:
        """Add a Line to a Category."""
        if index is None:
            index = cls.sel_ctg()
        cls[index].add_line(line)

    @classmethod
    def contains_line(cls) -> bool:
        """Return True if at least 1 Category contains a Line or more, otherwise False."""
        for ctg in cls:
            if ctg.contains_line():
                return True
        return False

    @classmethod
    def del_line(cls, ctg_index: int=None, line_index: int=None) -> None:
        """Delete a Line in a Category."""
        if ctg_index is None:
            ctg_index = cls.sel_ctg()
        cls[ctg_index].del_line(line_index)

    @classmethod
    def move_line(cls, ctg_index: int=None, line_index: int=None, direction: str=None) -> None:
        """Move a Line inside a Category."""
        if ctg_index is None:
            ctg_index = cls.sel_ctg(True, [x for x in cls if len(x.lines) < 2])
        cls[ctg_index].move_line(line_index, direction)

    @classmethod
    def move_line_to_ctg(cls, src_ctg_index: int=None, line_index: int=None, out_ctg_index: int=None) -> None:
        """Move a Line from one Category of the NFO to another.

        :param src_ctg_index: The index of the Category where the Line is located
        :param line_index: The index of the Line in the source Category's Line list
        :param out_ctg_index: The index of the Category where to move the Line
        """
        if src_ctg_index is None or line_index is None or out_ctg_index is None:
            cls.list_categories([x for x in cls if x.contains_line()])
            src_ctg_index = cls.sel_ctg(True, [x for x in cls if not x.contains_line()])
            line_index = cls[src_ctg_index].sel_line()
            out_ctg_index = cls.sel_ctg(False, [cls[src_ctg_index]])
        cls[out_ctg_index].add_line(cls[src_ctg_index][line_index])
        cls[src_ctg_index].del_line(line_index, True)

    @classmethod
    def ren_line(cls, ctg_index: int=None, line_index: int=None, new_name: str=None, new_value: str=None) -> None:
        """Rename a Line in a Category."""
        if ctg_index is None:
            ctg_index = cls.sel_ctg()
        cls[ctg_index].ren_line(line_index, new_name, new_value)
