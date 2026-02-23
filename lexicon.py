# class definition for NFSM
class FSM:
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
    
    def Add_Epsilon(self, s1, s2):

        # one layer set since epsilon is essentially no input
        self.epsilon.setdefault(s1, set()).add(s2)
    
# =========================================================

# testing code
transitions = {}
epsilon = {}









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
