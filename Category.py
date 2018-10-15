from Line import Line


class Category:
    def __init__(self, name: str, lines: list=None):
        self.name = name
        if lines is None:
            self.lines = []
        else:
            self.lines = lines

    def __len__(self):
        return max(len(self.name)+2, max([len(x) for x in self.lines]))

    def __repr__(self):
        res = ""
        for line in self.lines:
            res += line
        return res

    def add_line(self, line: Line):
        self.lines.append(line)
