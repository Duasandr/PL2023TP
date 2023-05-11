from value import Value


class Array:
    """
    Array class
    Contains a list of Values
    Example: Array: [Value('integer', 1), Value('integer', 2), Value('string', "hello")]
    """
    def __init__(self, value_list: [Value]):
        self.value_list = value_list

    def __repr__(self):
        return f'Array: {self.value_list}'
