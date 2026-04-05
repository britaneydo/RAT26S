# ==========================================================
# parsers.py
# Assignment 2 – Syntax Analyzer
# ==========================================================

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

def format_token_name(token_type):
    if token_type == 'IDENTIFIER':
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
    print(f"Token: {format_token_name(token_type):<20} Lexeme: {lexeme}")


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


def error(expected):
    print("\nSyntax Error")
    print(f"Expected: {expected}")
    print(f"Found Token: {format_token_name(current_token[0])}")
    print(f"Found Lexeme: {current_token[1]}")
    print(f"At token index: {token_index}")
    exit()


# ==========================================
# PROGRAM
# ==========================================

def Program():
    print_rule("<Program> -> <Statement List>")
    StatementList()


# ==========================================
# STATEMENT LIST
# ==========================================

def StatementList():
    print_rule("<Statement List> -> <Statement> <Statement List Prime>")
    Statement()
    StatementListPrime()


def StatementListPrime():
    if current_token[0] == 'IDENTIFIER' or current_token[1] in ['while', '{']:
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

    else:
        error("Statement")


# ==========================================
# COMPOUND
# ==========================================

def Compound():
    print_rule("<Compound> -> { <Statement List> }")

    if current_token[1] == '{':
        next_token()
    else:
        error("{")

    StatementList()

    if current_token[1] == '}':
        next_token()
    else:
        error("}")


# ==========================================
# ASSIGN
# ==========================================

def Assign():
    print_rule("<Assign> -> <Identifier> = <Expression> ;")

    Identifier()

    if current_token[1] == '=':
        next_token()
    else:
        error("=")

    Expression()

    if current_token[1] == ';':
        next_token()
    else:
        error(";")


# ==========================================
# WHILE
# ==========================================

def While():
    print_rule("<While> -> while ( <Expression> ) <Statement>")

    if current_token[1] == 'while':
        next_token()
    else:
        error("while")

    if current_token[1] == '(':
        next_token()
    else:
        error("(")

    Expression()

    if current_token[1] == ')':
        next_token()
    else:
        error(")")

    Statement()


# ==========================================
# IDENTIFIER
# ==========================================

def Identifier():
    print_rule("<Identifier> -> id")

    if current_token[0] == 'IDENTIFIER':
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

    elif current_token[1] in ['==', '!=', '<', '>', '<=', '>=']:
        print_rule("<Expression Prime> -> <RelOp> <Term> <Expression Prime>")
        RelOp()
        Term()
        ExpressionPrime()

    else:
        print_rule("<Expression Prime> -> ε")


# ==========================================
# RELOP
# ==========================================

def RelOp():
    if current_token[1] in ['==', '!=', '<', '>', '<=', '>=']:
        print_rule(f"<RelOp> -> {current_token[1]}")
        next_token()
    else:
        error("Relational Operator")


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
# FACTOR
# ==========================================

def Factor():
    if current_token[0] == 'IDENTIFIER':
        print_rule("<Factor> -> <Identifier>")
        Identifier()

    elif current_token[0] == 'INTEGER':
        print_rule("<Factor> -> <Integer>")
        next_token()

    elif current_token[0] == 'REAL':
        print_rule("<Factor> -> <Real>")
        next_token()

    elif current_token[1] == '(':
        print_rule("<Factor> -> ( <Expression> )")
        next_token()
        Expression()

        if current_token[1] == ')':
            next_token()
        else:
            error(")")

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