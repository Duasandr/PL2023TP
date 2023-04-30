# lexer_toml.py - Lexer for the TOMML language

import ply.lex as lex

# Tokens
tokens = (
    'BOOLEAN',
    'COMMA',
    'DATE',
    'DATETIME',
    'EQUAL',
    'FLOAT',
    'INTEGER',
    'LEFT_BRACKET',
    'LEFT_BRACE',
    'NEWLINE',
    'RIGHT_BRACKET',
    'RIGHT_BRACE',
    'STRING',
    'TIME',
    'WHITESPACE',
    'COMMENT',
    'IDENTIFIER',
    'DOT'
)


# Tokens
t_WHITESPACE = r'[ \t]+'
t_BOOLEAN = r'(true|false)'
t_COMMA = r','
t_DATE = r'\d{4}-\d{2}-\d{2}'
t_DATETIME = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})?'
t_EQUAL = r'='
t_FLOAT = r'[-+]?(\d*\.\d+|\d+\.\d*)([eE][-+]?\d+)?'
t_INTEGER = r'[-+]?\d+'
t_LEFT_BRACKET = r'\['
t_LEFT_BRACE = r'{'
t_RIGHT_BRACKET = r'\]'
t_RIGHT_BRACE = r'}'
t_STRING = r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\''
t_TIME = r'\d{2}:\d{2}:\d{2}(\.\d+)?'
t_COMMENT = r'\#.*'
t_IDENTIFIER = r'\w+'
t_DOT = r'\.'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1

# Error handling
def t_error(t):
    raise ValueError("Illegal character " + t.value[0])

# Build the lexer

lexer = lex.lex()

data = '''
# This is a TOML document.

title = "TOML Example"

name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00 # First class dates

'''
