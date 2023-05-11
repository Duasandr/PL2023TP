from value import Value

class Key:
    """
    Key class
    Contains a type and a value
    Example: Key: type:bare_key value:Value('string', "hello")
    """
    def __init__(self, type_, value: Value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Key: {self.type}: {self.value}'