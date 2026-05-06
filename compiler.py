# ============================================================================================
# compiler.py | assignment 3
# Symbol table handling and generating an assembly code for the simplified version of Rat26S.
# ============================================================================================

import sys
from lexicon import lexer

# ===============================================================================
# Data Structure(s)
# ===============================================================================
class Instruction:
    def __init__(self, address, op, operand=None):
        self.address = address #ex: 1, 2, 3
        self.op = op #ex: "POPM", "PUSHM"
        self.operand = operand #memory address or None

# ===============================================================================
# Global Variables
# ===============================================================================
sym_table = {}
next_mem = 10000
instr_table = [] #Assembly instructions array
instr_address = 1
jump_stack = [] #For backpatching (JMPZ)
tokens = []
pos = 0
current_token = ("", "")

# ===============================================================================
# Symbol Table
# ===============================================================================
def insert(lexeme):
    global next_mem
    if lexeme in sym_table:
        print(f"Error: Identifier '{lexeme}' already declared.")
        sys.exit(1)

    sym_table[lexeme] = next_mem
    next_mem += 1

def get_Address(lexeme):
    if lexeme not in sym_table:
        print(f"Error: Undeclared identifier '{lexeme}'.")
        sys.exit(1)

    return sym_table[lexeme]

# ===============================================================================
# Token Handling
# ===============================================================================
def next_token():
    global pos, current_token
    if pos < len(tokens):
        current_token = tokens[pos]
        pos += 1
    else:
        current_token = ("EOF", "EOF")  # End of file token

# ===============================================================================
# Parsing Functions
# ===============================================================================
def A():
    #A -> id = E;
    if current_token[0] == "IDENTIFIER":
        save = current_token[1] #Save the identifier
        next_token()

        if current_token[1] == "=":
            next_token()
            E()

            generate_instruction("POPM", get_Address(save))
        else:
            print("Error: Expected '='.")
            sys.exit(1)
    else:
        print("Error: Expected identifier.")
        sys.exit(1)

def E():
    #E -> T E'
    T()
    E_prime()

def E_prime():
    #E' -> + T E' | ε
    if current_token[1] == "+":
        next_token()
        T()
        #Addition instruction
        generate_instruction("A") #generate_instruction not expecting 'nil' due to operand assignment defaulted to None
        E_prime()
    elif current_token[1] == "-":
        next_token()
        T()
        #Subtraction instruction
        generate_instruction("S")
        E_prime()

def T():
    #T -> F T'
    F()
    T_prime()

def T_prime():
    #T' -> * F T' | ε
    if current_token[1] == "*":
        next_token()
        F()
        #Multiplication instruction
        generate_instruction("M")
        T_prime()
    elif current_token[1] == "/":
        next_token()
        F()
        #Division instruction
        generate_instruction("D")
        T_prime()

def F():
    #F -> id
    if current_token[0] == "IDENTIFIER":
        generate_instruction("PUSHM", get_Address(current_token[1]))
        next_token()
    elif current_token[0] == "INTEGER":
        generate_instruction("PUSHI", int(current_token[1]))
        next_token()
    elif current_token[1] == "(":
        next_token()
        E()

        if current_token[1] == ")":
            next_token()
        else:
            print("Error: Expected ')'.")
            sys.exit(1) 
    else:
        print(f"Error: Expected in factor: {current_token[1]}")
        sys.exit(1)

def generate_instruction(op, operand=None):
    #Code Generation function for instructions
    global instr_address
    instr_table.append(Instruction(instr_address, op, operand))
    instr_address += 1

def while_statement():
    if current_token[1] == "while":
        next_token()

        Ar = instr_address #Address of the first instruction in the while loop condition
        generate_instruction("LABEL")

        if current_token[1] == "(":
            next_token()

            C()

            if current_token[1] == ")":
                next_token()
                S()

                generate_instruction("JMP", Ar) #Jump back to the beginning of the while loop condition
                back_patch(instr_address)
            else:
                print("Error: Expected ')'.")
                sys.exit(1)
        else:
            print("Error: Expected '('.")
            sys.exit(1)
    else:
        print("Error: Expected 'while' keyword.")
        sys.exit(1)

