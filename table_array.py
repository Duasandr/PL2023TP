from key import Key


class TableArray:
    def __init__(self, key_list: [Key]):
        self.key_list = key_list

    def __repr__(self):
        return f'TableArray: {self.key_list}'
