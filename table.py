from key import Key

class Table:
    """
    Table class
    Contains a list of keys
    Example: Table: [Key('string', "hello"), Key('string', "world")]
    """
    def __init__(self, table_key_list: [Key]):
        self.key_list = table_key_list

    def __repr__(self):
        return f'Table: {self.key_list}'
