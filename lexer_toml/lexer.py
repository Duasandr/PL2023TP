from ply import lex

"""
Lexer for TOML files
"""

"""
ASCII table:
| Dec | Hex | Char | Dec | Hex | Char | Dec | Hex | Char | Dec | Hex | Char |
|-----|-----|------|-----|-----|------|-----|-----|------|-----|-----|------|
|  0  |  0  |  NUL | 32  | 20  |  SP  | 64  | 40  |   @  | 96  | 60  |   `  |
|  1  |  1  |  SOH | 33  | 21  |   !  | 65  | 41  |   A  | 97  | 61  |   a  |
|  2  |  2  |  STX | 34  | 22  |   "  | 66  | 42  |   B  | 98  | 62  |   b  |
|  3  |  3  |  ETX | 35  | 23  |   #  | 67  | 43  |   C  | 99  | 63  |   c  |
|  4  |  4  |  EOT | 36  | 24  |   $  | 68  | 44  |   D  | 100 | 64  |   d  |
|  5  |  5  |  ENQ | 37  | 25  |   %  | 69  | 45  |   E  | 101 | 65  |   e  |
|  6  |  6  |  ACK | 38  | 26  |   &  | 70  | 46  |   F  | 102 | 66  |   f  |
|  7  |  7  |  BEL | 39  | 27  |   '  | 71  | 47  |   G  | 103 | 67  |   g  |
|  8  |  8  |  BS  | 40  | 28  |   (  | 72  | 48  |   H  | 104 | 68  |   h  |
|  9  |  9  |  HT  | 41  | 29  |   )  | 73  | 49  |   I  | 105 | 69  |   i  |
| 10  |  A  |  LF  | 42  | 2A  |   *  | 74  | 4A  |   J  | 106 | 6A  |   j  |
| 11  |  B  |  VT  | 43  | 2B  |   +  | 75  | 4B  |   K  | 107 | 6B  |   k  |
| 12  |  C  |  FF  | 44  | 2C  |   ,  | 76  | 4C  |   L  | 108 | 6C  |   l  |
| 13  |  D  |  CR  | 45  | 2D  |   -  | 77  | 4D  |   M  | 109 | 6D  |   m  |
| 14  |  E  |  SO  | 46  | 2E  |   .  | 78  | 4E  |   N  | 110 | 6E  |   n  |
| 15  |  F  |  SI  | 47  | 2F  |   /  | 79  | 4F  |   O  | 111 | 6F  |   o  |
| 16  | 10  |  DLE | 48  | 30  |   0  | 80  | 50  |   P  | 112 | 70  |   p  |
| 17  | 11  |  DC1 | 49  | 31  |   1  | 81  | 51  |   Q  | 113 | 71  |   q  |
| 18  | 12  |  DC2 | 50  | 32  |   2  | 82  | 52  |   R  | 114 | 72  |   r  |
| 19  | 13  |  DC3 | 51  | 33  |   3  | 83  | 53  |   S  | 115 | 73  |   s  |
| 20  | 14  |  DC4 | 52  | 34  |   4  | 84  | 54  |   T  | 116 | 74  |   t  |
| 21  | 15  |  NAK | 53  | 35  |   5  | 85  | 55  |   U  | 117 | 75  |   u  |
| 22  | 16  |  SYN | 54  | 36  |   6  | 86  | 56  |   V  | 118 | 76  |   v  |
| 23  | 17  |  ETB | 55  | 37  |   7  | 87  | 57  |   W  | 119 | 77  |   w  |
| 24  | 18  |  CAN | 56  | 38  |   8  | 88  | 58  |   X  | 120 | 78  |   x  |
| 25  | 19  |  EM  | 57  | 39  |   9  | 89  | 59  |   Y  | 121 | 79  |   y  |
| 26  | 1A  |  SUB | 58  | 3A  |   :  | 90  | 5A  |   Z  | 122 | 7A  |   z  |
| 27  | 1B  |  ESC | 59  | 3B  |   ;  | 91  | 5B  |   [  | 123 | 7B  |   {  |
| 28  | 1C  |  FS  | 60  | 3C  |   <  | 92  | 5C  |   \\ | 124 | 7C  |   |  |
| 29  | 1D  |  GS  | 61  | 3D  |   =  | 93  | 5D  |   ]  | 125 | 7D  |   }  |
| 30  | 1E  |  RS  | 62  | 3E  |   >  | 94  | 5E  |   ^  | 126 | 7E  |   ~  |
| 31  | 1F  |  US  | 63  | 3F  |   ?  | 95  | 5F  |   _  | 127 | 7F  | DEL  |
"""

"""
Content description:
    - Control characters: 
        - 0x01 in hexadecimal represents the Start of Heading (SOH).
        - 0x02 in hexadecimal represents the Start of Text (STX).
        - 0x03 in hexadecimal represents the End of Text (ETX).
        - 0x04 in hexadecimal represents the End of Transmission (EOT).
        - 0x05 in hexadecimal represents the Enquiry (ENQ).
        - 0x06 in hexadecimal represents the Acknowledge (ACK).
        - 0x07 in hexadecimal represents the Bell (BEL).
        - 0x08 in hexadecimal represents the Backspace (BS).
        - 0x09 in hexadecimal represents the Horizontal Tab (HT).
"""


