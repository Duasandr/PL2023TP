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
                    | ASCII_DIGIT
                    | UNICODE_CHAR
                    | UNICODE_NUMBER
                    | UNICODE_PUNCTUATION
                    | COMMENT_START
                    | DASH
                    | UNDERSCORE
                    | WHITESPACE
                    | PLUS

    key_val : key ASSIGNMENT value

    key : simple_key
        | dotted_key

    simple_key : bare_key
                | quoted_key

    bare_key : bare_key_sequence

    bare_key_sequence : bare_key_char
                        | bare_key_char bare_key_sequence

    bare_key_char : ASCII_CHAR
                    | ASCII_DIGIT
                    | UNICODE_NUMBER
                    | DASH
                    | UNDERSCORE

    quoted_key : basic_string
                | literal_string

    dotted_key : simple_key DOT simple_key

    value : basic_string
            | literal_string
            | integer
            | float
            | boolean

    basic_string : BASIC_STR_QUOTE BASIC_STR_QUOTE
                    |   BASIC_STR_QUOTE basic_string_sequence BASIC_STR_QUOTE

    basic_string_sequence : basic_string_char
                            | basic_string_char basic_string_sequence

    basic_string_char : ASCII_CHAR
                        | ASCII_DIGIT
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
                        | PLUS
                        | escape


    literal_string : LITERAL_STR_QUOTE LITERAL_STR_QUOTE
                    | LITERAL_STR_QUOTE literal_string_sequence LITERAL_STR_QUOTE

    literal_string_sequence : literal_string_char
                            | literal_string_char literal_string_sequence

    literal_string_char : ASCII_CHAR
                        | ASCII_DIGIT
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
                        | REVERSE_SOLIDUS
                        | PLUS
                        | MINUS

    escape : REVERSE_SOLIDUS escape_char

    escape_char : LITERAL_STR_QUOTE
                | BASIC_STR_QUOTE
                | REVERSE_SOLIDUS
                | ASCII_CHAR

    integer : dec_int

    dec_int : dec_int_sequence
            | PLUS dec_int_sequence
            | DASH dec_int_sequence

    dec_int_sequence : dec_int_char
                    | dec_int_char dec_int_sequence

    dec_int_char : ASCII_DIGIT

    float : dec_float

    dec_float : integer DOT integer
                | integer DOT integer exponent
                | integer exponent

    exponent : ASCII_CHAR integer

    boolean : true
            | false

    true : ASCII_CHAR ASCII_CHAR ASCII_CHAR ASCII_CHAR
    false : ASCII_CHAR ASCII_CHAR ASCII_CHAR ASCII_CHAR ASCII_CHAR
                        """

    def p_toml(self, p):
        """
        toml : expression_list
        """
        p[0] = p[1]

    def p_expression_list_start_new_line(self, p):
        """
        expression_list : NEWLINE expression_list
        """
        p[0] = p[2]

    def p_expression_list_expression_new_line(self, p):
        """
        expression_list : expression NEWLINE expression_list
        """
        p[0] = p[1] + p[3]

    def p_expression_list_expression(self, p):
        """
        expression_list : expression
        """
        p[0] = p[1]

    def p_expression_comment(self, p):
        """
        expression : comment
        """
        p[0] = p[1]

    def p_expression_key_val(self, p):
        """
        expression : key_val
        """
        p[0] = p[1]

    def p_expression_key_val_comment(self, p):
        """
        expression : key_val comment
        """
        p[0] = p[1] + p[2]

    def p_comment(self, p):
        """
        comment : COMMENT_START comment_string
        """
        p[0] = p[2]

    def p_comment_string_stop(self, p):
        """
        comment_string : comment_char
        """
        p[0] = p[1]

    def p_comment_string(self, p):
        """
        comment_string : comment_char comment_string
        """
        p[0] = p[1] + p[2]

    def p_comment_char(self, p):
        """
        comment_char :  ASCII_CHAR
                        | ASCII_DIGIT
                        | UNICODE_CHAR
                        | UNICODE_NUMBER
                        | UNICODE_PUNCTUATION
                        | COMMENT_START
                        | DASH
                        | UNDERSCORE
                        | WHITESPACE
                        | PLUS
        """
        p[0] = p[1]

    def p_key_val(self, p):
        """
        key_val : key ASSIGNMENT value
        """
        p[0] = p[1] + p[2] + p[3]

    def p_key_simple(self, p):
        """
        key : simple_key
        """
        p[0] = p[1]

    def p_key_dotted(self, p):
        """
        key : dotted_key
        """
        p[0] = p[1]

    def p_simple_key_bare(self, p):
        """
        simple_key : bare_key
        """
        p[0] = p[1]

    def p_simple_key_quoted(self, p):
        """
        simple_key : quoted_key
        """
        p[0] = p[1]

    def p_bare_key(self, p):
        """
        bare_key : bare_key_sequence
        """
        p[0] = p[1]

    def p_bare_key_sequence_stop(self, p):
        """
        bare_key_sequence : bare_key_char
        """
        p[0] = p[1]

    def p_bare_key_sequence(self, p):
        """
        bare_key_sequence : bare_key_char bare_key_sequence
        """
        p[0] = p[1] + p[2]

    def p_bare_key_char(self, p):
        """
        bare_key_char : ASCII_CHAR
                        | ASCII_DIGIT
                        | UNICODE_CHAR
                        | UNICODE_NUMBER
                        | UNICODE_PUNCTUATION
                        | DASH
                        | UNDERSCORE
                        | WHITESPACE
                        | PLUS
        """
        p[0] = p[1]

    def p_quoted_key(self, p):
        """
        quoted_key : basic_string
                | literal_string
        """
        p[0] = p[1]


    def p_dotted_key(self, p):
        """
        dotted_key : simple_key DOT dotted_key
        """
        p[0] = p[1]


    def p_dotted_key_sequence(self, p):
        """
        dotted_key_sequence : dotted_key_char dotted_key_sequence
        """
        p[0] = p[1] + p[2]

    def p_dotted_key_char(self, p):
        """
        dotted_key_char : ASCII_CHAR
                        | ASCII_DIGIT
                        | UNICODE_CHAR
                        | UNICODE_NUMBER
                        | UNICODE_PUNCTUATION
                        | DASH
                        | UNDERSCORE
                        | WHITESPACE
                        | PLUS
                        | DOT
        """
        p[0] = p[1]

    def p_value(self, p):
        """
        value : string
                | boolean
                | integer
                | float
                | datetime
                | array
                | inline_table
        """
        p[0] = p[1]

    def p_string(self, p):
        """
        string : literal_string
                | basic_string
        """
        p[0] = p[1]

    def p_basic_literal_string_empty(self, p):
        """
        basic_literal_string : BASIC_LITERAL_STRING_QUOTE BASIC_LITERAL_STRING_QUOTE
        """
        p[0] = p[1] + p[2]

    def p_literal_string(self, p):
        """
        literal_string : LITERAL_STRING_QUOTE literal_string_sequence LITERAL_STRING_QUOTE
        """
        p[0] = p[1] + p[2] + p[3]

    def p_literal_string_sequence_stop(self, p):
        """
        literal_string_sequence : literal_string_char
        """
        p[0] = p[1]

    def p_literal_string_sequence(self, p):
        """
        literal_string_sequence : literal_string_char literal_string_sequence
        """
        p[0] = p[1] + p[2]

    def p_literal_string_char(self, p):
        """
        literal_string_char : ASCII_CHAR
                            | ASCII_DIGIT
                            | UNICODE_CHAR
                            | UNICODE_NUMBER
                            | UNICODE_PUNCTUATION
                            | DASH
                            | UNDERSCORE
                            | WHITESPACE
                            | PLUS
                            | DOT
                            | SLASH
                            | BACKSLASH
                            | COLON
                            | SEMICOLON
                            | COMMA
                            | EQUALS
                            | EXCLAMATION
                            | QUESTION
                            | AT
                            | HASH
                            | DOLLAR
                            | PERCENT
                            | CARET
                            | AMPERSAND
                            | ASTERISK
                            | LEFT_PAREN
                            | RIGHT_PAREN
                            | LEFT_BRACKET
                            | RIGHT_BRACKET
                            | LEFT_BRACE
                            | RIGHT_BRACE
                            | PIPE
                            | TILDE
                            | BACKTICK
                            | SINGLE_QUOTE
                            | DOUBLE_QUOTE
                            | NEWLINE
                            | TAB
                            | SPACE
        """
        p[0] = p[1]




    def p_error(self, p):
        if p:
            raise SyntaxError(f"Syntax error at line {p.lineno}, token={p.value}, character={p.lexpos}, type={p.type}")


    def parse(self, data):
        self.lexer.input(data)
        return self.parser.parse(data)
