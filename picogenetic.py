import random
from copy import deepcopy


HEIGHT = 25
WIDTH = 25
NUMSTATES = 5

KEEPDATA = [["+"] * WIDTH] + [["+"] + [" "]*(WIDTH -2) + ["+"] for row in range(HEIGHT-2)] + [["+"] * WIDTH] 


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
    
    def crossover(self,other):
        """Returns new program with some fraction of rules in each state from each parent. Both parents must have a full rulebook of keys"""
        crossoverstate = random.randint(0,3)
        statebreakindex = int(round(NUMSTATES * crossoverstate / 3))
        #This approach is strange
        newset = dict()
        for key in self.rules:
            if key[0] <= statebreakindex:
                newset[key] = self.rules[key]
            else:
                newset[key] = other.rules[key]
        newprog = Program()
        newprog.rules = newset
        return newprog



    def __gt__(self, other):
        """Greater-than operator -- works randomly, but works!"""
        return random.choice([True, False])

    def __lt__(self, other):
        """Less-than operator -- works randomly, but works!"""
        return random.choice([True, False])
    
    def working(self):
        """
        This method will set the current program (self) to a working
        room-clearing program. This is super-useful to make sure that
        methods such as step, run, and evaluateFitness are working!
        """
        POSSIBLE_SURROUNDINGS = ["NExx", "NxWx", "Nxxx", "xExS",
         "xExx", "xxWS", "xxWx", "xxxS", "xxxx"]
        POSSIBLE_MOVES = ['N', 'E', 'W', 'S']
        POSSIBLE_STATES = [0, 1, 2, 3, 4]
        for st in POSSIBLE_STATES:
            for surr in POSSIBLE_SURROUNDINGS:
                if st == 0 and ('N' not in surr):   val = ('N', 0)
                elif st == 0 and ('W' in surr):     val = ('E', 2)
                elif st == 0:                       val = ('W', 1)
                elif st == 1 and ('S' not in surr): val = ('S', 1)
                elif st == 1 and ('W' in surr):     val = ('E', 2)
                elif st == 1:                       val = ('W', 0)
                elif st == 2 and ('E' not in surr): val = ('E', 2)
                elif st == 2 and ('N' in surr):     val = ('S', 1)
                elif st == 2:                       val = ('N', 0)
                else:
                    stepdir = surr[0]
                    while stepdir in surr:
                        stepdir = random.choice(POSSIBLE_MOVES)
                    val = (stepdir, st)  # keep the same state
                self.rules[(st, surr)] = val

    

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
        if type(self.prog) != Program:
            print("j")
            print(self.prog)
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
        """Return fraction of all cells not containing a wall that picobot has been to"""
        visited = 0
        freecells = 0
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.room[row][col] == "o":
                    visited += 1
                elif self.room[row][col] == " ":
                    freecells += 1
        return visited / (visited + freecells)


    def setRoom(self, data):
        assert len(data) == len(self.room)
        assert len(data[0]) == len(self.room[0])
        # assert data[self.row][self.col] != "+"
        if data[self.row][self.col] == "+":
            trow = random.randint(0, HEIGHT -1)
            tcol = random.randint(0, WIDTH -1)
            while data[trow][tcol] == "+":
                trow = random.randint(0, HEIGHT -1)
                tcol = random.randint(0, WIDTH -1)
            self.col = tcol
            self.row = trow
        self.room = deepcopy(data) #Deepcopy is what keeps everything from breaking
        self.room[self.row][self.col] = "P"
                


def genPopulation(size):
    """Returns list of randomized picobot Programs of size size."""
    t = []
    for i in range(size):
        t += [Program()]
        t[i].randomize()
    return t


def evaluateFitness(program, trials, steps):
    amountcovered = []
    for i in range(trials):
        scol = random.randint(0,WIDTH-1) 
        srow = random.randint(0,HEIGHT-1)
        tworld = World(srow, scol, program)
        tworld.setRoom(KEEPDATA)  #Important!!
        tworld.run(steps)
        amountcovered += [tworld.fractionVisitedCells()]
    return sum(amountcovered)/len(amountcovered)

USESTEPS = 1000
USETRIALS = 42
FRACTOKEEP = .1
MUTATEPROB = .5

def averager(nlist):
    """Return average fitness from list of fitnesses"""
    h = 0
    for i in range(len(nlist)):
        h += nlist[i][0]
    return h/len(nlist)

def expandTopPopulation(slist):
    toptoKeep = []
    for entry in range(round(len(slist) *FRACTOKEEP)):
        toptoKeep += [slist[entry][1]]
    newpop = toptoKeep # note the keeping of the parent population

    while len(newpop) < len(slist):
        first = toptoKeep[random.randint(0,len(toptoKeep)-1)] 
        second = toptoKeep[random.randint(0,len(toptoKeep)-1)]
        toAdd = first.crossover(second)
        if random.random() < MUTATEPROB: # note only children mutate, is that bad?
            toAdd.mutate()
        newpop += [toAdd]
    return newpop

    


    


def GA(popsize, numgens):
    print("Fitness is measured using " + str(USETRIALS) + " random trials and running for "+ str(USESTEPS) + " steps per trial:")
    cprogs = genPopulation(popsize)
    assert (FRACTOKEEP * popsize ) >= 1
    for i in range(numgens):
        print()
        print("Generation " + str(i))
        fitnesses = []
        for p in cprogs:
            fitnesses += [(evaluateFitness(p, USETRIALS, USESTEPS), p)]
        SLfit = sorted(fitnesses, reverse=True)
        print("Average fitness:  " + str(averager(SLfit)))
        print("Best fitness:  " + str(SLfit[0][0]))
        cprogs =  expandTopPopulation(SLfit)
    
    print("Best Picobot program:")
    print(SLfit[0][1])


        







        








