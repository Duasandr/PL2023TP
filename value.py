class Value:
    """
    Value class
    Contains a type and a value
    Example: Value: type:integer value:1
    """
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Value: {self.type}: {self.value}'
