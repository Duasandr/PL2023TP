import ply.lex as lex
import unicodedata


class Lexer:
    # Tokens tuple declaration
    tokens = (
        'STRING',
        'LITERAL_STRING',
        'MULTILINE_STRING',
        'LITERAL_MULTILINE_STRING',
        'INTEGER',
        'HEX_INTEGER',
        'OCT_INTEGER',
        'BIN_INTEGER',
        'FLOAT',
        'BOOLEAN',
        'OFFSET_DATE_TIME',
        'LOCAL_DATE_TIME',
        'LOCAL_DATE',
        'LOCAL_TIME',
        'COMMENT',
        'EQUALS',
        'COMMA',
        'LBRACKET',
        'RBRACKET',
        'LBRACE',
        'RBRACE',
        'DOT',
        'NEWLINE',
        'IDENTIFIER'
    )
    t_ignore = ' \t'

    # Tokens regex declaration

    def t_NEWLINE(self, t):
        r'[\n\r]+'
        t.lexer.lineno += len(t.value)

    def t_MULTILINE_STRING(self, t):
        r'\"\"\"[^\"]*\"\"\"'
        return t

    def t_LITERAL_MULTILINE_STRING(self, t):
        r'\'\'\'[^\']*\'\'\''
        return t

    # Tokens regex declaration
    def t_STRING(self, t):
        r'"[^\"\n\r]*"'
        return t

    def t_DOT(self, t):
        r'\.'
        return t

    def t_EQUALS(self, t):
        r'='
        return t

    def t_COMMA(self, t):
        r','
        return t

    def t_LBRACKET(self, t):
        r'\['
        return t

    def t_RBRACKET(self, t):
        r'\]'
        return t

    def t_LBRACE(self, t):
        r'\{'
        return t

    def t_RBRACE(self, t):
        r'\}'
        return t

    def t_COMMENT(self, t):
        r'\#.*'
        t.lexer.skip(1)


    def t_LITERAL_STRING(self, t):
        r'\'[^\'\n\r]*\''
        return t

    def t_OFFSET_DATE_TIME(self, t):
        # This one is just LOCAL_DATE_TIME with an optional offset
        r'\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2}([zZ]|[+-]\d{2}:\d{2})'
        return t

    def t_LOCAL_DATE_TIME(self, t):
        # e.g. 2019-09-24T23:04:20
        r'\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2}'
        return t

    def t_LOCAL_DATE(self, t):
        # e.g. 2019-09-24
        r'\d{4}-\d{2}-\d{2}'
        return t

    def t_LOCAL_TIME(self, t):
        # e.g. 23:04:20
        r'\d{2}:\d{2}:\d{2}'
        return t

    def t_FLOAT(self, t):
        # This regex is a bit more complex than the others, but it is
        # basically the same as the INTEGER regex but with a decimal
        # point and an optional exponent part which is just an e or E
        # followed by an INTEGER
        r'([+-]?\d(\d|_(?=\d))*\.(\d|_(?=\d))*([eE][+-]?\d(\d|_(?=\d))*)?)|([+-]?\d(\d|_(?=\d))*[eE][+-]?\d(\d|_(?=\d))*)'
        return t

    def t_HEX_INTEGER(self, t):
        # 0x or 0X is the prefix for hexadecimal numbers
        # and the number can have underscores between digits
        r'0[xX][\da-fA-F]([\da-fA-F]|_(?=[\da-fA-F]))*'
        return t

    def t_OCT_INTEGER(self, t):
        # 0o or 0O is the prefix for octal numbers
        # and the number can have underscores between digits
        r'0[oO][0-7]([0-7]|_(?=[0-7]))*'
        return t

    def t_BIN_INTEGER(self, t):
        # 0b or 0B is the prefix for binary numbers
        # and the number can have underscores between digits
        r'0[bB][01]([01]|_(?=[01]))*'
        return t

    def t_INTEGER(self, t):
        # + or - sign is optional in front of the number
        # and the number can have underscores between digits
        r'[+-]?\d(\d|_(?=\d))*'
        return t

    def t_BOOLEAN(self, t):
        r'(true|false)'
        return t

    def t_IDENTIFIER(self, t):
        r'\b[\w-]+\b'
        return t

    def __init__(self):
        self.lex = lex.lex(module=self)

    # Token rules

    # Error handling
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def token(self):
        return self.lex.token()

    def input(self, data):
        self.lex.input(data)
