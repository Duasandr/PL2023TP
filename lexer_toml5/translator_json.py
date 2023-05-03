import re
from translator_tomml import TranslatorUnit


class JSONTranslator(TranslatorUnit):
    def __init__(self):
        super().__init__()

    def toml(self, toml):
        return "{" + toml

    def key_val(self, key, val):
        return key + ':' + val

    def simple_key(self, key):
        return key

    def quoted_key(self, key):
        return key

    def dotted_key(self, key, nested_key):
        return key + ':' + nested_key

    def dotted_key_2(self, key):
        if '.' in key:
            keys = key.split('.')
            return self.dotted_key("'" + keys[0] + "'", "'" + keys[1] + "'")
        else:
            return key

    def bare_key(self, key):
        return "'" + key + "'"

    def string(self, string):
        return string[1:-1]

    def integer(self, integer):
        return int(re.sub(r'_', r'', integer))

    def to_float(self, val):
        return float(re.sub(r'_', r'', val))

    def array(self, array):
        return array

    def expression_list(self, exp):
        return exp + '}'

    def expression_list_2(self, exp1, exp2):
        return exp1 + ',' + exp2
