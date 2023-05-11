class InlineTable:
    """
    InlineTable class
    Contains a list of expressions
    Example: InlineTable: [KeyVal(Key('string', "hello"), Value('integer', 1)), KeyVal(Key('string', "world"), Value('integer', 2))
    """
    def __init__(self, expression_list):
        self.expression_list = expression_list

    def __repr__(self):
        return f'InlineTable: {self.expression_list}'