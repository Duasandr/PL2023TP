class InlineTable:
    def __init__(self, expression_list):
        self.expression_list = expression_list

    def __repr__(self):
        return f'InlineTable: {self.expression_list}'