import random


HEIGHT = 10
WIDTH = 10
NUMSTATES = 5



class Program(object):
    def __init__(self):
        self.rules = {}

    def __repr__(self):
        unsortedKeys = list(self.rules.keys())
        sortedKeys = sorted(unsortedKeys)
        # outLines = [str(i[0]) + " " + i[0] + " -> " + \
        #     self.rules[i][0] + " " + str(self.rules[i][1]) \
        #     for i in sortedKeys]
        fullSt = ""
        for i in sortedKeys:
            fullSt = fullSt + str(i[0]) + " " + str(i[1]) + " -> " + \
                self.rules[i][0] + " " + str(self.rules[i][1]) + '\n'
        return fullSt
        
    def randomize(self):
        """Sets self.rules to a random set of rules, encompassing all possible states, with no outputs."""
        # self.rules = {}
        for i in range(NUMSTATES):
            for mnorth in ["N", "x"]:
                for meast in ["E", "x"]:
                    for mwest in ["W", "x"]:
                        for msouth in ["S", "x"]:
                            tPossibilities = ["X"]
                            if mnorth == "x":
                                tPossibilities += ["N"]
                            if meast == "x":
                                tPossibilities += ["E"]
                            if mwest == "x":
                                tPossibilities += ["W"]
                            if msouth == "x":
                                tPossibilities += ["S"]
                            self.rules[(i, mnorth + meast + mwest + msouth)] = \
                                 (random.choice(tPossibilities), random.choice(range(NUMSTATES))) #This concatenates the 
            
    
    def getMove(self, state, surroundings):
        """Give the next move and state according to self.rules
        """
        return self.rules[(state, surroundings)]
    
    def mutate(self):
        """Change a random entry from self.rules and set to a different valid next move and state
        """
        changeKey = random.choice( list(self.rules.keys()))
        currentVal = self.rules[changeKey]
        tPossibilities = ["X"]
        if changeKey[1][0] == "x":
            tPossibilities += ["N"]
        if changeKey[1][1] == "x":
            tPossibilities += ["E"]
        if changeKey[1][2] == "x":
            tPossibilities += ["W"]
        if changeKey[1][3] == "x":
            tPossibilities += ["S"]
        
        t = currentVal
        while t == currentVal:
            t = (random.choice(tPossibilities), random.choice(range(NUMSTATES)))
        
        self.rules[changeKey] = t


    def __gt__(self, other):
        """Greater-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])
    

    

class World: #are the walls built in??
    def __init__(self, initial_row, initial_col, program):
        self.row = initial_row                                  # the current row in which Picobot is located (will change).
        self.col = initial_col                                  # the current column in which Picobot is located (will change).
        self.state = 0                                          # the current state for Picobot (will change).
        self.prog = program                                     # a list-of-lists that holds the 2D room in which Picobot is located (very similar to the C4 Board's self.data).
        self.room = [[' ']*WIDTH for row in range(HEIGHT)]      # an object of type Program that controls the Picobot simulation.
        self.room[initial_row][initial_col] = "P"
    
    def __repr__(self):
        """This method returns a string representation
           for an object of type World
        """
        nstring = ""
        nstring += " " + "-" * WIDTH + "\n"
        for row in range(HEIGHT):
            nstring += "|"
            for colv in range(WIDTH):
                nstring += self.room[row][colv]
            nstring += '|\n'
        nstring += " " + "-" * WIDTH
        return nstring

    def getCurrentSurroundings(self):
        """Gets current surroundings of Pico bot
        """
        # long, but most straightforward
        outstr = ""
        if self.row != 0:
            if self.room[self.row -1][self.col] == "+":
                outstr += "N"
            else:
                outstr += "x"
        else:
            outstr += "N"

        if self.col != (WIDTH - 1):
            if self.room[self.row][self.col +1] == "+":
                outstr += "E"
            else:
                outstr += "x"
        else:
            outstr += "E"
        
        if self.col != 0:
            if self.room[self.row][self.col - 1] == "+":
                outstr += "W"
            else:
                outstr += "x"
        else:
            outstr += "W"

        if self.row != (HEIGHT - 1):
            if self.room[self.row + 1][self.col] == "+":
                outstr += "S"
            else:
                outstr += "x"
        else:
            outstr += "S"

        return outstr


    def step (self): #optional later marker code here also 
        """Use current state and surrounding data to move the simlutaion forward one unit"""
        self.room[self.row][self.col] = "o"
        nextpos = self.prog.getMove(self.state, self.getCurrentSurroundings())
        self.state = nextpos[1]
        if nextpos[0] == "N":
            self.row -= 1
        if nextpos[0] == "E":
            self.col += 1
        if nextpos[0] == "W":
            self.col -= 1
        if nextpos[0] == "S":
            self.row += 1
        self.room[self.row][self.col] = "P"

    def run(self, steps):
        """Step the simulation steps times
        """
        for i in range(steps):
            self.step()

    def fractionVisitedCells(self):
        visited = 0
        freecells = 0
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.room[row][col] == "o":
                    visited += 1
                elif self.room[row][col] == " ":
                    freecells += 1
        return visited / (visited + freecells)
                