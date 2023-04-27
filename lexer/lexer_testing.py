import unittest
from lexer import Lexer


class LexerTestCase(unittest.TestCase):
    def test_comment(self):
        data = """
                    # This is a comment.
                    # This is another comment.
               """
        lexer = Lexer()
        lexer.build()
        lexer.lexer.input(data)

        token = lexer.lexer.token()  # First comment

        self.assertEqual(token, None)

        token = lexer.lexer.token()  # Newline

        token = lexer.lexer.token()  # Second comment

        self.assertEqual(token, None)

        token = lexer.lexer.token()  # Newline

        self.assertEqual(2, lexer.lexer.lineno)

    def test_quotation_string(self):
        data = """
                    "This is a string."
                    'This is another string.'
                """
        lexer = Lexer()
        lexer.build()
        lexer.lexer.input(data)

        token = lexer.lexer.token()
        self.assertEqual(token.type, 'STRING')
        self.assertEqual(token.value, '"This is a string."')
        token = lexer.lexer.token()
        self.assertEqual(token.type, 'STRING')
        self.assertEqual(token.value, "'This is another string.'")

    def test_comment_string(self):
        data = """
                    # This is a comment.
                    "This is a string."
                    '# This is a string'
                    "# This is another string"
                    # This is another comment."
        """
        lexer = Lexer()
        lexer.build()
        lexer.lexer.input(data)

        while True:
            token = lexer.lexer.token()
            if not token:
                break
            self.assertEqual('STRING', token.type)

    def test_int_float(self):
        data = """
                    11-23-2018
                    2 2.5 3.0
                   "4.5 5.0 6.5"
                    # 7 8 9
        """
        lexer = Lexer()
        lexer.build()
        lexer.lexer.input(data)

        token = lexer.lexer.token()

        self.assertEqual('INT', token.type)
        self.assertEqual(11, token.value)

        token = lexer.lexer.token()

        self.assertEqual('INT', token.type)
        self.assertEqual(-23, token.value)

        token = lexer.lexer.token()

        self.assertEqual('INT', token.type)
        self.assertEqual(-2018, token.value)

        token = lexer.lexer.token()

        self.assertEqual('INT', token.type)
        self.assertEqual(2, token.value)

        token = lexer.lexer.token()

        self.assertEqual('FLOAT', token.type)
        self.assertEqual(2.5, token.value)

        token = lexer.lexer.token()

        self.assertEqual('FLOAT', token.type)
        self.assertEqual(3.0, token.value)

        token = lexer.lexer.token()

        self.assertEqual('STRING', token.type)
        self.assertEqual('"4.5 5.0 6.5"', token.value)

    def test_boolean(self):
        data = """
                    true false
                    "true false"
                    'true false'
                    # true false
        """
        lexer = Lexer()
        lexer.build()
        lexer.lexer.input(data)

        token = lexer.lexer.token()

        self.assertEqual('BOOLEAN', token.type)
        self.assertEqual(True, token.value)

        token = lexer.lexer.token()

        self.assertEqual('BOOLEAN', token.type)
        self.assertEqual(False, token.value)

        token = lexer.lexer.token()

        self.assertEqual('STRING', token.type)
        self.assertEqual('"true false"', token.value)

        token = lexer.lexer.token()

        self.assertEqual('STRING', token.type)
        self.assertEqual("'true false'", token.value)

    def test_local_date(self):
        data = """
                    2018-11-23 12:00:00z-05:00
                    2018-11-23 12:00:00z-05:00
                    2018-11-23T12:00:00z-05:00
                    2018-11-23t12:00:00Z+05:00
                    2018-11-23t12:00:00Z
                    2018-11-23 12:00:00
                    2018-11-23t12:00:00
                    2018-11-23T12:00:00
                    2018-11-23
                    12:00:00
                    """
        lexer = Lexer()
        lexer.build()
        lexer.lexer.input(data)

        tokens = []

        while True:
            token = lexer.lexer.token()
            if not token:
                break
            tokens.append(token)

        for i in range(0, 3):
            self.assertEqual('OFFSET_DATE_TIME', tokens[i].type)

        for i in range(6, 8):
            self.assertEqual('DATE_TIME', tokens[i].type)

        self.assertEqual('LOCAL_DATE', tokens[9].type)
        self.assertEqual('LOCAL_TIME', tokens[10].type)

    def test_key(self):
        data = """
                    key = value
                    key = "value"
                    key = 'value'
                    key = 1
                    key = 1.0
                    key = true
                    key = false
                    key = 2018-11-23
                    key = 12:00:00
                    key = 2018-11-23 12:00:00
                    key = 2018-11-23T12:00:00
                    key = 2018-11-23t12:00:00
                    key = 2018-11-23T12:00:00z-05:00
                    key = 2018-11-23t12:00:00z-05:00
                    key = 2018-11-23T12:00:00z
                    key = 2018-11-23t12:00:00z
                    key = "2018-11-23 12:00:00"
                    "key" = value
                    'key' = value
                    1 = value
                    1.0 = value
                    true = value
                    """
        lexer = Lexer()
        lexer.build()
        lexer.lexer.input(data)

        tokens = []

        while True:
            token = lexer.lexer.token()
            if not token:
                break
            print(token)
            tokens.append(token)


if __name__ == '__main__':
    unittest.main()
