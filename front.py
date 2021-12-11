import re
identifiers = '[_a-zA-Z][_a-zA-Z0-9]*'
integers = '[0-9][0-9]*'
float_val = '\d+\.\d*'
float_val1 = '\.\d+'
octal = '[0][0-7]{1,2}'
hexadecimal = '[0][x][0-9a-fA-f]{1,2}'
operations = {'=':'assign_op', '+':'add_op', '-':'sub_op', '*':'mul_op', '/':'div_op', '%':'mod_op', '\'':'single_quotes', '"':'double_quotes', '(':'left_paranthesis',')':'right_paranthesis', ';':'delimiter','{':'left_curly','}':'right_curly', '>':"GREATER_THAN", '<':"LESS_THAN", "!":"EXCLAMATION", ":":"EACH"}
keywords = {'auto':'AUTO_CODE','const':'CONST_CODE','double':'DOUBLE_CODE','float':'FLOAT_CODE','int':"INT_CODE",'short':'SHORT_CODE','struct':'STRUCT_CODE','unsigned':'UNSIGNED_CODE','break':"BREAK_CODE",'continue':'CONTINUE_CODE','else':'ELSE_CODE','for':'FOR_CODE','long':'LONG_CODE','signed':'SIGNED_CODE','switch':'SWITCH_CODE','void':'VOID_CODE','case':'CASE_CODE','default':'DEFAULT_CODE','enum':"ENUM_CODE",'goto':'GOTO_CODE','register':'REGISTER_CODE','sizeof':'SIZEOF_CODE','typedef':'TYPEDEF_CODE','volatile':'VOLATILE_CODE','char':'CHAR_CODE','do':'DO_CODE','extern':"EXTERN_CODE",'if':'IF_CODE','return':'RETURN_CODE','static':'STATIC_CODE','union':'UNION_CODE','while':'WHILE_CODE', 'main':'MAIN_CODE', 'forEach':'FOREACH_CODE', 'fn':'FUNCTION_CODE'}
delimiter = ';'
parsed_array = []
val_temp=''
with open('front.c','r') as file:
    while True:
        new_char = file.read(1)
        if new_char=="":
            break
        token = new_char
        identifier = re.fullmatch(identifiers, new_char)
        if identifier:
            val='IDENTIFIER'
        integer = re.fullmatch(integers, new_char)
        floats = re.fullmatch(float_val, new_char)
        if integer:
            val='INTEGER'
        if new_char == ".":
            while new_char!='':
                next_char = file.read(1)
                if next_char == "":
                    break
                if next_char == " ":
                    break
                temp_char = token + next_char
                float_dot = re.fullmatch(float_val1, temp_char)
                if float_dot:
                    token = temp_char
                    val = "FLOAT" 
                if next_char in operations.keys():
                    val_temp = operations[next_char]  
                else:
                    break
        if new_char!="" and new_char in operations.keys():
            val = operations[new_char]
            parsed_array.append((new_char, val))              
        while new_char!='' and identifier: 
            next_char = file.read(1)
            if next_char == "":
                break
            if next_char == " ":
                break
            temp_char = token + next_char
            identifier = re.fullmatch(identifiers, temp_char)
            if identifier:
                token = temp_char
                val="IDENTIFIER"
            if next_char in operations.keys():
                val_temp = operations[next_char]   
        while new_char!='' and integer or floats:
            next_char = file.read(1)
            if next_char == "":
                break
            if next_char == " ":
                break
            temp_char = token + next_char
            integer = re.fullmatch(integers, temp_char)
            floats = re.fullmatch(float_val, temp_char)
            if floats:
                token = temp_char
                val = "FLOAT"
            elif integer:
                token = temp_char
                val="INTEGER"
            if next_char in operations.keys():
                val_temp = operations[next_char]
        
        if val == "IDENTIFIER" or val == "INTEGER" or val=="FLOAT" or val=="OCTAL"and token != " " and token != "\n":
            if token != " ":
                parsed_array.append((token,val))
            token=''
            val=""
        if val_temp and next_char != " " and next_char != "\n":
            parsed_array.append((next_char, val_temp))
            val_temp=''
        token=''
        val=""
        if new_char=="":
            break 
