# ==========================================================
# parsers.py
# Assignment 2 – Syntax Analyzer
# ==========================================================

import sys
from lexicon import lexer
from contextlib import redirect_stdout

# ==========================================
# GLOBALS
# ==========================================

tokens = []
current_token = None
token_index = -1

PRINT_RULES = True


# ==========================================
# OUTPUT HELPERS
# ==========================================

def format_token_name(token_type, lexeme=None):
    if lexeme == 'function':
        return 'Keyword'
    elif token_type == 'IDENTIFIER':
        return 'Identifier'
    elif token_type == 'KEYWORD':
        return 'Keyword'
    elif token_type == 'OPERATOR':
        return 'Operator'
    elif token_type == 'SEPARATOR':
        return 'Separator'
    elif token_type == 'INTEGER':
        return 'Integer'
    elif token_type == 'REAL':
        return 'Real'
    elif token_type == 'EOF':
        return 'EOF'
    else:
        return token_type


def print_token(token):
    token_type, lexeme = token
    print(f"Token: {format_token_name(token_type, lexeme):<20} Lexeme: {lexeme}")


def print_rule(rule):
    if PRINT_RULES:
        print(f"     {rule}")


# ==========================================
# TOKEN CONTROL
# ==========================================

def next_token():
    global token_index
    global current_token

    token_index += 1

    if token_index < len(tokens):
        current_token = tokens[token_index]
        print_token(current_token)
    else:
        current_token = ('EOF', 'EOF')


def match(expected):
    if current_token[1] == expected:
        next_token()
    else:
        error(expected)


def error(expected):
    print("\nSyntax Error")
    print(f"Expected: {expected}")
    print(f"Found Token: {format_token_name(current_token[0], current_token[1])}")
    print(f"Found Lexeme: {current_token[1]}")
    print(f"At token index: {token_index}")
    sys.exit()


# ==========================================
# PROGRAM
# ==========================================

def Program():
    print_rule("<Rat26S> -> @ <Opt Function Definitions> @ <Opt Declaration List> @ <Statement List> @")

    match('@')
    OptFunctionDefinitions()

    match('@')
    OptDeclarationList()

    match('@')
    StatementList()

    match('@')


# ==========================================
# FUNCTION DEFINITIONS
# ==========================================

def OptFunctionDefinitions():
    if current_token[1] == 'function':
        print_rule("<Opt Function Definitions> -> <Function Definitions>")
        FunctionDefinitions()
    else:
        print_rule("<Opt Function Definitions> -> ε")


def FunctionDefinitions():
    print_rule("<Function Definitions> -> <Function> <Function Definitions Prime>")
    Function()
    FunctionDefinitionsPrime()


def FunctionDefinitionsPrime():
    if current_token[1] == 'function':
        print_rule("<Function Definitions Prime> -> <Function> <Function Definitions Prime>")
        Function()
        FunctionDefinitionsPrime()
    else:
        print_rule("<Function Definitions Prime> -> ε")


def Function():
    print_rule("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")

    match('function')
    Identifier()
    match('(')
    OptParameterList()
    match(')')
    OptDeclarationList()
    Body()


def OptParameterList():
    if current_token[0] == 'IDENTIFIER':
        print_rule("<Opt Parameter List> -> <Parameter List>")
        ParameterList()
    else:
        print_rule("<Opt Parameter List> -> ε")


def ParameterList():
    print_rule("<Parameter List> -> <Parameter> <Parameter List Prime>")
    Parameter()
    ParameterListPrime()


def ParameterListPrime():
    if current_token[1] == ',':
        print_rule("<Parameter List Prime> -> , <Parameter> <Parameter List Prime>")
        match(',')
        Parameter()
        ParameterListPrime()
    else:
        print_rule("<Parameter List Prime> -> ε")


def Parameter():
    print_rule("<Parameter> -> <IDs> <Qualifier>")
    IDs()
    Qualifier()


def Body():
    print_rule("<Body> -> { <Statement List> }")
    match('{')
    StatementList()
    match('}')


# ==========================================
# DECLARATIONS
# ==========================================

def OptDeclarationList():
    if current_token[1] in ['integer', 'boolean', 'real']:
        print_rule("<Opt Declaration List> -> <Declaration List>")
        DeclarationList()
    else:
        print_rule("<Opt Declaration List> -> ε")


def DeclarationList():
    print_rule("<Declaration List> -> <Declaration> ; <Declaration List Prime>")
    Declaration()
    match(';')
    DeclarationListPrime()


def DeclarationListPrime():
    if current_token[1] in ['integer', 'boolean', 'real']:
        print_rule("<Declaration List Prime> -> <Declaration> ; <Declaration List Prime>")
        Declaration()
        match(';')
        DeclarationListPrime()
    else:
        print_rule("<Declaration List Prime> -> ε")


def Declaration():
    print_rule("<Declaration> -> <Qualifier> <IDs>")
    Qualifier()
    IDs()


def Qualifier():
    if current_token[1] in ['integer', 'boolean', 'real']:
        print_rule(f"<Qualifier> -> {current_token[1]}")
        next_token()
    else:
        error("integer | boolean | real")


def IDs():
    print_rule("<IDs> -> <Identifier> <IDs Prime>")
    Identifier()
    IDsPrime()


def IDsPrime():
    if current_token[1] == ',':
        print_rule("<IDs Prime> -> , <Identifier> <IDs Prime>")
        match(',')
        Identifier()
        IDsPrime()
    else:
        print_rule("<IDs Prime> -> ε")


