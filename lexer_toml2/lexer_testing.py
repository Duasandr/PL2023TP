import unittest
from lexer_toml import Lexer


class LexerTestCase(unittest.TestCase):

    def test_input_with_comment(self):
        data = '# this is a comment'
        lexer = Lexer()
        lexer.input(data)
        token = lexer.token()
        self.assertEqual('COMMENT', token.type)
        self.assertEqual(data, token.value)

    def test_input_with_key_value(self):
        data = 'key = "value"\n3.14 = "value"'
        lexer = Lexer()
        lexer.input(data)
        tokens = [lexer.token() for _ in range(13)]
        self.assertEqual('NUM', tokens[6].type)
        self.assertEqual('DOT', tokens[7].type)
        self.assertEqual('NUM', tokens[8].type)


if __name__ == '__main__':
    unittest.main()
