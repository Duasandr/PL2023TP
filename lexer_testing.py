import unittest
from lexer_toml import Lexer

# Test data
full_line_comment = '# This is a full-line comment'
inline_comment = 'key = "value"  # This is a comment at the end of a line'
comment_in_string = 'another = "# This is not a comment"'
valid_integers = "decimal = 123 123_456_789 hex = 0xDEADBEEF 0xdead_beef octal = 0o1234567 0O123_456_7 binary = " \
                 "0b1010101 0B1010_1010_1010_1010"
valid_floats = "float = 123.456 123_456.789 123.456_789 123_456.789_123 123e456 123e+456 123e-456 123.456e789 "
valid_offsets = "offset = 2019-01-01T00:00:00Z 2019-01-01T00:00:00+00:00 2019-01-01T00:00:00-00:00"
valid_local_date_time = "local_date = 2019-01-01T00:00:00"
valid_local_date = "local_date = 2019-01-01"
valid_local_time = "local_time = 00:00:00"
valid_string = 'string = \"127.0.0.1\"'
valid_multiline_string = 'string = """ value \n hello1 """'

# Expected results
inline_comment_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1,
    },
    {
        'type': 'EQUALS',
        'counter': 1,
    },
    {
        'type': 'STRING',
        'counter': 1,
    }
]

comment_in_string_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1,
    },
    {
        'type': 'EQUALS',
        'counter': 1,
    },
    {
        'type': 'STRING',
        'counter': 1,
    }
]

valid_integers_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 4
    },
    {
        'type': 'EQUALS',
        'counter': 4
    },
    {
        'type': 'INTEGER',
        'counter': 2
    },
    {
        'type': 'HEX_INTEGER',
        'counter': 2
    },
    {
        'type': 'OCT_INTEGER',
        'counter': 2
    },
    {
        'type': 'BIN_INTEGER',
        'counter': 2
    }
]

valid_floats_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1
    },
    {
        'type': 'EQUALS',
        'counter': 1
    },
    {
        'type': 'FLOAT',
        'counter': 8
    }
]

valid_offsets_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1
    },
    {
        'type': 'EQUALS',
        'counter': 1
    },
    {
        'type': 'OFFSET_DATE_TIME',
        'counter': 3
    }
]

valid_local_date_time_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1
    },
    {
        'type': 'EQUALS',
        'counter': 1
    },
    {
        'type': 'LOCAL_DATE_TIME',
        'counter': 1
    }
]

valid_local_date_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1
    },
    {
        'type': 'EQUALS',
        'counter': 1
    },
    {
        'type': 'LOCAL_DATE',
        'counter': 1
    }
]

valid_local_time_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1
    },
    {
        'type': 'EQUALS',
        'counter': 1
    },
    {
        'type': 'LOCAL_TIME',
        'counter': 1
    }
]

valid_string_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1
    },
    {
        'type': 'EQUALS',
        'counter': 1
    },
    {
        'type': 'STRING',
        'counter': 1
    }
]

valid_multiline_string_expected = [
    {
        'type': 'IDENTIFIER',
        'counter': 1
    },
    {
        'type': 'EQUALS',
        'counter': 1
    },
    {
        'type': 'MULTILINE_STRING',
        'counter': 1
    }
]

class LexerTestCase(unittest.TestCase):
    def test_full_line_comment(self):
        lexer = Lexer()
        lexer.input(full_line_comment)
        self.assertEqual(None, lexer.token())

    def test_inline_comment(self):
        lexer = Lexer()
        lexer.input(inline_comment)
        self.lexer_test(inline_comment_expected, lexer)

    def test_comment_in_string(self):
        lexer = Lexer()
        lexer.input(comment_in_string)
        self.lexer_test(comment_in_string_expected, lexer)

    def test_valid_integers(self):
        lexer = Lexer()
        lexer.input(valid_integers)
        self.lexer_test(valid_integers_expected, lexer)

    def test_valid_floats(self):
        lexer = Lexer()
        lexer.input(valid_floats)
        self.lexer_test(valid_floats_expected, lexer)

    def test_valid_offsets(self):
        lexer = Lexer()
        lexer.input(valid_offsets)
        self.lexer_test(valid_offsets_expected, lexer)

    def test_valid_local_date_time(self):
        lexer = Lexer()
        lexer.input(valid_local_date_time)
        self.lexer_test(valid_local_date_time_expected, lexer)

    def test_valid_local_date(self):
        lexer = Lexer()
        lexer.input(valid_local_date)
        self.lexer_test(valid_local_date_expected, lexer)

    def test_valid_local_time(self):
        lexer = Lexer()
        lexer.input(valid_local_time)
        self.lexer_test(valid_local_time_expected, lexer)

    def test_valid_string(self):
        lexer = Lexer()
        lexer.input(valid_string)
        self.lexer_test(valid_string_expected, lexer)

    def test_valid_multiline_string(self):
        lexer = Lexer()
        lexer.input(valid_multiline_string)
        self.lexer_test(valid_multiline_string_expected, lexer)

    def lexer_test(self, expected_results, lexer):
        """
        Test the tokens returned by the lexer.
        Example:
        expected_results = [ { 'type': 'ASSIGNMENT', 'counter': 1 } ]


        This means that the lexer should return 1 token of type ASSIGNMENT.
        :param expected_results: A list of dictionaries with the expected parameters
        :param lexer: The lexer object
        """
        token_count = {}

        for expected_token in expected_results:
            token_count[expected_token['type']] = 0

        token = lexer.token()
        while token:
            token_count[token.type] += 1
            print(token)
            token = lexer.token()

        for expected in expected_results:
            actual = {
                'type': expected['type'],
                'counter': token_count[expected['type']]
            }
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
