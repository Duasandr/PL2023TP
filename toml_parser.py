# toml_parser.py - TOML parser
#

from toml_lexer import tokens
import ply.yacc as yacc

# Parsing rules

def p_grammar(p):
    """
toml : expression *( newline expression )

expression :  ws [ comment ]
expression :
            | ws keyval ws [ comment ]
expression :
            | ws table ws [ comment ]

ws : *wschar
wschar :  %x20  
        | %x09  

newline :  %x0A    
         | %x0D.0A 

comment : comment-start-symbol *allowed-comment-char

comment-start-symbol : %x23 

allowed-comment-char : %x01-09 
    | %x0E-7F 
    | non-ascii

non-ascii : %x80-D7FF 
    | %xE000-10FFFF

keyval : key keyval-sep val
key : simple-key 
    | dotted-key
val : string 
    | boolean 
    | array 
    | inline-table 
    | date-time 
    | float 
    | integer

simple-key : quoted-key 
    | unquoted-key

unquoted-key : 1*unquoted-key-char
unquoted-key-char : 
    |   ALPHA 
    | DIGIT 
    | %x2D 
    | %x5F    
    | %xB2 
    | %xB3 
    | %xB9 
    | %xBC-BE  
    | %xC0-D6 
    | %xD8-F6 
    | %xF8-37D 
    | %x37F-1FFF
    | %x200C-200D 
    | %x203F-2040    
    | %x2070-218F 
    | %x2C00-2FEF 
    | %x3001-D7FF
    | %xF900-FDCF 
    | %xFDF0-FFFD
    | %x10000-EFFFF                   

quoted-key : basic-string 
    | literal-string

dotted-key : simple-key 1*( dot-sep simple-key )

dot-sep : ws %x2E ws  
keyval-sep : ws %x3D ws 
string : ml-basic-string 
    | basic-string 
    | ml-literal-string 
    | literal-string


basic-string : quotation-mark *basic-char quotation-mark

quotation-mark : %x22           

basic-char : basic-unescaped 
    | escaped
basic-unescaped : wschar 
    | %x21 
    | %x23-5B 
    | %x5D-7E 
    | non-ascii
escaped : escape escape-seq-char

escape : %x5C                  
escape-seq-char :  %x22         
                | %x5C        
                | %x62         
                | %x65        
                | %x66         
                | %x6E         
                | %x72         
                | %x74         
                | %x78 2HEXDIG
                | %x75 4HEXDIG 
                | %x55 8HEXDIG

ml-basic-string : ml-basic-string-delim [ newline ] ml-basic-body
                |  ml-basic-string-delim
ml-basic-string-delim : 3quotation-mark
ml-basic-body : *mlb-content *( mlb-quotes 1*mlb-content ) [ mlb-quotes ]

mlb-content : basic-char 
    | newline 
    | mlb-escaped-nl
mlb-quotes : 1*2quotation-mark
mlb-escaped-nl : escape ws newline *( wschar 
    | newline )

literal-string : apostrophe *literal-char apostrophe

apostrophe : %x27 

literal-char : %x09 
    | %x20-26 
    | %x28-7E 
    | non-ascii


ml-literal-string : ml-literal-string-delim [ newline ] ml-literal-body
                   | ml-literal-string-delim
ml-literal-string-delim : 3apostrophe
ml-literal-body : *mll-content *( mll-quotes 1*mll-content ) [ mll-quotes ]

mll-content : literal-char 
    | newline
mll-quotes : 1*2apostrophe


integer : dec-int 
    | hex-int 
    | oct-int 
    | bin-int

minus : %x2D                       
plus : %x2B                        
underscore : %x5F                  
digit1-9 : %x31-39                 
digit0-7 : %x30-37                 
digit0-1 : %x30-31                 

hex-prefix : %x30.78               
oct-prefix : %x30.6F               
bin-prefix : %x30.62               

dec-int : [ minus / plus ] unsigned-dec-int
unsigned-dec-int : DIGIT / digit1-9 1*( DIGIT / underscore DIGIT )

hex-int : hex-prefix HEXDIG *( HEXDIG / underscore HEXDIG )
oct-int : oct-prefix digit0-7 *( digit0-7 / underscore digit0-7 )
bin-int : bin-prefix digit0-1 *( digit0-1 / underscore digit0-1 )

float : float-int-part ( exp / frac [ exp ] )
      | special-float

float-int-part : dec-int
frac : decimal-point zero-prefixable-int
decimal-point : %x2E              
zero-prefixable-int : DIGIT *( DIGIT / underscore DIGIT )

exp : "e" float-exp-part
float-exp-part : [ minus / plus ] zero-prefixable-int

special-float : [ minus / plus ] ( inf / nan )
inf : %x69.6e.66  
nan : %x6e.61.6e  


boolean : true 
    | false

true    : %x74.72.75.65     
false   : %x66.61.6C.73.65  


date-time      : offset-date-time | local-date-time | local-date | local-time

date-fullyear  : 4DIGIT
date-month     : 2DIGIT  
date-mday      : 2DIGIT  
time-delim     : "T" / %x20 
time-hour      : 2DIGIT  
time-minute    : 2DIGIT  
time-second    : 2DIGIT  
time-secfrac   : "." 1*DIGIT
time-numoffset : ( "+" | "-" ) time-hour ":" time-minute
time-offset    : "Z" | time-numoffset

partial-time   : time-hour ":" time-minute [ ":" time-second [ time-secfrac ] ]
full-date      : date-fullyear "-" date-month "-" date-mday
full-time      : partial-time time-offset



offset-date-time : full-date time-delim full-time



local-date-time : full-date time-delim partial-time



local-date : full-date



local-time : partial-time



array : array-open [ array-values ] ws-comment-newline array-close

array-open : %x5B 
array-close : %x5D 

array-values :  ws-comment-newline val ws-comment-newline array-sep array-values
             | ws-comment-newline val ws-comment-newline [ array-sep ]

array-sep : %x2C  

ws-comment-newline : *( wschar / [ comment ] newline )


table : std-table / array-table



std-table : std-table-open key std-table-close

std-table-open  : %x5B ws     
std-table-close : ws %x5D     


inline-table : inline-table-open [ inline-table-keyvals ] ws-comment-newline inline-table-close

inline-table-open  : %x7B  
inline-table-close : %x7D  
inline-table-sep   : %x2C  

inline-table-keyvals :  ws-comment-newline keyval ws-comment-newline inline-table-sep inline-table-keyvals
                    | ws-comment-newline keyval ws-comment-newline [ inline-table-sep ]



array-table : array-table-open key array-table-close

array-table-open  : %x5B.5B ws  
array-table-close : ws %x5D.5D  


ALPHA : %x41-5A | %x61-7A 
DIGIT : %x30-39 
"""

parser = yacc.yacc()

data = '''
# This is a TOML document.

title = "TOML Example"

name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00 # First class dates

'''

print(parser.parse(data))
