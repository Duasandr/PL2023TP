import ply.lex as lex

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
        'COMMENT',
        'ID',
        'STRING',
        'NUM',
        'DOT',
        'EQUAL',
        'MINUS',
        'PLUS',
        'UNDERSCORE',
        'TRUE',
        'FALSE',
        'LEFT_BRACKET',
        'RIGHT_BRACKET',
        'COMMA',
        'LEFT_CURLY_BRACKET',
        'RIGHT_CURLY_BRACKET'
    )

    # Tokens regex declaration
    t_ignore = ' \t'  # Whitespace character (space or tab)
    t_ID = r'[a-zA-Z]+'  # Alphabetic characters
    t_STRING = r'([\'"])(.*?)[\'"]'  # String characters
    t_NUM = r'[0-9]+'  # Numeric characters
    t_DOT = r'\.'
    t_EQUAL = r'='
    t_MINUS = r'-'
    t_PLUS = r'\+'
    t_UNDERSCORE = r'_'
    t_LEFT_BRACKET = r'\['  # Left bracket
    t_RIGHT_BRACKET = r'\]'  # Right bracket

    def __init__(self):
        self.lex = lex.lex(module=self)

    def t_COMMENT(self, t):
        r'\#.*'
        t.lexer.lineno += t.value.count('\n')
        t.lexer.skip(1)

    def t_NEWLINE(self, t):
        r'[\n\r]+'
        t.lexer.lineno += len(t.value)
        return t

    # Error handling
    def t_error(self, t):
        """Error handling rule for illegal characters"""
        print("Illegal character: {!r} ".format(t.value[0]))
        t.lexer.skip(1)

    def token(self):
        return self.lex.token()

    def input(self, data):
        self.lex.input(data)
