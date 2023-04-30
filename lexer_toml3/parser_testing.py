import unittest
from parser_toml import Parser

# Test data
full_line_comment = ' # This is a full-line comment'
invalid_char_comment = '# This is a full-line comment with an invalid char: \u0000'
inline_comment = '"key" = "value"  # This is a comment at the end of a line'
comment_in_string = 'another = "# This is not a comment"'
valid_bare_key = '''

    bare_key = "value"
    bare-key = "value"
    1234 = "value"
    
'''
invalid_bare_key = """
汉语大字典 = "value"
辭源 = "value"
பெண்டிரேம் = "value"
"""
valid_quoted_key = '''
"127.0.0.1" = "value"
"character encoding" = "value"
'quoted "value"' = "value"
"╠═╣" = "value"
"⋰∫∬∭⋱" = "value"
'''


class ParserTestCase(unittest.TestCase):

    def test_full_line_comment(self):
        parser = Parser()
        self.assertEqual(None, parser.parse(full_line_comment))

    def test_comment_with_invalid_char(self):
        parser = Parser()
        parser.parse(invalid_char_comment)
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


if __name__ == '__main__':
    unittest.main()