for i in range(len(parsed_array)):
    if parsed_array[i][1] == 'IDENTIFIER':
        if parsed_array[i][0] in keywords.keys():
            temp_var = list([parsed_array[i][0],keywords[parsed_array[i][0]]])
            parsed_array[i] = tuple(temp_var)
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "=" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("==", 'EQUALITY_OPERATOR')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == ">" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = (">=", 'GREAT_EQUAL')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "<" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("<=", 'LESS_EQUAL')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "!" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("!=", 'NOT_EQUAL')
    else:
        i +=1
for i in parsed_array:
    print(i)

############################RDA Algorithm#################################################
# <stmt> := <if_stmt>|<while_stmt>|<for_stmt>

def lex():
    global nextToken
    if parsed_array:
        val = parsed_array.pop(0)
        val = val[1]
        nextToken = val
        print(nextToken)
    else:
        nextToken = None

def stmt():
    lex()
    if nextToken == 'INT_CODE' or nextToken == 'FLOAT_CODE' or nextToken == 'DOUBLE_CODE' or nextToken=='IDENTIFIER':
        assignment_stmt()
    elif nextToken == 'WHILE_CODE':
        while_stmt()
    elif nextToken == 'FOR_CODE':
        for_stmt()
    elif nextToken == 'IF_CODE':
        if_stmt()
    elif nextToken == 'RETURN_CODE':
        return_stmt()
    elif nextToken == 'FOREACH_CODE':
        forEach_stmt()
    elif nextToken == 'DO_CODE':
        do_while_stmt()
    elif nextToken == 'left_curly':
        block()
    elif nextToken == 'SWITCH_CODE':
        switch_stmt()
def block():
    print("Start <block>")
    if nextToken != 'left_curly':
        error()
    while nextToken != 'right_curly' and parsed_array:
        stmt()
    if nextToken == 'right_curly':
        print("END <block>")
    else:
        error()
        
 
def assignment_stmt():
    print('Enter <assign statement>')
    if nextToken == 'INT_CODE' or nextToken == 'FLOAT_CODE' or nextToken=='DOUBLE_CODE':
        lex()
        if nextToken != 'IDENTIFIER':
            error()
        lex()
        if nextToken == 'assign_op':
            lex()
            expr()
            if nextToken != 'delimiter':
                error()
            print('End <assignement statement>')
            return
        elif nextToken == "delimiter":
            print('END <assignment statement>')
        else:
            error()
    elif nextToken == 'IDENTIFIER':
        lex()
        if nextToken == 'assign_op':
            lex()
            expr()
            if nextToken != 'delimiter':
                error()
            print('End <assignement statement>')
        else:
            error()

    else:
        error()

def expr():
    print("Enter <expr>")
    term()
    while (nextToken == 'add_op' or nextToken == 'sub_op'):
        lex()
        term()
    print("Exit <expr>")
    
def term():
    print("Enter <term>")
    factor()

    while(nextToken == 'mul_op' or nextToken == 'div_op' or nextToken == 'mod_op'):
        lex()
        factor()
    print("Exit <term>")
    

def factor():
    print("Enter <factor>")
    if (nextToken == 'IDENTIFIER' or nextToken == 'INTEGER' or nextToken == 'FLOAT'):
        lex()

    elif nextToken == 'left_paranthesis':
        lex()
        expr()
        if nextToken == 'right_paranthesis':
            lex()
        else:
            error()
    else:
        error()
    print("Exit <factor>")




def bool_expr():
    print("Enter <bool_expr>")
    expr()
    if nextToken == "EQUALITY_OPERATOR" or nextToken == "NOT_EQUAL" or nextToken == "GREAT_EQUAL" or nextToken =="LESS_EQUAL" or nextToken == "GREATER_THAN" or nextToken == "LESS_THAN":
        lex()
        expr()
    else:
        error()
    print("End <bool_expr>")
    


