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


class Line:
    count = 1

    def __init__(self, name: str='', value: str='') -> None:
        if len(name) > 0 and name[0] == '=':
            name = name[1:]
        self.name = 'Line ' + str(Line.count) if name == '' else name
        Line.count += 1
        self.value = 'Ø' if value == '' else value

    def __len__(self) -> int:
        return len(self.name) + len(self.value) + 3

    def __repr__(self) -> str:
        return self.name + ' : ' + self.value
