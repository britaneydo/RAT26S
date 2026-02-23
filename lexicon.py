# class definition for NFSM
""" class FSM:

    #CSTR
    def __init__(self):

        # dictionary for transitions
        # edit with (add_transitions()), ()
        self.transitions = {}
        
        # epsilon transitions
        self.epsilon = {}

        # machine starting state
        self.start = None

        # machine accepting state
        self.accept = None

    # s1 --symbol--> s2
    def Add_Transition(self, s1, symbol, s2):

        # input symbol; (s1 --symbol--> s2) if possible
        # if this symbol does not exist, create it, along with its empty set
        # two layer set (nested dictionary), same symbol can result in different output states
        self.transitions.setdefault(s1, {}).setdefault(symbol, set()).add(s2)
    
    # s1 --> s2
    def Add_Epsilon(self, s1, s2):

        # one layer set since epsilon is essentially no input
        self.epsilon.setdefault(s1, set()).add(s2)
    
    def Epsilon_Closure(machine, states):
        

 """



# =========================================================

# DFA table from FSM stored into Python dictionary
transitions = {
    'A': {'l': 'B', 'd': None, '_': None},
    'B': {'l': 'C', 'd': 'D', '_': 'E'},
    'C': {'l': 'C', 'd': 'D', '_': 'E'},
    'D': {'l': 'C', 'd': 'D', '_': 'E'},
    'E': {'l': 'C', 'd': 'D', '_': 'E'},
}

# all states with state 11 in them (accepting states)
acceptingStates = {'B', 'C', 'D', 'E'}

startingState = 'A'

# !!! remember to add keywords as needed !!!
keywords = {'integer', 'if', 'otherwise', 'fi', 'else', 'while', 'for', 'return', 'read', 'write'}

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
def FSM(s):

    state = startingState

    # go thru every char in string
    for char in s:

        # determine char type
        charType = getCharType(char)

        # error handling
        if charType is None:
            return False
        
        # move onto next state based on char type
        state = transitions[state].get(charType)

        # error handling
        if state is None:
            return False
    
    # check if final state is accepting state, return
    return state in acceptingStates



















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
