from ply import lex


class Lexer:
    # Tokens tuple declaration
    tokens = (
        'COMMENT',
        'STRING',
        'INT',
        'FLOAT',
        'BOOLEAN',
        'OFFSET_DATE_TIME',
        'DATE_TIME',
        'LOCAL_DATE',
        'LOCAL_TIME',
        'IDENTIFIER',
        'NEWLINE',
        'EQUAL',
        'VALUE',
        'DOT'
    )

    # Tokens regex declaration
    t_EQUAL = r'\='  # Equal sign (=)
    t_STRING = r'[\"|\'].*[\"|\']'  # String (any characters between quotation marks or apostrophes)
    t_IDENTIFIER = r'\w+'  # Identifier (any word)
    t_DOT = r'\.'  # Dot (.)
    t_ignore = ' \t'  # Ignore spaces and tabs

    """
    key: simple_key
        | dotted_key
        
    simple_key: STRING
            | IDENTIFIER
            
    dotted_key: simple_key DOT simple_key
    
    0.0 = "Hello"
       
    """
    def __init__(self):
        self.lexer = lex.lex(module=self)
    def t_OFFSET_DATE_TIME(self, t):
        r'\d{4}-\d{2}-\d{2}[T|t| ]\d{2}:\d{2}:\d{2}[Z|z][+|\-]\d{2}:\d{2}'
        # (yyyy-mm-ddThh:mm:ssZ|z(+|-)hh:mm)
        return t

    def t_DATE_TIME(self, t):
        r'\d{4}-\d{2}-\d{2}[T|t| ]\d{2}:\d{2}:\d{2}'
        # (yyyy-mm-ddThh:mm:ss)
        return t

    def t_LOCAL_DATE(self, t):
        r'\d{4}-\d{2}-\d{2}'
        # (yyyy-mm-dd)
        return t

    def t_LOCAL_TIME(self, t):
        r'\d{2}:\d{2}:\d{2}'
        # (hh:mm:ss)
        return t


    # Comment handling
    def t_COMMENT(self, t):
        r'\#.*'  # hash sign (#) followed by any character except newline
        t.lexer.skip(1)  # Skip the token to ignore comments

    def t_FLOAT(self, t):
        r'[\+|\-]?\d+\.\d+'  # Any number of digits, a dot (.), and any number of digits
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'[\+|\-]?\d+'  # Any number of digits preceded by a plus or minus sign (+ or -)
        t.value = int(t.value)
        return t

    def t_BOOLEAN(self, t):
        r'(true|false)'  # true or false
        if t.value == 'true':
            t.value = True
        else:
            t.value = False
        return t

    # Newline handling
    def t_NEWLINE(self, t):
        r"""[\n|\r]+"""
        t.lexer.lineno += len(t.value)
        t.lexer.skip(1)  # Skip the token to ignore newlines

    # Error handling
    def t_error(self, t):
        """Error handling rule for illegal characters"""
        print("Illegal character: {!r} ".format(t.value[0]))
        t.lexer.skip(1)

    def lexer(self):
        return self.lexer

    # Build the lexer
    def build(self, **kwargs):
        """
        Build the lexer
        :param kwargs: Additional arguments to pass to the lexer constructor
        """
        self.lexer = lex.lex(module=self, **kwargs)
