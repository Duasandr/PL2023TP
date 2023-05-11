from value import Value


class Array:
    def __init__(self, value_list: [Value]):
        self.value_list = value_list

    def __repr__(self):
        return f'Array: {self.value_list}'
