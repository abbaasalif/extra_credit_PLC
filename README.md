# Extra Credit for PLC

## Team: 

Abbaas Alif
<br><br>
Michelle Serrano 
<br><br>
Chihumeya Eresia-Eke
<br><br>
---------------------------------

Where a your specification document must fully explain the language you have designed:
Description of every data type that is provided with the language

Int: [0-9][0-9]*'

Float: '\d+\.\d*'

Floats2: '\.\d+'

Instructions of how to create valid code.

<factor> --> identifier | float | int

<term> --> <factor>| <term> / factor | <term> * <factor> | <term> % <factor>
<expression> -->  <term> | <expression> + <term> | <expression> - <term>
<bool> --> <expression> ( '<=' | '>=' | '<' | '>' |'==' | '!=' ) <expression>
<stmt> -->  <do_while_stmt> | <while_stmt> |<if_stmt>| <for_stmt> | <forEach_stmt> | <switch_stmt>| <assignment >|<return_stmt>|<block>
 
<switch_stmt> --> switch'{'{case <expression>: <stmt>} [default : <stmt>] '}'
<foreach_stmt> --> foreach'('<variable> ':' <expression> ')'<stmt>
<for_stmt> --> for(<expression>; <expression>; <expression>)<statement>
<while_stmt> --> while '(' <bool> ')' <statement>
<do_while_stmt> --> do <statement> while '(' <bool> ')'
<block> --> '{' (' ' | <stmt>) '}'
<if_stmt> --> if'('<bool> |<expression>')' <stmt> [else <stmt>]
<assignment > - IDENTIFIER ‘=’ <expression>
<return_stmt> --> return <expression

