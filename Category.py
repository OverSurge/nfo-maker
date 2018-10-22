from Line import Line


class Category:
    count = 1
    filler = '='

    def __init__(self, name: str='', lines: list=None):
        self.name = 'Category ' + str(Category.count) if name == '' else name
        Category.count += 1
        if lines is None:
            self.lines = []
        else:
            self.lines = lines

    def __len__(self):
        if len(self.lines) == 0:
            return len(self.name)+4
        return max(len(self.name)+4, max([len(x) for x in self.lines]))

    def __repr__(self):
        width = len(self)
        if (width % 2 == 0 and len(self.name) % 2 == 0) or (width % 2 != 0 and len(self.name) % 2 != 0):
            res = '{0} {1} {0}'.format((width - len(self.name) - 2) // 2 * self.filler, self.name)
        else:
            res = '{0} {1} {2}'.format((width - len(self.name)) // 2 * self.filler, self.name, ((width - len(self.name)) // 2 - 1) * self.filler)
        for line in self.lines:
            res = res + '\n' + str(line)
        return res

    def add_line(self, line: Line=None):
        if line is None:
            name = input('Enter the new line\'s name :\n> ')
            value = input('Enter the value of "{}" :\n> '.format(name))
            self.lines.append(Line(name, value))
        elif isinstance(line, Line):
            self.lines.append(line)
        else:
            raise TypeError