def C():
    E()
    op = current_token[1] #operator
    next_token()

    E()

    if op == "<": generate_instruction("LES")
    elif op == ">": generate_instruction("GRT")
    elif op == "==": generate_instruction("EQU")
    elif op == "!=": generate_instruction("NEQ")
    elif op == "<=": generate_instruction("LEQ")
    elif op == ">=": generate_instruction("GEQ")
    
    generate_instruction("JMPZ", None) #Jump to be backpatched
    jump_stack.append(instr_address - 1) #Push the address of the JMPZ instruction onto the jump stack for backpatching

def back_patch(jmp_address):
    addr = jump_stack.pop() #Pop the address of the JMPZ instruction from the jump stack
    instr_table[addr - 1].operand = jmp_address #Backpatch the JMPZ instruction with the correct jump address

def I():
    #I -> if ( C ) S fi
    if current_token[1] == "if":
        next_token()
        if current_token[1] == "(":
            next_token()
            C()

            if current_token[1] == ")":
                next_token()
                S()

                back_patch(instr_address)

                if current_token[1] == "fi":
                    next_token()
                else:
                    print("Error: Expected 'fi'.")
                    sys.exit(1)
            else:
                print("Error: Expected ')'.")
                sys.exit(1)
        else:
            print("Error: Expected '('.")
            sys.exit(1)
    else:
        print("Error: Expected 'if' keyword.")
        sys.exit(1)

def S():
    if current_token[0] == "IDENTIFIER":
        A()
    elif current_token[1] == "while":
        while_statement()
    elif current_token[1] == "read":
        scan()
    elif current_token[1] == "write":
        print_statement()
    elif current_token[1] == "{":
        compound()
    elif current_token[1] == "if":
        I()
    else:
        next_token() #Skip unrecognized tokens


def compound():
    #compound -> { <statement list> }
    if current_token[1] == "{":
        next_token()

        while current_token[1] != "}" and current_token[0] != "EOF":
            S()

        if current_token[1] == "}":
            next_token()
        else:
            print("Error: Expected '}'.")
            sys.exit(1)

def print_statement():
    next_token() #consume 'write'

    if current_token[1] == "(":
        next_token()

        E()

        generate_instruction("SOUT")

        if current_token[1] == ")":
            next_token()
            if current_token[1] == ";":
                next_token()
            else:
                print("Error: Expected ';' after ')'.")
                sys.exit(1)
        else:
            print("Error: Expected ')' after expression.")
            sys.exit(1)

def scan():
    next_token() #consume 'read'

    if current_token[1] == "(":
        next_token()

        id_name = current_token[1]

        generate_instruction("SIN")
        generate_instruction("POPM", get_Address(id_name))
        next_token()

        if current_token[1] == ")":
            next_token()
            if current_token[1] == ";":
                next_token()
            else:
                print("Error: Expected ';' after ')'.")
                sys.exit(1)
        else:
            print("Error: Expected ')' after identifier.")
            sys.exit(1)

def program():
    #Controls the flow of the program
    while current_token[1] == "@":
        next_token()

    while current_token[1] == "function":
        while current_token[1] != "@" and current_token[0] != "EOF":
            next_token() #Skip function definitions

        if current_token[1] == "@":
            next_token()

    #Declarations
    if current_token[1] == "integer":
        next_token()

        while current_token[1] != ";":
            if current_token[0] == "IDENTIFIER":
                insert(current_token[1]) #Insert identifier into symbol table
            next_token()
        next_token()

    if current_token[1] == "@":
        next_token()

    #Statements
    while current_token[0] != "EOF" and current_token[1] != "@":
        S()

    print_assembly()
    print_symbol_table()

def print_assembly():
    print("\nListing of Assembly Code:")
    for i in range(1, instr_address):
        instruction = instr_table[i - 1]
        print(f"{instruction.address:<6} {instruction.op:<10}", end="")

        if instruction.operand is not None:
            print(instruction.operand, end="")

        print() #New line after each instruction

def print_symbol_table():
    print("\nSymbol Table:")
    print("Identifier   Memory Location      Type")
    for lex in sorted(sym_table.keys()):
        print(f"{lex:<12} {sym_table[lex]:<12}      integer")

# ===================================================================================================
# Main Driver
# ===================================================================================================
def main():
        filename = "test_files/sample_code.txt"

        with open(filename, "r") as f:
            source = f.read()

        global tokens, pos
        tokens = lexer(source)
        pos = 0
        next_token()

        program()
        input("\nPress Enter to exit.")

if __name__ == "__main__":
    main()