class KeyVal:
    """
    This class is used to represent a key-value pair in TOML.
    This class contains a list of keys and a value.
    Keys can be simple or dotted. Dotted keys are represented
    as a list of simple keys, that is why the key_list is a list.
    e.g.
        KeyVal(Key('string', "hello"), Value('integer', 1))
    """
    def __init__(self, key_list, value):
        self.key_list = key_list
        self.value = value

    def __repr__(self):
        return f'KeyVal: {self.key_list} = {self.value}'