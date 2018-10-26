import typing
import NFO
from Line import Line


class Category:
    count = 1

    def __init__(self, name: str='', lines: typing.List[Line]=None) -> None:
        self.name = 'Category ' + str(Category.count) if name == '' else name
        Category.count += 1
        if lines is None:
            self.lines = []
        else:
            self.lines = lines

    def __len__(self) -> int:
        if len(self.lines) == 0:
            return len(self.name)+4
        return max(len(self.name)+4, max([len(x) for x in self.lines]))

    def __repr__(self) -> str:
        width = NFO.nfo.width()
        if (width % 2 == 0 and len(self.name) % 2 == 0) or (width % 2 != 0 and len(self.name) % 2 != 0):
            res = '{0} {1} {0}'.format((width - len(self.name) - 2) // 2 * NFO.filler, self.name)
        else:
            res = '{0} {1} {2}'.format((width - len(self.name)) // 2 * NFO.filler, self.name,
                                       ((width - len(self.name)) // 2 - 1) * NFO.filler)
        for line in self.lines:
            res = res + '\n' + str(line)
        return res

    def add_line(self, line: Line=None) -> None:
        if line is None:
            name = input('Enter the new line\'s name :\n> ')
            value = input('Enter the value of "{}" :\n> '.format(name))
            self.lines.append(Line(name, value))
        elif isinstance(line, Line):
            self.lines.append(line)
        else:
            raise TypeError

    def contains_line(self):
        return len(self.lines) > 0

    def list_lines(self) -> str:
        res = ''
        for i in range(len(self.lines)):
            res += '{}: {}\n'.format(str(i + 1).rjust(2), str(self.lines[i]).split('\n', 1)[0])
        return res

    def del_line(self, index: int=None, force=False) -> None:
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

    def move_line(self, index: int=None, direction: str=None) -> None:
        if len(self.lines) == 2:
            self.lines[0], self.lines[1] = self.lines[1], self.lines[0]
        else:
            index = self.sel_line() if index is None else index
            if direction is None:
                while direction != 'up' and direction != 'down':
                    direction = input('Enter "up" or "down" to move line :\n> ')
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
        if index is None:
            index = self.sel_line()
        if new_name is None or new_value is None:
            name = self.lines[index].name
            new_name = input('Enter a new name for "{}" :\n> '.format(name))
            self.lines[index].name = new_name if new_name != '' else self.lines[index].name
            new_value = input('Enter a new value for "{}" :\n> '.format(self.lines[index].name))
            self.lines[index].value = new_value if new_value != '' else self.lines[index].value
        else:
            self.lines[index].name = new_name
            self.lines[index].value = new_value

    def sel_line(self) -> int:
        if len(self.lines) == 1:
            return 0
        else:
            print(self.list_lines())
            index = int(input('Enter line number :\n> '))
            if 1 <= index <= len(self.lines):
                return index - 1
            else:
                raise IndexError
