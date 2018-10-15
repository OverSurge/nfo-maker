class Line:
    def __init__(self, name: str="", value: str=""):
        self.name = name
        self.value = value

    def __len__(self):
        return len(self.name) + len(self.value) + 3

    def __repr__(self):
        return self.name + " : " + self.value
