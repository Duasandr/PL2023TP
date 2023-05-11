from value import Value

class Key:
    def __init__(self, type_, value: Value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Key: {self.type}: {self.value}'