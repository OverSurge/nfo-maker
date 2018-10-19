import os

from Category import Category


class NFO:
    def __init__(self, name: str="Unnamed", categories=None):
        self.name = name
        if categories is None:
            self.categories = []
        elif isinstance(categories, list):
            self.categories = categories
        else:
            self.categories = [categories]

    def __repr__(self):
        res = self.name + "\n\n"
        for cat in self.categories:
            res += str(cat)
        return res

    def add_category(self, category: Category):
        self.categories.append(category)

    def write(self, path=None):
        if path is None:
            if os.name == "nt":
                path = os.getenv("TMP") + "\\" + self.name + ".nfo"
            else:
                path = "/tmp/" + self.name + ".nfo"
        out = open(path, "w+")
        out.write(str(self))
        out.close()
