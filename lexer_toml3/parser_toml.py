import json

import ply.yacc as yacc
from lexer_toml import Lexer

"""
Unspecified values are invalid.

key = # INVALID
There must be a newline (or EOF) after a key/value pair. (See Inline Table for exceptions.)

first = "Tom" last = "Preston-Werner" # INVALID
"""

"""
Keys

A key may be either bare, quoted, or dotted.

Bare keys may contain any letter-like or number-like Unicode character from any 
Unicode script, as well as ASCII digits, dashes and underscores. 
Punctuation, spaces, arrows, box drawing and private use characters are not allowed. 
Note that bare keys are allowed to be composed of only ASCII digits, e.g. 1234, but are always interpreted as strings.
"""

"""
    toml : 
         | expression
         | expression NEWLINE toml

    expression : key_val

    key_val : key EQUAL value
    
    key : simple_key
        | dotted_key

    simple_key :  ID
               | STRING
               | NUM
        
    dotted_key : simple_key DOT simple_key

    value :   STRING
            | NUM
"""

"""
    toml : expression
    
    expression : comment
                | key_val
                | key_val comment
    
    comment : COMMENT_START comment_string
            | COMMENT_START comment_string NEWLINE
    
    comment_string : comment_char
                        | comment_char comment_string
    
    comment_char : UNICODE_CHAR
                    | UNICODE_NUMBER
                    | UNICODE_PUNCTUATION
                    | COMMENT_START
                    | DASH
                    | UNDERSCORE
                    
    key_val : key ASSIGNMENT value
    
    key : simple_key
        | dotted_key
        
    simple_key : bare_key
                | quoted_key
                
    bare_key : bare_key_sequence
    
    bare_key_sequence : bare_key_char
                        | bare_key_char bare_key_sequence
                        
    bare_key_char : UNICODE_CHAR
                    | UNICODE_NUMBER
                    | DASH
                    | UNDERSCORE
                    
    quoted_key : basic_string
    
    dotted_key : simple_key DOT simple_key
                    
    value : basic_string
    
    basic_string : BASIC_STR_QUOTE BASIC_STR_QUOTE
                    |   BASIC_STR_QUOTE basic_string_sequence BASIC_STR_QUOTE
                    
    basic_string_sequence : basic_string_char
                            | basic_string_char basic_string_sequence
                            
    basic_string_char : UNICODE_CHAR
                        | UNICODE_NUMBER
                        | UNICODE_PUNCTUATION
                        | UNICODE_CONTROL
                        | UNICODE_SYMBOL
                        | UNICODE_SEPARATOR
                        | DASH
                        | UNDERSCORE
                        | WHITESPACE
                        | NEWLINE

                    
"""


class Parser:
    def __init__(self):
        self.tokens = Lexer.tokens
        self.lexer = Lexer()  # Create a lexer object using lex.lex()
        self.parser = yacc.yacc(module=self)

    # Parsing rules
    def p_grammar(self, p):
        """
    toml : expression_list

    expression_list : NEWLINE expression_list
                | expression NEWLINE expression_list
                | expression

    expression : comment
                | key_val
                | key_val comment

    comment : COMMENT_START comment_string

    comment_string : comment_char
                        | comment_char comment_string

    comment_char :  ASCII_CHAR
                    | UNICODE_CHAR
                    | UNICODE_NUMBER
                    | UNICODE_PUNCTUATION
                    | COMMENT_START
                    | DASH
                    | UNDERSCORE
                    | WHITESPACE

    key_val : key ASSIGNMENT value

    key : simple_key
        | dotted_key

    simple_key : bare_key
                | quoted_key

    bare_key : bare_key_sequence

    bare_key_sequence : bare_key_char
                        | bare_key_char bare_key_sequence

    bare_key_char : ASCII_CHAR
                    | UNICODE_NUMBER
                    | DASH
                    | UNDERSCORE

    quoted_key : basic_string
                | literal_string

    dotted_key : simple_key DOT simple_key

    value : basic_string
            | literal_string

    basic_string : BASIC_STR_QUOTE BASIC_STR_QUOTE
                    |   BASIC_STR_QUOTE basic_string_sequence BASIC_STR_QUOTE

    basic_string_sequence : basic_string_char
                            | basic_string_char basic_string_sequence

    basic_string_char : ASCII_CHAR
                        | UNICODE_CHAR
                        | UNICODE_NUMBER
                        | UNICODE_PUNCTUATION
                        | UNICODE_CONTROL
                        | UNICODE_SYMBOL
                        | UNICODE_SEPARATOR
                        | UNICODE_PRIVATE_USE
                        | LITERAL_STR_QUOTE
                        | DASH
                        | UNDERSCORE
                        | WHITESPACE
                        | DOT
                        | COMMENT_START

    literal_string : LITERAL_STR_QUOTE LITERAL_STR_QUOTE
                    | LITERAL_STR_QUOTE literal_string_sequence LITERAL_STR_QUOTE

    literal_string_sequence : literal_string_char
                            | literal_string_char literal_string_sequence

    literal_string_char : ASCII_CHAR
                        | UNICODE_CHAR
                        | UNICODE_NUMBER
                        | UNICODE_PUNCTUATION
                        | UNICODE_CONTROL
                        | UNICODE_SYMBOL
                        | UNICODE_SEPARATOR
                        | UNICODE_PRIVATE_USE
                        | BASIC_STR_QUOTE
                        | DASH
                        | UNDERSCORE
                        | WHITESPACE
                        | DOT
                        | COMMENT_START
                        | NEWLINE
                        """

    def p_error(self, p):
        if p:
            raise SyntaxError(f"Syntax error at line {p.lineno}, token={p.value}, character={p.lexpos}, type={p.type}")


    def parse(self, data):
        self.lexer.input(data)
        return self.parser.parse(data)