# ==========================================
# STATEMENT LIST
# ==========================================

def starts_statement():
    return current_token[0] == 'IDENTIFIER' or current_token[1] in ['while', '{', 'return']


def StatementList():
    print_rule("<Statement List> -> <Statement> <Statement List Prime>")
    Statement()
    StatementListPrime()


def StatementListPrime():
    if starts_statement():
        print_rule("<Statement List Prime> -> <Statement> <Statement List Prime>")
        Statement()
        StatementListPrime()
    else:
        print_rule("<Statement List Prime> -> ε")


# ==========================================
# STATEMENT
# ==========================================

def Statement():
    if current_token[0] == 'IDENTIFIER':
        print_rule("<Statement> -> <Assign>")
        Assign()

    elif current_token[1] == 'while':
        print_rule("<Statement> -> <While>")
        While()

    elif current_token[1] == '{':
        print_rule("<Statement> -> <Compound>")
        Compound()

    elif current_token[1] == 'return':
        print_rule("<Statement> -> <Return>")
        Return()

    else:
        error("Statement")


# ==========================================
# COMPOUND
# ==========================================

def Compound():
    print_rule("<Compound> -> { <Statement List> }")
    match('{')
    StatementList()
    match('}')


# ==========================================
# ASSIGN
# ==========================================

def Assign():
    print_rule("<Assign> -> <Identifier> = <Expression> ;")
    Identifier()
    match('=')
    Expression()
    match(';')


# ==========================================
# RETURN
# ==========================================

def Return():
    if current_token[1] == 'return':
        next_token()
    else:
        error("return")

    if current_token[1] == ';':
        print_rule("<Return> -> return ;")
        next_token()
    else:
        print_rule("<Return> -> return <Expression> ;")
        Expression()
        match(';')


# ==========================================
# WHILE
# ==========================================

def While():
    print_rule("<While> -> while ( <Condition> ) <Statement>")
    match('while')
    match('(')
    Condition()
    match(')')
    Statement()


# ==========================================
# CONDITION / RELOP
# ==========================================

def Condition():
    print_rule("<Condition> -> <Expression> <Relop> <Expression>")
    Expression()
    RelOp()
    Expression()


def RelOp():
    if current_token[1] in ['==', '!=', '<', '>', '<=', '>=']:
        print_rule(f"<Relop> -> {current_token[1]}")
        next_token()
    else:
        error("Relational Operator")


# ==========================================
# IDENTIFIER
# ==========================================

def Identifier():
    print_rule("<Identifier> -> id")
    if current_token[0] == 'IDENTIFIER' and current_token[1] != 'function':
        next_token()
    else:
        error("Identifier")


# ==========================================
# EXPRESSION
# ==========================================

def Expression():
    print_rule("<Expression> -> <Term> <Expression Prime>")
    Term()
    ExpressionPrime()


def ExpressionPrime():
    if current_token[1] in ['+', '-']:
        if current_token[1] == '+':
            print_rule("<Expression Prime> -> + <Term> <Expression Prime>")
        else:
            print_rule("<Expression Prime> -> - <Term> <Expression Prime>")
        next_token()
        Term()
        ExpressionPrime()
    else:
        print_rule("<Expression Prime> -> ε")


# ==========================================
# TERM
# ==========================================

def Term():
    print_rule("<Term> -> <Factor> <Term Prime>")
    Factor()
    TermPrime()


def TermPrime():
    if current_token[1] in ['*', '/']:
        if current_token[1] == '*':
            print_rule("<Term Prime> -> * <Factor> <Term Prime>")
        else:
            print_rule("<Term Prime> -> / <Factor> <Term Prime>")
        next_token()
        Factor()
        TermPrime()
    else:
        print_rule("<Term Prime> -> ε")


# ==========================================
# FACTOR / PRIMARY
# ==========================================

def Factor():
    print_rule("<Factor> -> <Primary>")
    Primary()


def Primary():
    if current_token[0] == 'IDENTIFIER':
        print_rule("<Primary> -> <Identifier>")
        Identifier()

    elif current_token[0] == 'INTEGER':
        print_rule("<Primary> -> <Integer>")
        next_token()

    elif current_token[0] == 'REAL':
        print_rule("<Primary> -> <Real>")
        next_token()

    elif current_token[1] == '(':
        print_rule("<Primary> -> ( <Expression> )")
        match('(')
        Expression()
        match(')')

    else:
        error("Identifier | Integer | Real | ( Expression )")


# ==========================================
# PARSER ENTRY
# ==========================================

def parse(token_list):
    global tokens
    global current_token
    global token_index

    tokens = token_list
    current_token = None
    token_index = -1

    next_token()
    Program()

    if current_token[0] != 'EOF':
        error("EOF")

    print("\nParsing Completed Successfully!")


# ==========================================
# RUN ONE TEST
# ==========================================

def run_test(input_file, output_file):
    with open(input_file, "r") as f:
        file = f.read()

    token_list = lexer(file)

    with open(output_file, "w", encoding="utf-8") as out:
        with redirect_stdout(out):
            parse(token_list)


# ==========================================
# MAIN DRIVER
# ==========================================

if __name__ == "__main__":
    run_test("test_files/test1.txt", "output_files/test1output.txt")
    run_test("test_files/test2.txt", "output_files/test2output.txt")
    run_test("test_files/test3.txt", "output_files/test3output.txt")

    print("All 3 test outputs generated successfully.")