def error():
    print("You messed up. You are not worthy!!")
    exit()



def if_stmt():
    print("Enter <IF STMT>")
    if (nextToken != 'IF_CODE'):
        error()
    else:
        lex()
        if (nextToken != 'left_paranthesis'):
            error()
        else:
            lex()
            bool_expr()
            if nextToken != 'right_paranthesis':
                error()
            else:
                stmt()
                lex()
                if nextToken == 'ELSE_CODE':
                    print("ENTER <ELSE STMT>")
                    stmt()
                    print("EXIT <ELSE STMT>")
    print("End <IF STMT>")
def for_stmt():
    print("Enter <FOR STATMENT>")
    if nextToken != 'FOR_CODE':
        error()
    lex()
    if nextToken!='left_paranthesis':
        error()
    while nextToken != 'delimiter' and parsed_array:
        lex()
    if nextToken != 'delimiter':
        error()
    lex()
    while nextToken != 'delimiter' and parsed_array:
        lex()
    if nextToken != 'delimiter':
        error()
    while nextToken != 'right_paranthesis' and parsed_array:
        lex()
    if nextToken != 'right_paranthesis':
        error()
    stmt()
    print("End <for statement>") 
def forEach_stmt():
    print("Enter <forEach statement>")
    if nextToken != "FOREACH_CODE":
        error()
    lex()
    if nextToken != 'left_paranthesis':
        error()
    lex()
    if nextToken != 'IDENTIFIER':
        error()
    lex()
    if nextToken != 'EACH':
        error()
    lex()
    if nextToken != 'IDENTIFIER':
        error()
    lex()
    if nextToken != 'right_paranthesis':
        error()
    else:
        stmt()
    print('End <forEach statement>')
def while_stmt():
    print('Enter <while statement>')
    if nextToken != 'WHILE_CODE':
        error()
    else:
        lex()
        if nextToken != 'left_paranthesis':
            error()
        else:
            lex()
            bool_expr()
            if nextToken != 'right_paranthesis':
                error()
            else:
                stmt()
    print("End <while statement>")
def switch_stmt():
    print('Enter <switch statement>')
    if nextToken != 'SWITCH_CODE':
        error()
    else:
        lex()
        if nextToken != 'left_paranthesis':
            error()
        lex()
        expr()
        if nextToken != 'right_paranthesis':
            error()
        lex()
        if nextToken != 'left_curly':
            error()
        
        lex()
        if nextToken == 'CASE_CODE' or nextToken == 'DEFAULT_CODE':
            lex()
            expr()
            if nextToken != 'EACH':
                error()
            stmt()
        else:
            if nextToken != 'right_curly':
                error()
        print('End <switch statement>')
def return_stmt():
    print("Enter <Return statement>")
    if nextToken != 'RETURN_CODE':
        error()
    lex()
    expr()
    print('End <return statement>')
def do_while_stmt():
    print('Enter <Do While Statement>')
    if nextToken != 'DO_CODE':
        error()
    stmt()
    lex()
    if nextToken != "WHILE_CODE":
        error()
    lex()
    if nextToken != "left_paranthesis":
        error()
    lex()
    bool_expr()
    if nextToken != 'right_paranthesis':
        print(nextToken)
        error()
    lex()
    if nextToken != 'delimiter':
        error()
    print("End <Do While Statement>")
def program():
    print('START <Program>')
    lex()
    if nextToken != 'VOID_CODE':
        error()
    lex()
    if nextToken != 'MAIN_CODE':
        error()
    lex()
    if nextToken != 'left_paranthesis':
        error()
    lex()
    if nextToken != 'right_paranthesis':
        error()
    else:
        stmt()
    print('END <Program>')                 

#starts cheking the syntax of the program        
program()