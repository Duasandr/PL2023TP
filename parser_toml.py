import ply.yacc as yacc
from lexer_toml import Lexer
from array import Array
from inline_table import InlineTable
from key import Key
from key_val import KeyVal
from table import Table
from value import Value
from table_array import TableArray
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
        p[0] = p[1]

    def p_expression_list(self, p):
        """expression_list : expression"""
        p[0] = [p[1]]

    def p_expression_list_2(self, p):
        """expression_list : expression expression_list"""
        p[0] = [p[1]] + p[2]

    def p_expression(self, p):
        """expression : key_val
                    | table
                    | inline_table
                    | table_array"""
        p[0] = p[1]

    def p_key_val(self, p):
        """key_val : key EQUALS value"""
        p[0] = KeyVal(p[1], p[3])

    def p_key(self, p):
        """key : simple_key"""
        p[0] = [p[1]]

    def p_key_2(self, p):
        """key : dotted_key"""
        p[0] = p[1]

    def p_simple_key(self, p):
        """simple_key : quoted_key"""
        p[0] = Key('quoted_key', p[1])

    def p_simple_key_2(self, p):
        """simple_key : bare_key"""
        p[0] = Key('bare_key', p[1])

    def p_quoted_key(self, p):
        """quoted_key : STRING
                        | LITERAL_STRING"""
        p[0] = Value('string', p[1][1:-1])

    def p_bare_key(self, p):
        """bare_key : IDENTIFIER"""
        p[0] = Value('string', p[1])

    def p_bare_key_2(self, p):
        """bare_key : INTEGER"""
        p[0] = Value('integer', p[1])

    def p_dotted_key(self, p):
        """dotted_key : simple_key DOT key"""
        p[0] = [p[1]] + p[3]

    def p_dotted_key_2(self, p):
        """dotted_key : FLOAT"""
        keys = p[1].split('.')
        p[0] = [Key('bare_key', Value('integer', key)) for key in keys]

    def p_value(self, p):
        """value : STRING
                | LITERAL_STRING"""
        p[0] = Value('string', p[1][1:-1])

    def p_value_2(self, p):
        """value : MULTILINE_STRING
                | LITERAL_MULTILINE_STRING"""
        p[0] = Value('ml_string', p[1][3:-3])

    def p_value_3(self, p):
        """value : BOOLEAN"""
        p[0] = Value("boolean", p[1])

    def p_value_4(self, p):
        """value : OFFSET_DATE_TIME
                | LOCAL_DATE_TIME
                | LOCAL_DATE
                | LOCAL_TIME"""
        p[0] = Value("datetime", p[1])

    def p_value_5(self, p):
        """value : INTEGER
                | HEX_INTEGER
                | OCT_INTEGER
                | BIN_INTEGER"""
        p[0] = Value("integer", p[1])

    def p_value_6(self, p):
        """value : array"""
        p[0] = Value("array", p[1])

    def p_value_7(self, p):
        """value : FLOAT"""
        p[0] = Value("float", p[1])

    def p_value_8(self, p):
        """value : inline_table"""
        p[0] = Value("inline_table", p[1])

    def p_array(self, p):
        """array : LBRACKET value_list RBRACKET"""
        p[0] = Array(p[2])

    def p_value_list(self, p):
        """value_list : value"""
        p[0] = [p[1]]

    def p_value_list_2(self, p):
        """value_list : value COMMA value_list"""
        p[0] = [p[1]] + p[3]

    def p_table(self, p):
        """table : LBRACKET key RBRACKET"""
        p[0] = Table(p[2])

    def p_inline_list(self, p):
        """inline_list : expression"""
        p[0] = [p[1]]

    def p_inline_list_2(self, p):
        """inline_list : expression COMMA inline_list"""
        p[0] = [p[1]] + p[3]

    def p_inline_table(self, p):
        """inline_table : LBRACE inline_list RBRACE"""
        p[0] = InlineTable(p[2])

    def p_table_array(self, p):
        """table_array : LBRACKET LBRACKET key RBRACKET RBRACKET"""
        p[0] = TableArray(p[3])

    def p_error(self, p):
        if p:
            raise SyntaxError(f"Syntax error at line {p.lineno}, token={p.value}, character={p.lexpos}, type={p.type}")

    def parse(self, data):
        self.lexer.input(data)
        node = self.parser.parse(data)
        self.translation_unit.translate(node)
        return self.translation_unit.get_result()
