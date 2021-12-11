import re
identifiers = '[_a-zA-Z][_a-zA-Z0-9]*'
integers = '[0-9][0-9]*'
float_val = '\d+\.\d*'
float_val1 = '\.\d+'
octal = '[0][0-7]{1,2}'
hexadecimal = '[0][x][0-9a-fA-f]{1,2}'
operations = {'=':'assign_op', '+':'add_op', '-':'sub_op', '*':'mul_op', '/':'div_op', '%':'mod_op', '\'':'single_quotes', '"':'double_quotes', '(':'left_paranthesis',')':'right_paranthesis', ';':'delimiter','{':'left_curly','}':'right_curly', '>':"GREATER_THAN", '<':"LESS_THAN", "!":"EXCLAMATION", ":":"EACH"}
keywords = {'auto':'AUTO_CODE','const':'CONST_CODE','double':'DOUBLE_CODE','float':'FLOAT_CODE','int':"INT_CODE",'short':'SHORT_CODE','struct':'STRUCT_CODE','unsigned':'UNSIGNED_CODE','break':"BREAK_CODE",'continue':'CONTINUE_CODE','else':'ELSE_CODE','for':'FOR_CODE','long':'LONG_CODE','signed':'SIGNED_CODE','switch':'SWITCH_CODE','void':'VOID_CODE','case':'CASE_CODE','default':'DEFAULT_CODE','enum':"ENUM_CODE",'goto':'GOTO_CODE','register':'REGISTER_CODE','sizeof':'SIZEOF_CODE','typedef':'TYPEDEF_CODE','volatile':'VOLATILE_CODE','char':'CHAR_CODE','do':'DO_CODE','extern':"EXTERN_CODE",'if':'IF_CODE','return':'RETURN_CODE','static':'STATIC_CODE','union':'UNION_CODE','while':'WHILE_CODE', 'main':'MAIN_CODE', 'forEach':'FOREACH_CODE', "assign": "ASSIGN_KEY"}
delimiter = ';'
parsed_array = []
val_temp=''
with open('input.txt','r') as file:
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
        elif parsed_array[i][0] == 'true':
            temp_var = list(['true','BOOLEAN'])
            parsed_array[i] = tuple(temp_var)
        elif parsed_array[i][0] == 'false':
            temp_var = list(['false', 'BOOLEAN'])
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

for i in range(len(parsed_array)):
        if parsed_array[i][0] == 'true':
            temp_var = list(['1','INTEGER'])
            parsed_array[i] = tuple(temp_var)
        elif parsed_array[i][0] == 'false':
            temp_var = list(['0', 'INTEGER'])
            parsed_array[i] = tuple(temp_var)

final_type = 'INTEGER'
for i in range(len(parsed_array)):
    if parsed_array[i][1] == 'FLOAT':
        final_type = 'FLOAT'
final_value = None
def lex():
    global nextToken
    global nextValue
    if parsed_array:
        val = parsed_array.pop(0)
        nextToken = val[1]
        nextValue = val[0]
        print(nextToken)   

def expr():
    global final_value
    print("Enter <expr>")
    if nextToken == 'INTEGER':
        final_value = int(nextValue)
    elif nextToken == 'FLOAT':
        final_value = float(nextValue)

    term()
    while (nextToken == 'add_op' or nextToken == 'sub_op'):
        if nextToken == 'add_op':
            lex()
            term()
        elif nextToken == 'sub_op':
            lex()
            term()
    print("Exit <expr>")
    
def term():
    global final_value
    print("Enter <term>")
    factor()
    while(nextToken == 'mul_op' or nextToken == 'div_op' or nextToken == 'mod_op'):
        if nextToken == 'mul_op':
            lex()
            if nextToken == 'INTEGER':
                final_value *= int(nextValue)
            elif nextToken == 'FLOAT':
                final_value *= float(nextValue)
            factor()
        elif nextToken == 'div_op' or nextToken=='mod_op':
            lex()
            if nextToken == 'INTEGER' and int(nextValue) == 0 or nextToken == 'FLOAT' and float(nextValue) == 0.0:
                print('MathERROR: Zero Division')
                exit()
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
def error():
    print("You messed up. You are not worthy!!")
    exit()

def assign():
    print('START <assignment>')
    global expected_type
    lex()
    if nextToken != "ASSIGN_KEY":
        error()
    lex()
    if nextValue == 'int':
        expected_type = 'INTEGER'
        lex()
        if nextToken != 'IDENTIFIER':
            error()
        lex()
        if nextToken != 'assign_op':
            error()
        lex()
        expr()
        if nextToken != 'delimiter':
            error()
        if expected_type == final_type:
            print('the expected type and actual type are matching')
        else:
            print('TypeError: assignment not possible')
            exit()    
        print('END <assingment>')
    elif nextValue == 'float':
        expected_type = 'FLOAT'
        lex()
        if nextToken != 'IDENTIFIER':
            error()
        lex()
        if nextToken != 'assign_op':
            error()
        lex()
        expr()
        if nextToken != 'delimiter':
            error()
        if expected_type == final_type:
            print('the expected type and actual type are matching')
        else:
            print('TypeError: assigment not possible')
            exit()    
        print('END <assignment>')

assign()  