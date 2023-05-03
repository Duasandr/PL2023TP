import json

import ply.yacc as yacc
from lexer_toml import Lexer
from translator_json import JSONTranslator


class Parser:
    def __init__(self, lang='JSON'):
        self.tokens = Lexer.tokens
        self.lexer = Lexer()  # Create a lexer object using lex.lex()
        self.parser = yacc.yacc(module=self)

        if lang == 'JSON':
            self.translation_unit = JSONTranslator()

    # Parsing rules

    def p_toml(self, p):
        """toml : expression_list"""
        p[0] = self.translation_unit.toml(p[1])

    def p_expression_list(self, p):
        """expression_list : expression"""
        p[0] = self.translation_unit.expression_list(p[1])

    def p_expression_list_2(self, p):
        """expression_list : expression expression_list"""
        p[0] = self.translation_unit.expression_list_2(p[1], p[2])

    def p_expression(self, p):
        """expression : key_val"""
        p[0] = p[1]

    def p_expression_2(self, p):
        """expression : table"""
        p[0] = p[1]

    def p_key_val(self, p):
        """key_val : key EQUALS value"""
        p[0] = self.translation_unit.key_val(p[1], p[3])

    def p_key(self, p):
        """key : simple_key"""
        p[0] = p[1]

    def p_key_2(self, p):
        """key : dotted_key"""
        p[0] = p[1]

    def p_simple_key(self, p):
        """simple_key : bare_key"""
        p[0] = p[1]

    def p_simple_key_2(self, p):
        """simple_key : quoted_key"""
        p[0] = p[1]

    def p_bare_key(self, p):
        """bare_key : IDENTIFIER
                    | INTEGER"""
        p[0] = self.translation_unit.bare_key(p[1])

    def p_quoted_key(self, p):
        """quoted_key : STRING
                    | LITERAL_STRING"""
        p[0] = self.translation_unit.quoted_key(p[1])

    def p_dotted_key(self, p):
        """dotted_key : simple_key DOT simple_key"""
        p[0] = self.translation_unit.dotted_key(p[1], p[3])

    def p_dotted_key_2(self, p):
        """dotted_key : FLOAT"""
        p[0] = self.translation_unit.dotted_key_2(p[1])

    def p_value_string(self, p):
        """value : STRING"""
        p[0] = self.translation_unit.string(p[1])
    def p_value_literal_string(self, p):
        """value : LITERAL_STRING"""
        p[0] = self.translation_unit.literal_string(p[1])

    def p_value_integer(self, p):
        """value : INTEGER"""
        p[0] = self.translation_unit.integer(p[1])

    def p_value_float(self, p):
        """value : FLOAT"""
        p[0] = self.translation_unit.to_float(p[1])

    def p_value_rest(self, p):
        """value : HEX_INTEGER
                | OCT_INTEGER
                | BIN_INTEGER
                | BOOLEAN
                | OFFSET_DATE_TIME
                | LOCAL_DATE_TIME
                | LOCAL_DATE
                | LOCAL_TIME
                | MULTILINE_STRING
                | LITERAL_MULTILINE_STRING
                | array
                | inline_table"""
        p[0] = p[1]

    def p_array(self, p):
        """array : LBRACKET value_list RBRACKET"""
        p[0] = p[1] + p[2] + p[3]
        # p[0] = self.translation_unit.translate('array', p)

    def p_value_list(self, p):
        """value_list : value"""
        p[0] = p[1]

    def p_value_list_2(self, p):
        """value_list : value COMMA value_list"""
        p[0] = p[1] + p[2] + p[3]

    def p_inline_table(self, p):
        """inline_table : LBRACE key_val_list RBRACE"""
        p[0] = p[1] + p[2] + p[3]

    def p_key_val_list(self, p):
        """key_val_list : key_val"""
        p[0] = p[1]

    def p_key_val_list_2(self, p):
        """key_val_list : key_val COMMA key_val_list"""
        p[0] = p[1] + p[2] + p[3]

    def p_table(self, p):
        """table : LBRACKET key RBRACKET"""
        p[0] = p[1] + p[2] + p[3]
        # self.translation_unit.translate('table', p)

    def p_error(self, p):
        if p:
            raise SyntaxError(f"Syntax error at line {p.lineno}, token={p.value}, character={p.lexpos}, type={p.type}")

    def parse(self, data):
        self.lexer.input(data)
        return self.parser.parse(data)
