import unittest
from parser_toml import Parser

# Test data
toml_with_comments = '''
# This is a full-line comment
key = "value"  # This is a comment at the end of a line
another = "# This is not a comment"
'''
json_with_comments_expected = '''{
    "key": "value",
    "another": "# This is not a comment"
}'''

toml_invalid_key_val = 'key = # INVALID'

toml_bare_keys = '''key = "value"
bare_key = "value"
bare-key = "value"
1234 = "value"'''
json_bare_keys_expected = '''{
    "key": "value",
    "bare_key": "value",
    "bare-key": "value",
    "1234": "value"
}'''

toml_quoted_keys = '''"127.0.0.1" = "value"
"character encoding" = "value"
"ʎǝʞ" = "value"
'key2' = "value"
'quoted "value"' = "value"
"" = "blank"     # VALID but discouraged
'' = 'blank'     # VALID but discouraged'''
json_quoted_keys_expected = '''{
    "127.0.0.1": "value",
    "character encoding": "value",
    "ʎǝʞ": "value",
    "key2": "value",
    "quoted \\"value\\"": "value",
    "": "blank"
}'''

toml_invalid_quoted_key = '= "no key name"  # INVALID'

toml_dot_keys = '''name = "Orange"
physical.color = "orange"
physical.shape = "round"
site."google.com" = true
3.14159 = "pi"'''
json_dot_keys_expected = '''{
    "name": "Orange",
    "physical": {
        "color": "orange",
        "shape": "round"
    },
    "site": {
        "google.com": true
    },
    "3": {
        "14159": "pi"
    }
}'''

toml_integers = '''int1 = +99
int2 = 42
int3 = 0
int4 = -17
int5 = 1_000
int6 = 5_349_221
int7 = 53_49_221  # Indian number system grouping
int8 = 1_2_3_4_5
# hexadecimal with prefix `0x`
hex1 = 0xDEADBEEF
hex2 = 0xdeadbeef
hex3 = 0xdead_beef

# octal with prefix `0o`
oct1 = 0o01234567
oct2 = 0o755 # useful for Unix file permissions

# binary with prefix `0b`
bin1 = 0b11010110'''
json_integers_expected = '''{
    "int1": 99,
    "int2": 42,
    "int3": 0,
    "int4": -17,
    "int5": 1000,
    "int6": 5349221,
    "int7": 5349221,
    "int8": 12345,
    "hex1": 3735928559,
    "hex2": 3735928559,
    "hex3": 3735928559,
    "oct1": 342391,
    "oct2": 493,
    "bin1": 214
}'''

toml_floats = '''# fractional
flt1 = +1.0
flt2 = 3.1415
flt3 = -0.01

# exponent
flt4 = 5e+22
flt5 = 1e06
flt6 = -2E-2

# both
flt7 = 6.626e-34'''
json_floats_expected = '''{
    "flt1": 1.0,
    "flt2": 3.1415,
    "flt3": -0.01,
    "flt4": 5e+22,
    "flt5": 1000000.0,
    "flt6": -0.02,
    "flt7": 6.626e-34
}'''
toml_arrays = '''integers = [ 1, 2, 3 ]
colors = [ "red", "yellow", "green" ]
nested_arrays_of_ints = [ [ 1, 2 ], [3, 4, 5] ]
nested_mixed_array = [ [ 1, 2 ], ["a", "b", "c"] ]
string_array = [ "all", 'strings', """are the same""", \'\'\'type\'\'\' ]

# Mixed-type arrays are allowed
numbers = [ 0.1, 0.2, 0.5, 1, 2, 5 ]
contributors = [
  "Foo Bar <foo@example.com>",
  { name = "Baz Qux", email = "bazqux@example.com", url = "https://example.com/bazqux" }
]'''
json_arrays_expected = '''{
    "integers": [
        1,
        2,
        3
    ],
    "colors": [
        "red",
        "yellow",
        "green"
    ],
    "nested_arrays_of_ints": [
        [
            1,
            2
        ],
        [
            3,
            4,
            5
        ]
    ],
    "nested_mixed_array": [
        [
            1,
            2
        ],
        [
            "a",
            "b",
            "c"
        ]
    ],
    "string_array": [
        "all",
        "strings",
        "are the same",
        "type"
    ],
    "numbers": [
        0.1,
        0.2,
        0.5,
        1,
        2,
        5
    ],
    "contributors": [
        "Foo Bar <foo@example.com>",
        {
            "name": "Baz Qux",
            "email": "bazqux@example.com",
            "url": "https://example.com/bazqux"
        }
    ]
}'''

toml_tables = '''[table-1]
key1 = "some string"
key2 = 123

[table-2]
key1 = "another string"
key2 = 456
[dog."tater.man"]
type.name = "pug"'''
json_tables_expected = '''{
    "table-1": {
        "key1": "some string",
        "key2": 123
    },
    "table-2": {
        "key1": "another string",
        "key2": 456
    },
    "dog": {
        "tater.man": {
            "type": {
                "name": "pug"
            }
        }
    }
}'''

toml_inline_tables = '''name = { first = "Tom", last = "Preston-Werner" }
point = { x = 1, y = 2 }
animal = { type.name = "pug" }'''
json_inline_tables_expected = '''{
    "name": {
        "first": "Tom",
        "last": "Preston-Werner"
    },
    "point": {
        "x": 1,
        "y": 2
    },
    "animal": {
        "type": {
            "name": "pug"
        }
    }
}'''

toml_table_array = '''[[products]]
name = "Hammer"
sku = 738594937

[[products]]  # empty table within the array

[[products]]
name = "Nail"
sku = 284758393

color = "gray"'''
json_table_array_expected = '''{
    "products": [
        {
            "name": "Hammer",
            "sku": 738594937
        },
        {},
        {
            "name": "Nail",
            "sku": 284758393,
            "color": "gray"
        }
    ]
}'''


class ParserTestCase(unittest.TestCase):

    def test_toml_with_comments(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_with_comments)
        self.assertEqual(json_with_comments_expected, actual)

    def test_toml_invalid_key_val(self):
        parser = Parser('JSON')
        with self.assertRaises(Exception):
            parser.parse(toml_invalid_key_val)

    def test_toml_bare_keys(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_bare_keys)
        self.assertEqual(json_bare_keys_expected, actual)

    def test_toml_quoted_keys(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_quoted_keys)
        self.assertEqual(json_quoted_keys_expected, actual)

    def test_toml_invalid_quoted_key(self):
        parser = Parser('JSON')
        with self.assertRaises(Exception):
            parser.parse(toml_invalid_quoted_key)

    def test_toml_dot_keys(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_dot_keys)
        self.assertEqual(json_dot_keys_expected, actual)

    def test_toml_integers(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_integers)
        self.assertEqual(json_integers_expected, actual)

    def test_toml_floats(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_floats)
        self.assertEqual(json_floats_expected, actual)

    def test_toml_arrays(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_arrays)
        self.assertEqual(json_arrays_expected, actual)

    def test_toml_tables(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_tables)
        self.assertEqual(json_tables_expected, actual)

    def test_toml_inline_tables(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_inline_tables)
        self.assertEqual(json_inline_tables_expected, actual)

    def test_toml_table_array(self):
        parser = Parser('JSON')
        actual = parser.parse(toml_table_array)
        self.assertEqual(json_table_array_expected, actual)


if __name__ == '__main__':
    unittest.main()
