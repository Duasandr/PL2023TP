from key import Key


class TableArray:
    """
    TableArray class
    Contains a list of keys
    Example: TableArray: [Key('string', "hello"), Key('string', "world")]
    """
    def __init__(self, key_list: [Key]):
        self.key_list = key_list

    def __repr__(self):
        return f'TableArray: {self.key_list}'
