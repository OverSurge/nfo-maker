from Category import Category


class NFO:
    def __init__(self, categories=None):
        if categories is None:
            self.categories = []
        elif isinstance(categories, list):
            self.categories = categories
        else:
            self.categories = [categories]

    def add_category(self, category: Category):
        self.categories.append(category)

    def __repr__(self):
        res = ""
        for cat in self.categories:
            res += str(cat)
        return res