class Lexer:
    # Tokens tuple declaration
    tokens = (
        'WS_CHAR',
        'NEWLINE',
        'COMMENT_START_SYMBOL',
        'ASCII_CONTROL_CHAR',
        'ASCII_PRINTABLE_CHAR',
        'NON_ASCII_CHAR',
        'ALPHA',
        'DIGIT',
        'SUPERSCRIPT_DIGIT',
        'FRACTION_CHAR',
        'LATIN_NON_SYMBOL_CHAR',
        'GREEK_CHAR',
        'GENERAL_PUNCTUATION_CHAR',
        'ENCLOSED_ALPHANUM_CHAR',
        'ENCLOSED_IDEOGRAPH_CHAR',
        'SURROGATE_CHAR',
        'OUTSIDE_BMP_CHAR',
        'DOT',
        'EQUAL',
        'QUOTATION_MARK',
        'REVERSE_SOLIDUS',
        'BACKSPACE',
        'ESCAPE',
        'FORM_FEED',
        'LINE_FEED',
        'CARRIAGE_RETURN',
        'HORIZONTAL_TAB',
        'APOSTROPHE',
        'LITERAL_CHAR',
        'MINUS',
        'PLUS',
        'UNDERSCORE',
        'DIGIT_1_9',
        'DIGIT_0_7',
        'DIGIT_0_1',
        'HEX_PREFIX',
        'OC_PREFIX',
        'BINARY_PREFIX',
        'INF',
        'NAN',
        'TRUE',
        'FALSE',
        'LEFT_BRACKET',
        'RIGHT_BRACKET',
        'COMMA',
        'LEFT_CURLY_BRACKET',
        'RIGHT_CURLY_BRACKET'
    )

    # Tokens regex declaration
    t_WS_CHAR = r'[ \t]+'  # Whitespace character (space or tab)
    t_NEWLINE = r'[\n\r]'  # Newline character (line feed) or (carriage return)
    t_COMMENT_START_SYMBOL = r'\#'  # Comment start character (hash)
    t_ASCII_CONTROL_CHAR = r'[\x01-\x09]'  # Control characters
    t_ASCII_PRINTABLE_CHAR = r'[\x0E-\x7E]'  # ASCII printable characters
    #t_NON_ASCII_CHAR = r'[\x80-D7FF\xE000-10FFFF]'  # Non-ASCII characters (Unicode)
    t_ALPHA = r'[a-zA-Z]'  # Alphabetic characters
    t_DIGIT = r'[0-9]'  # Numeric characters
    t_SUPERSCRIPT_DIGIT = r'[\xB2\xB3\xB9]'  # Superscript numeric characters  (² ³ ¹)
    #t_FRACTION_CHAR = r'[\xBC\BD\BE]'  # Fractions characters (¼ ½ ¾)
    #t_LATIN_NON_SYMBOL_CHAR = r'[\xC0-D6\xD8-F6\xF8-37D]'  # Latin non-symbol characters (À-ÖØ-öø-ͽ)
    #t_GREEK_CHAR = r'[\x37F-1FFF]'  # Greek block characters (Ϳ-῿) without greek question mark (;)
    #t_GENERAL_PUNCTUATION_CHAR = r'[\x200C-200D\x203F-\x2040 ]'  # General punctuation characters (‿⁀-⁁) includes ZWJ ZWNJ
    t_ENCLOSED_ALPHANUM_CHAR = r'[\x2070-218F\x2460-24FF]'  # Enclosed alphanumeric characters (⁰-↏①-⓿)
    t_ENCLOSED_IDEOGRAPH_CHAR = r'[\x2C00-2FEF\x3001-D7FF]'  # Enclosed ideographic characters (㈀-㋿㌀-㏿)
    t_SURROGATE_CHAR = r'[\xF900-FDCF\xFDF0-FFFD]'  # Surrogate characters (豈-﷏ﷰ-�)
    t_OUTSIDE_BMP_CHAR = r'[\x10000-EFFFF]'  # BMP characters (𐀀-󯿿)
    t_DOT = r'\.'
    t_EQUAL = r'='
    t_QUOTATION_MARK = r'\"'
    t_REVERSE_SOLIDUS = r'\\'
    t_BACKSPACE = r'\b'
    #t_ESCAPE = r'\e'
    t_FORM_FEED = r'\f'
    t_LINE_FEED = r'\n'
    t_CARRIAGE_RETURN = r'\r'
    t_HORIZONTAL_TAB = r'\t'
    t_APOSTROPHE = r'\''
    t_LITERAL_CHAR = r'[\x20-26\x28-7E]'  # (space - & ( ) * + , - . / 0-9 : ; < = > ? @ A-Z [ \ ] ^ _ ` a-z)
    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_UNDERSCORE = r'_'
    t_DIGIT_1_9 = r'[1-9]'  # Numeric characters without 0
    t_DIGIT_0_7 = r'[0-7]'  # Numeric characters without 8 and 9
    t_DIGIT_0_1 = r'[0-1]'  # Numeric characters without 2-9
    t_HEX_PREFIX = r'0x'  # Hexadecimal prefix
    t_OC_PREFIX = r'0c'  # Octal prefix
    t_BINARY_PREFIX = r'0b'  # Binary prefix
    t_INF = r'inf'  # Infinity
    t_NAN = r'nan'  # Not a number
    t_TRUE = r'true'  # True
    t_FALSE = r'false'  # False
    t_LEFT_BRACKET = r'\['  # Left bracket
    t_RIGHT_BRACKET = r'\]'  # Right bracket


    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Error handling
    def t_error(self, t):
        """Error handling rule for illegal characters"""
        print("Illegal character: {!r} ".format(t.value[0]))
        t.lexer.skip(1)

    def lexer(self):
        return self.lexer

    def token(self):
        return self.lexer.token()

    def input(self, data):
        self.lexer.input(data)

    # Build the lexer
    def build(self, **kwargs):
        """
        Build the lexer
        :param kwargs: Additional arguments to pass to the lexer constructor
        """
        self.lexer = lex.lex(module=self, **kwargs)
