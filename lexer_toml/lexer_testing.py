import unittest
from lexer import Lexer


class LexerTestCase(unittest.TestCase):

    def test_input(self):
        data = 'a = 1'
        lexer = Lexer()
        lexer.input(data)
        for token in lexer.lexer:
            print(token)


if __name__ == '__main__':
    unittest.main()
