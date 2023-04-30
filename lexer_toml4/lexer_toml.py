import ply.lex as lex
import unicodedata

"""
Lexer for TOML files
"""

"""
Preliminaries

TOML is case-sensitive.

Whitespace means tab (U+0009) or space (U+0020).

Newline means LF (U+000A) or CRLF (U+000D U+000A).

A TOML file must be a valid UTF-8 encoded Unicode document.

Specifically this means that a file as a whole must form a well-formed code-unit sequence. 
Otherwise, it must be rejected (preferably) or have ill-formed byte sequences replaced with U+FFFD, 
as per the Unicode specification.
"""


class Lexer:
    # Tokens tuple declaration
    tokens = (
        'ASCII_CHAR',
        'ASCII_DIGIT',
        'UNICODE_CHAR',
        'UNICODE_NUMBER',
        'UNICODE_PUNCTUATION',
        'UNICODE_CONTROL',
        'UNICODE_SYMBOL',
        'UNICODE_SEPARATOR',
        'UNICODE_PRIVATE_USE',
        'COMMENT_START',
        'ASSIGNMENT',
        'BASIC_STR_QUOTE',
        'LITERAL_STR_QUOTE',
        'NEWLINE',
        'WHITESPACE',
        'DASH',
        'UNDERSCORE',
        'DOT',
        'REVERSE_SOLIDUS',
        'PLUS',
        'MINUS',
    )
    t_ignore = ' \t'

    def __init__(self):
        self.lex = lex.lex(module=self)

    # Token rules

    def t_PLUS(self, t):
        r'\+'
        return t

    def t_REVERSE_SOLIDUS(self, t):
        r'\\'
        return t

    def t_DOT(self, t):
        r'\.'
        return t

    def t_UNDERSCORE(self, t):
        r'_'
        return t

    def t_DASH(self, t):
        r'-'
        return t

    def t_NEWLINE(self, t):
        r'[\n\r]+'
        return t

    def t_WHITESPACE(self, t):
        r'[ \t]'
        return t

    def t_BASIC_STR_QUOTE(self, t):
        r'\"'
        return t

    def t_LITERAL_STR_QUOTE(self, t):
        r'\''
        return t

    def t_ASSIGNMENT(self, t):
        r'\='
        return t

    def t_COMMENT_START(self, t):
        r'\#'
        return t

    # Unicode's character handling
    def t_UNICODE_CHAR(self, t):
        r'.'
        if unicodedata.category(t.value).startswith('N') and ord(t.value) < 128:
            t.type = 'ASCII_DIGIT'
            return t
        if unicodedata.category(t.value).startswith('N'):
            t.type = 'UNICODE_NUMBER'
            return t
        if unicodedata.category(t.value).startswith("L") and ord(t.value) < 128:
            t.type = 'ASCII_CHAR'
            return t
        # If the character is a valid Unicode letter
        if unicodedata.category(t.value).startswith('L'):
            t.type = 'UNICODE_CHAR'
            return t
        # If the character is a valid Unicode punctuation
        if unicodedata.category(t.value).startswith('P'):
            t.type = 'UNICODE_PUNCTUATION'
            return t
        # If the character is a valid Unicode control character
        if unicodedata.category(t.value).startswith('Cc'):
            t.type = 'UNICODE_CONTROL'
            return t
        # If the character is a valid Unicode symbol
        if unicodedata.category(t.value).startswith('S'):
            t.type = 'UNICODE_SYMBOL'
            return t
        # If the character is a valid Unicode separator
        if unicodedata.category(t.value).startswith('Z'):
            t.type = 'UNICODE_SEPARATOR'
            return t
        # If the character is a valid Unicode private use
        if unicodedata.category(t.value).startswith('Co'):
            t.type = 'UNICODE_PRIVATE_USE'
            return t

        # If the character is not a valid Unicode letter, report an error
        self.t_error(t)

    # Error handling
    def t_error(self, t):
        """Error handling rule for illegal characters"""
        if unicodedata.category(t.value).startswith('L'):
            print("Invalid character: {!r}".format(t.value[0]))
            return
        if unicodedata.category(t.value).startswith('N'):
            print("Invalid number: {!r}".format(t.value[0]))
            return
        if unicodedata.category(t.value).startswith('P'):
            print("Invalid punctuation: {!r}".format(t.value[0]))
            return

        raise ValueError("Non-Unicode character: {!r}".format(t.value[0]))


    def token(self):
        return self.lex.token()

    def input(self, data):
        self.lex.input(data)
