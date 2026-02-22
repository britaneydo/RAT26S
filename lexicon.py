# class definition
class FSM:
    def __init__(self):

        # dictionary for transitions
        self.Transitions = {}

        # machine starting state
        self.StartingState = None







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
