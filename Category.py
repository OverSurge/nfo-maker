from Line import Line


class Category:
    filler = '='

    def __init__(self, name: str, lines: list=None):
        self.name = ' ' + name + ' '
        if lines is None:
            self.lines = []
        else:
            self.lines = lines

    def __len__(self):
        return max(len(self.name)+2, max([len(x) for x in self.lines]))

    def __repr__(self):
        fill = (len(self) - len(self.name)) // 2 * self.filler
        res = fill + self.name + fill + '\n'
        for line in self.lines:

            res = res + str(line) + '\n'
        return res

    def add_line(self, line: Line):
        self.lines.append(line)
