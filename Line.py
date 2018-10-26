class Line:
    count = 1

    def __init__(self, name: str='', value: str='') -> None:
        self.name = 'Line ' + str(Line.count) if name == '' else name
        Line.count += 1
        self.value = 'Ø' if value == '' else value

    def __len__(self) -> int:
        return len(self.name) + len(self.value) + 3

    def __repr__(self) -> str:
        return self.name + ' : ' + self.value
