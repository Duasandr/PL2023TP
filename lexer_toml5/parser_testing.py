import unittest
from parser_toml import Parser

# Test data
full_line_comment = ' # This is a full-line comment 1'
invalid_char_comment = '# This is a full-line comment with an invalid char: \u0000'
inline_comment = '"key" = "value"  # This is a comment at the end of a line'
comment_in_string = 'another = "# This is not a comment1"'
valid_bare_key = '''

    bare_key.ke2 = "value1"
    bare-key = 1_234
    key7 = 0x12
    key8 = true
    1234 = "value"
    
'''
invalid_bare_key = """
汉语大字典 = "value1"
辭源 = "value1"
பெண்டிரேம் = "value1"
"""
valid_quoted_key = '''
"127.0.0.1" = """
    value1    
"""

"character encoding" = "value1"
'quoted "value"' = "value1"
"╠═╣" = "value1"
"⋰∫∬∭⋱" = "value1"
'''
valid_basic_string = '''
"key" = "value1"
key2 = "value2"
"3"."14159" = "pi"
3.14159 = "pi"
'''

invalid_basic_string = '''
"key" = "value\nhello1"
'''
valid_literal_string = '''
'key' = 'value \\n hello1'
'''
invalid_literal_string = '''
'key' = 'value \n hello1'
'''
valid_multiline_basic_string = '''
"key" = """value \\n hello1"""
'''
valid_integer = '''
"key" = 1234
"key" = +1234
"key" = -1234
'''
invalid_integer = '''
"key" = 1_234_
'''
valid_hex_integer = '''
"key" = 0xDEADBEEF
"key" = 0xdeadbeef
"key" = 0xdead_beef
'''
invalid_hex_integer = '''
"key" = 0xdead_beef_
'''
valid_oct_integer = '''
"key" = 0o01234567
"key" = 0o755
'''
invalid_oct_integer = '''
"key" = 0o755_
'''
valid_bin_integer = '''
"key" = 0b11010110
'''
invalid_bin_integer = '''
"key" = 0b11010110_
'''
valid_float = '''
"key" = 1.0
"key" = 1e10
"key" = 1e+10
"key" = 1e-10
"key" = 1E10
"key" = 1E+10
"key" = 1E-10
"key" = 1.0e10
"key" = 1.0e+10
'''
invalid_float = '''
"key" = 1.0e10_
'''
valid_bool = '''
"key" = true
"key" = false
'''
invalid_bool = '''
"key" = true_
'''
table_array = '''
# This is a TOML document.

title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00 # First class dates

[database]
server = "192.168.1.1"
ports = [ 8000, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]

  # Indentation (tabs and/or spaces) is allowed but not required
  [servers.alpha]
  ip = "10.0.0.1"
  dc = "eqdc10"

  [servers.beta]
  ip = "10.0.0.2"
  dc = "eqdc10"

[clients]
data = [ ["gamma", "delta"], [1, 2] ]

# Line breaks are OK when inside arrays
hosts = [ "alpha", "omega" ]
'''


class ParserTestCase(unittest.TestCase):

    def test_full_line_comment(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(full_line_comment))

    def test_comment_with_invalid_char(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_char_comment)

    def test_inline_comment(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(inline_comment))

    def test_comment_in_string(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(comment_in_string))

    def test_valid_bare_key(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_bare_key))

    def test_invalid_bare_key(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_bare_key)

    def test_valid_quoted_key(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_quoted_key))

    def test_valid_basic_string(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_basic_string))

    def test_invalid_basic_string(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_basic_string)

    def test_valid_literal_string(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_literal_string))

    def test_invalid_literal_string(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_literal_string)

    def test_valid_integer(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_integer))

    def test_invalid_integer(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_integer)

    '''def test_valid_hex_integer(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_hex_integer))

    def test_invalid_hex_integer(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_hex_integer)

    def test_valid_oct_integer(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_oct_integer))

    def test_invalid_oct_integer(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_oct_integer)

    def test_valid_bin_integer(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_bin_integer))

    def test_invalid_bin_integer(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_bin_integer)'''

    def test_valid_float(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_float))

    def test_invalid_float(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_float)

    def test_valid_bool(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(valid_bool))

    def test_invalid_bool(self):
        parser = Parser()
        with self.assertRaises(SyntaxError):
            parser.parse(invalid_bool)

    def test_table_array(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(table_array))


if __name__ == '__main__':
    unittest.main()
