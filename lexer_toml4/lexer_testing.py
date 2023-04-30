import unittest
from lexer_toml import Lexer

# Test data
full_line_comment = '# This is a full-line comment'
inline_comment = 'key = "value"  # This is a comment at the end of a line'
comment_in_string = 'another = "# This is not a comment"'

# Expected results
full_line_comment_expected = [
    {
        'type': 'COMMENT_START',
        'counter': 1
    },
    {
        'type': 'UNICODE_CHAR',
        'counter': 22
    },
    {
        'type': 'WHITESPACE',
        'counter': 5
    },
    {
        'type': 'DASH',
        'counter': 1
    }
]

inline_comment_expected = [
    {
        'type': 'ASSIGNMENT',
        'counter': 1
    },
    {
        'type': 'UNICODE_CHAR',
        'counter': 37
    },
    {
        'type': 'COMMENT_START',
        'counter': 1
    },
    {
        'type': 'BASIC_STR_QUOTE',
        'counter': 2
    },
    {
        'type': 'WHITESPACE',
        'counter': 14
    }
]

comment_in_string_expected = [
    {
        'type': 'COMMENT_START',
        'counter': 1
    },
    {
        'type': 'UNICODE_CHAR',
        'counter': 24
    },
    {
        'type': 'ASSIGNMENT',
        'counter': 1
    },
    {
        'type': 'BASIC_STR_QUOTE',
        'counter': 2
    },
    {
        'type': 'WHITESPACE',
        'counter': 7
    }
]


class LexerTestCase(unittest.TestCase):
    def test_full_line_comment(self):
        lexer = Lexer()
        lexer.input(full_line_comment)
        self.lexer_test(full_line_comment_expected, lexer)

    def test_inline_comment(self):
        lexer = Lexer()
        lexer.input(inline_comment)
        self.lexer_test(inline_comment_expected, lexer)

    def test_comment_in_string(self):
        lexer = Lexer()
        lexer.input(comment_in_string)
        self.lexer_test(comment_in_string_expected, lexer)

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
            token = lexer.token()

        for expected in expected_results:
            actual = {
                'type': expected['type'],
                'counter': token_count[expected['type']]
            }
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
