import json

import ply.yacc as yacc
from lexer_toml import Lexer

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

class Parser():
    def __init__(self):
        self.tokens = Lexer.tokens
        self.lexer = Lexer()  # Create a lexer object using lex.lex()
        self.parser = yacc.yacc(module=self)

    def p_toml_empty(self, p):
        """toml : """
        p[0] = {}
        print("p_toml_empty")

    def p_toml_single(self, p):
        """toml : expression"""
        p[0] = p[1]
        print("p_toml_single: {}".format(p[0]))

    def p_toml_multiple(self, p):
        """toml : expression NEWLINE toml"""
        p[0] = {**p[1], **p[3]}  # Merge two dictionaries
        print("p_toml_multiple: {}".format(p[0]))

    def p_expression(self, p):
        """expression : key_val"""
        p[0] = p[1]
        print("p_expression: {}".format(p[0]))

    def p_key_val(self, p):
        """key_val : key EQUAL value"""
        if isinstance(p[1], tuple):
            p[0] = {p[1][0]: {p[1][1]: p[3]}}
        else:
            p[0] = {p[1]: p[3]}
        print("p_key_val: {}".format(p[0]))

    def p_key_simple(self, p):
        """key : simple_key"""
        p[0] = p[1]
        print("p_key_simple: {}".format(p[0]))

    def p_key_dotted(self, p):
        """key : dotted_key"""
        p[0] = p[1]
        print("p_key_dotted: {}".format(p[0]))

    def p_simple_key_unquoted(self, p):
        """simple_key : ID"""
        p[0] = p[1]
        print("p_simple_key_unquoted: {}".format(p[0]))

    def p_simple_key_quoted(self, p):
        """simple_key : STRING"""
        p[0] = p[1].replace('"', '')
        print("p_simple_key_quoted: {}".format(p[0]))

    def p_simple_key_number(self, p):
        """simple_key : NUM"""
        p[0] = p[1]
        print("p_simple_key_number: {}".format(p[0]))

    def p_dotted_key(self, p):
        """dotted_key : simple_key DOT simple_key"""
        p[0] = (p[1], p[3])
        print("p_dotted_key: {}".format(p[0]))

    def p_value_string(self, p):
        """value : STRING"""
        p[0] = p[1].replace('"', '')
        print("p_value_string: {}".format(p[0]))

    def p_value_number(self, p):
        """value : NUM"""
        p[0] = p[1]
        print("p_value_number: {}".format(p[0]))

    def p_error(self, p):
        print("Syntax error at token", p.type)

    def parse(self, data):
        self.lexer.input(data)
        rec = self.parser.parse(data)
        if rec:
            return json.dumps(rec, indent=4, ensure_ascii=False, )
        return None
