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

# !!! remember to add keywords/operators/separators as needed !!!
keywords = {'integer', 'if', 'otherwise', 'fi', 'else', 'while', 'for', 'return', 'read', 'write'}
operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
separators = {'(', ')', '{', '}', '[', ']', ';', ','}

# implement lexer here... tired...



















# =========================================================

# open file, read char
with open("test.txt", "r") as file:

    while True:
        c = file.read(1)

        # EOF handler
        if not c:
            break

        # can add repr before (c) if want clearer representation
        # delete this line once code is finished
        print((c), end = '')
