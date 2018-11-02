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

import typing
import NFO
from Line import Line


class Category:
    count = 1

    def __init__(self, name: typing.Union[str, None]='', lines: typing.List[Line]=None) -> None:
        """A Category is defined by a name and a list of Line.

        :param name: Should not contain an '='. If None, will be empty. If '', will ask user to type a name
        :param lines:
        """
        if name is None:
            self.name = ''
        elif name == '':
            if input('Create an unnamed category ? (Y/n)\n> ').upper() == 'N':
                self.name = 'Category ' + str(Category.count)
            else:
                self.name = ''
        else:
            self.name = name.replace('=', '')[:NFO.NFO.max_width - 4]
        if lines is None:
            self.lines = []
        else:
            self.lines = lines
        Category.count += 1

    def __getitem__(self, item):
        return self.lines[item]

    def __iter__(self):
        return self.lines.__iter__()

    def __len__(self) -> int:
        """The length of a Category's title is the length of its name + 4 because there is at least 2 '=' and 2 spaces
        in a title.
        Considering this, there is 2 possible values for the length of a Category :
        - If there is no Line in the Category or if its title's length is greater than the length of
        the longest Line in the Category, then the Category's length will be the length of its title.
        - If the length of the longest Line in the Category is greater than the title's length, then
        the Category's length will be the length of the longest Line in the Category.
        """
        if len(self.lines) == 0:
            return len(self.name)+4
        return min(NFO.NFO.max_width, max(len(self.name)+4, max([len(x) for x in self.lines])))

    def __repr__(self) -> str:
        """Category's __repr__ is made of 2 sections : A title and its content.

        If the Category's name is empty, then the title is only made of '='.
        Otherwise, the title is made of one or more '=', a space, the Category's name, a space, and one or more '='.
        The number of '=' depends on the length of the NFO, there is at least one on each side.
        If the number of '=' on the left and on the right have to be different, there will be 1 more '=' on the left.
        It can occur for example if the width of the NFO is odd and the length of the Category's name is even.

        Its content is made of the concatenation of all its lines' __repr__.
        """
        width = NFO.NFO.width()
        if len(self.name) == 0:
            res = width * '='
        else:
            if (width % 2 == 0 and len(self.name) % 2 == 0) or (width % 2 != 0 and len(self.name) % 2 != 0):
                res = '{0} {1} {0}'.format((width - len(self.name) - 2) // 2 * '=', self.name)
            else:
                res = '{0} {1} {2}'.format((width - len(self.name)) // 2 * '=', self.name,
                                           ((width - len(self.name)) // 2 - 1) * '=')
        for line in self.lines:
            res = res + '\n' + str(line)
        return res

    def set_name(self, new_name: str=None):
        """Set the name of a Category."""
        if new_name is None:
            new_name = input('Enter a new name for "{}"\n> '.format(self.name))
            if new_name == '':
                return
        if new_name[0] == '=':
            new_name = new_name[1:]
        self.name = new_name.replace('=', '')[:NFO.NFO.max_width-4]

    def max_line_name_width(self):
        """Return the maximum length of a Line's name in this Category."""
        return max([len(x.name) for x in self.lines])

    def add_line(self, line: Line=None) -> None:
        """Add a Line to the Category."""
        if line is None:
            name = input('Enter the new line\'s name\n> ')
            if name == '':
                name = 'Line ' + str(Line.count)
            elif name[0] == '=':
                name = name[1:]
            value = input('Enter the value of "{}"\n> '.format(name))
            self.lines.append(Line(self, name, value))
        elif isinstance(line, Line):
            line.set_category(self)
            self.lines.append(line)
        else:
            raise TypeError

    def contains_line(self):
        """Return True if there is at least 1 Line in the Category, False otherwise."""
        return len(self.lines) > 0

    def del_line(self, index: int=None, force=False) -> None:
        """Delete a Line from the Category.

        :param index: The index of the Line in the Category's Line list
        :param force: If set to True, it will delete the Line without confirmation
        """
        if index is None:
            index = self.sel_line()
        name = self.lines[index].name
        if force:
            self.lines.pop(index)
        elif input('Are you sure to delete line "{}" ? (Y/n)\n> '.format(name)).upper() == 'Y':
            self.lines.pop(index)
            print('Deleted line "{}"'.format(name))
        else:
            print('Canceled deletion.')

    def list_lines(self) -> str:
        """Return a string containing the list of all lines in the Category, numbered from 1 for readability."""
        res = ''
        for i in range(len(self.lines)):
            res += '{}: {}\n'.format(str(i + 1).rjust(2), str(self.lines[i]).split('\n', 1)[0])
        return res

    def move_line(self, index: int=None, direction: str=None) -> None:
        """Move a Line upwards or downwards inside a Category. It can move from top to bottom and vice versa.

        :param index: The index of the Line in the Category's Line list
        :param direction: "up" or "down"
        """
        if len(self.lines) == 2:
            self.lines[0], self.lines[1] = self.lines[1], self.lines[0]
        else:
            index = self.sel_line() if index is None else index
            if direction is None:
                while direction != 'up' and direction != 'down':
                    direction = input('Enter "up" or "down" to move line\n> ')
            if direction == 'up':
                if index == 0:
                    self.lines.append(self.lines[0])
                    self.lines.pop(0)
                else:
                    self.lines[index-1], self.lines[index] = self.lines[index], self.lines[index-1]
            elif direction == 'down':
                if index == len(self.lines) - 1:
                    self.lines.insert(0, self.lines[-1])
                    self.lines.pop()
                else:
                    self.lines[index], self.lines[index+1] = self.lines[index+1], self.lines[index]
            else:
                raise ValueError

    def ren_line(self, index: int=None, new_name: str=None, new_value: str=None) -> None:
        """Rename a Line in the Category's Line list.

        :param index: The index of the Line in the Category's Line list
        :param new_name:
        :param new_value:
        """
        if index is None:
            index = self.sel_line()
        self.lines[index].set_name(new_name)
        self.lines[index].set_value(new_value)

    def sel_line(self) -> int:
        """Print all lines in the Category and return the index of the Line the user chose.
        If there is only 1 Line, return 0."""
        if len(self.lines) == 1:
            return 0
        else:
            print(self.list_lines())
            index = int(input('Enter line number\n> '))
            if 1 <= index <= len(self.lines):
                return index - 1
            else:
                raise IndexError
