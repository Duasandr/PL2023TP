import unittest
from parser_toml import Parser


class ParserTestCase(unittest.TestCase):

    def test_input_with_comment(self):
        data = '# this is a comment'
        parser = Parser()
        result = parser.parse(data)

    def test_input_with_key_value(self):
        data = 'key = "value"\n3.14 = "value"\n"another" = "value"'
        parser = Parser()
        result = parser.parse(data)
        print(result)


if __name__ == '__main__':
    unittest.main()
