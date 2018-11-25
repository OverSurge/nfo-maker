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

import Category
import NFO


class Line:
    count = 1

    def __init__(self, category: Category, name: str='', value: str='') -> None:
        """Create a Line, defined by a category, a name and a value.
        :param category: Give the Category in which this Line is stored
        :param name: Should not start with an '=', max 40 chars
        :param value: Should not contain a ':'
        """
        self.category = category
        if len(name) > 0 and name[0] == '=':
            name = name[1:]
        name = name[:40]
        self.name = 'Line ' + str(Line.count) if name == '' else name
        value = value.replace(':', '')
        self.value = 'Ø' if value == '' else value
        Line.count += 1

    def __len__(self) -> int:
        """A Line's length is calculated by addition of the max name length, the length of its value, and 3 for ' : '
        in the middle of the 2 fields.
        The max name length is the maximum of the names' lengths in lines which are in the same Category as this Line.
        With this, all ' : ' and values are aligned horizontally.
        """
        return self.category.max_line_name_width() + len(self.value) + 3

    def __repr__(self) -> str:
        """If the line is larger than the width limit set in NFO, then it will be cut into multiple lines,
        without cutting words in half, otherwise it will be printed normally in one line.
        """
        if len(self) > NFO.NFO.max_width:
            words = self.value.split()
            if NFO.NFO.vertical_align:
                res = self.name.ljust(self.category.max_line_name_width()) + ' : '
            else:
                res = self.name + ' : '
            while len(words) > 0:
                if len(res.split('\n')[-1]) + len(words[0]) < NFO.NFO.max_width:
                    res += words.pop(0) + ' '
                else:
                    res += '\n' + words.pop(0) + ' '
            return res[:-1]
        if NFO.NFO.vertical_align:
            return self.name.ljust(self.category.max_line_name_width()) + ' : ' + self.value
        else:
            return self.name + ' : ' + self.value

    def set_category(self, category: Category):
        """Set the category of a Line."""
        self.category = category

    def set_name(self, new_name: str=None):
        """Set the name of a Line (max 40 chars)."""
        if new_name is None:
            new_name = input('Enter a new name for "{}"\n> '.format(self.name))
            if new_name == '':
                return
        if new_name[0] == '=':
            new_name = new_name[1:]
        new_name = new_name[:40]
        self.name = new_name.replace('\n', '').replace('\r', '')
    
    def set_value(self, new_value: str=None):
        """Set the value of a Line."""
        if new_value is None:
            new_value = input('Enter a new value for "{}" ("{}" before)\n> '.format(self.name, self.value))
            if new_value == '':
                return
        self.value = new_value.replace('\n', '').replace('\r', '').replace(':', '')
