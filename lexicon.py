# ===================================================================================================
# FSM for identifiers
# l(l|d|_)*
# ===================================================================================================

# DFA table from FSM stored into Python dictionary
id_transitions = {
    'A': {'l': 'B', 'd': None, '_': None},
    'B': {'l': 'C', 'd': 'D', '_': 'E'},
    'C': {'l': 'C', 'd': 'D', '_': 'E'},
    'D': {'l': 'C', 'd': 'D', '_': 'E'},
    'E': {'l': 'C', 'd': 'D', '_': 'E'},
}

# !!! remember to add keywords as needed !!!
keywords = {'integer', 'if', 'otherwise', 'fi', 'else', 'while', 'for', 'return', 'read', 'write'}

# all states with state 11 in them (accepting states)
id_acceptingStates = {'B', 'C', 'D', 'E'}

startingState = 'A'

# function to determine char type (letter/digit/underscore)
def getCharType(c):

    if c.isalpha():
        return 'l'
    elif c.isdigit():
        return 'd'
    elif c == '_':
        return '_'
    
    # invalid char
    else:
        return None

# FSM function to determine if string is valid identifier
# read string, then check if identifier
def identifierFSM(s):

    state = startingState

    # go thru every char in string
    for char in s:

        # determine char type
        charType = getCharType(char)

        # error handling
        if charType is None:
            return False
        
        # move onto next state based on char type
        state = id_transitions[state].get(charType)

        # error handling
        if state is None:
            return False
    
    # check if final state is accepting state; return TRUE if so, FALSE if not
    return state in id_acceptingStates


# ===================================================================================================
# FSM for integers
# d+
# ===================================================================================================

int_transitions = {
    'A': {'d': 'B'},
    'B': {'d': 'B'},
}

int_acceptingStates = {'B'}

# FSM function to determine if string is valid integer
def integerFSM(s):

    # start from da beginning
    state = startingState

    # loop thru every char in string
    for char in s:
        
        # check if digit
        if char.isdigit():
            charType = 'd'
        else:
            charType = None

        # error handling
        if charType is None:
            return False

        # move onto next state based on char type
        state = int_transitions[state].get(charType)

        # error handling
        if state is None:
            return False

    # check if final state is accepting state; return TRUE if so, FALSE if not
    return state in int_acceptingStates


# ===================================================================================================
# FSM for real numbers
# d+ . d+
# ===================================================================================================

real_transitions = {
    'A': {'d': 'B', '.': None},
    'B': {'d': 'B', '.': 'C'},
    'C': {'d': 'D', '.': None},
    'D': {'d': 'D', '.': None},
}

real_acceptingStates = {'D'}

#function to determine char type for real numbers (digit or decimal point)
def realType(c):

    if c.isdigit():
        return 'd'
    elif c == '.':
        return '.'
    else:
        return None
    
# FSM function to determine if string is valid real number
def realFSM(s):

    # start from da beginning again
    state = startingState

    #loop thru every char in string
    for char in s:

        # get char type
        charType = realType(char)

        # error handling
        if charType is None:
            return False

        # move onto next state based on char type
        state = real_transitions[state].get(charType)

        # error handling
        if state is None:
            return False
    
    # check if final state is accepting state; return TRUE if so, FALSE if not
    return state in real_acceptingStates

# ===================================================================================================
# LEXER
# ===================================================================================================

# !!! remember to add operators/separators as needed !!!
operators = {'+', '-', '*', '/', '=', '<', '>'}
# need this bc operators have diff string sizes
operator2 = {'==', '!=', '<=', '>=', '&&', '||', '++', '--', '+=', '-=', '*=', '/='} 
separators = {'(', ')', '{', '}', '[', ']', ';', ','}

def lexer(file):

    tokens = []
    i = 0

    while i < len(file):

        # skip whitespace
        if file[i].isspace():
            i += 1

            # continue with papa loop
            continue
    
        # skip comments /* ... */
        if file[i:i+2] == '/*':

            # skip past /*
            i += 2

            # while comment is unfinished
            while file[i:i+2] != '*/':
                i += 1

            # skip past */
            i += 2

            # continue with papa loop
            continue

        # check for operators
        if file[i:i+2] in operator2:
            tokens.append(('OPERATOR', file[i:i+2]))
            i += 2

            # continue with papa loop
            continue

        if file[i] in operators:
            tokens.append(('OPERATOR', file[i]))
            i += 1

            # continue with papa loop
            continue

        # check for separators
        if file[i] in separators:
            tokens.append(('SEPARATOR', file[i]))
            i += 1

            # continue with papa loop
            continue

        # check for keywords/identifiers
        # nested loop prob to check ahead
        if file[i].isalpha():
            
            # look ahead!!
            j = i

            # while the next char is a letter/digit/underscore, run run run
            # also make sure we don't go out of bounds
            # STOP as soon as no longer in identifier char type. this way we don't have to depend on whitespace to separate tokens
            while j < len(file) and (file[j].isalpha() or file[j].isdigit() or file[j] == '_'):
                j += 1

            # slice out word from file
            # from i to just before j
            word = file[i:j]

            # run thru identifier FSM to make sure it's valid, then check if it's a keyword or identifier
            if identifierFSM(word):
                if word in keywords:
                    tokens.append(('KEYWORD', word))
                else:
                    tokens.append(('IDENTIFIER', word))

            # error handling
            else:
                tokens.append(('ERROR', word))
            
            # reset i to j to continue scanning from the end of the word
            i = j

            # continue with papa loop
            continue

        # check for integers/real numbers
        if file[i].isdigit():

            j = i

            # while the next char is a digit or decimal point, run run run
            # also make sure we don't go out of bounds
            # STOP as soon as no longer int/real. this way we don't have to depend on whitespace to separate tokens
            while j < len(file) and (file[j].isdigit() or file[j] == '.'):
                j += 1

            # slice out num from file
            # from i to just before j
            num = file[i:j]

            # check if real or integer
            if realFSM(num):
                tokens.append(('REAL', num))
            elif integerFSM(num):
                tokens.append(('INTEGER', num))

            # error handling
            else:
                tokens.append(('ERROR', num))
            
            # reset i to j to continue scanning from the end of the num
            i = j

            # continue with papa loop
            continue

        # check for invalid char
        tokens.append(('ERROR', file[i]))
        i += 1

    return tokens

# ===================================================================================================
# Printing all Tokens
# ===================================================================================================

# open file, read char
with open("test_files/test1.txt", "r") as f:
    file = f.read()

# run lexer!!!
tokens = lexer(file)

# print tokens
for token in tokens:
    print(token)

""" 
# write tokens to output file
with open("test1output.txt", "w") as out:
    for token in tokens:
        out.write(f"{token}\n")

"""
# yay!