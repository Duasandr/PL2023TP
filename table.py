from key import Key

class Table:
    """
    A table is a list of keys and values.

    e.g. [key1, key2, ...] [key_val1, key_val1, ...]
    """
    def __init__(self, table_key_list: [Key]):
        self.key_list = table_key_list

    def __repr__(self):
        return f'Table: {self.key_list}'
