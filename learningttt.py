"""
first set up a table of numbers. - for each possible state of the game.
each number is the latest probability of winning.
    this estimate = state's VALUE
    whole table = LEARNED VALUE FUNCTION

[
if X wins: prob =1
if O wins: prob =0
else: prob = .5
]

when play game, we find all possible states
and their current value of winning.
usually, select move w greatest value. (GREEDY)
occasionally, must select randomly. (EXPLATORY)

how to change values:
make them more accurate
back up value of state after greedy move to the state before
the move.
    how? move the earlier state's value a fraction of the way
    toward later state's value.

[
S1 = earlier state's value
S2 = later state's value
a = step-size parameter

S1 = S1 + a(S2-S1)
]

if the stepsize parameter is reduced over time (properly)
this will work nicely.

"""
from random import*



class Comp:
    def __init__(self,player):
        self.statesdict = {}
        self.player = player
        self.stepsize = 0.9
        
    def explore(self,S):
        legal = legalMoves(S)
        move = None
        while move not in legal:
            move = randrange(0,8)
        return move
    def lookup(self, S):
        if S not in self.statesdict:
            self.statesdict[S] = 0.5
        return self.statesdict[S]
    def greedy(self, S):
        children = legalMoves(S)
        maxval = 0
        move = children[0]
        if self.player == 'X':
            maxval = -1
            for i in children:
                S[i] = self.player
                val = self.lookup(self.statetuple(S))
                S[i] = ' '
                if val > maxval:
                    maxval = val
                    move = i
        if self.player == 'O':
            maxval = -1
            for i in children:
                S[i] = self.player
                val = self.lookup(self.statetuple(S))
                S[i] = ' '
                if val < maxval:
                    maxval = val
                    move = i
        self.backup(maxval,S)
        return move
    def backup(self,nextval,S):
        self.prevstate = self.statetuple(S)
        self.prevscore = self.lookup(self.statetuple(S)) 
        if self.prevstate != None:
            self.statesdict[self.prevstate] += self.stepsize * (nextval - self.prevscore)
    def statetuple(self,S):
        return tuple(S[0]), tuple(S[1]),tuple(S[2]), tuple(S[3]),tuple(S[4]),tuple(S[5]), tuple(S[6]),tuple(S[7]),tuple(S[8])            
        
    
        


        
def board(state):
    # given state as a list, this will print out the current state of the board
    print("-------")
    print("|{0}|{1}|{2}|".format(state[0],state[1],state[2]))
    print("-------")
    print("|{0}|{1}|{2}|".format(state[3],state[4],state[5]))
    print("-------")
    print("|{0}|{1}|{2}|".format(state[6],state[7],state[8]))
    print("-------")
    
def printIntro():
    print("Welcome to tic-tac-toe. Player A is X and Player B is O.")
    print("You may choose from 3 modes: 0-player, 1-player, or 2-player.")
    print("You will pick a square using the board's coordinates.")
    print("You may choose an initial state for the game.") 
    print("The top left corner is (0,0) and the bottom right corner is (2,2)")
    


    
def legalMoves(state):
    # this creates a list of legal moves that can be made
    # ie. we create a list of board positions that are free
    moves = []
    for i in range(9):
        if state[i] == ' ':
            moves.append(i)
    return moves

def legitMoveP(state):
    legal = legalMoves(state)
    #this fx will check if the move that a human player has picked is in legal moves
    move = None
    while move not in legal:
        move = input("Which square will you pick?")
        move = convertCoord(move)
        if move not in legal:
            print("That square is occupied. Choose another.")
    return move



def getInputs():
    mode = input("Let's begin. Do you want to play the game in 0-player, 1-player, or 2-player mode? (Type in 0,1, or 2): ")
    if mode == "0":
        playerA, playerB = "c", "c"
        return playerA, playerB
    if mode == "1":
        playerA, playerB = "h", "c"
        return playerA, playerB
    if mode == "2":
        playerA, playerB = "h", "h"
        return playerA, playerB
    
def switchP(player):# switch players 
    if player == 'X':
        return 'O'            
    return 'X'
def playAgain():
    x = input("Play again? (y or n): ")
    return x

def main(): # I wasn't sure how to make it loop. it only repeats the game
    #if user puts "y" when prompted by playAgain() 
    printIntro()
    playerA,playerB = getInputs()
    s1,s2,s3,s4,s5,s6,s7,s8,s9 = input("What is the initial state of the board? (Enter without spaces. eg, XOX OX0 0X): ")
    state = [s1,s2,s3,s4,s5,s6,s7,s8,s9]

    
    legal = legalMoves(state)
    #game continues as long as nobody has won or tied 
    x = "y"
    statesX = Comp('X')
    statesO = Comp('O')

    while x == "y":
        while not (win(state,'X') or win(state,'O') or tie(state)):
            turn = "A"
            
            #player a goes first 
            if turn == "A":

                board(state)
                print("It's Player A's turn.")
                if playerA == "c":
                    
                    x = randrange(0,101)
                    if x <75:
                        move = statesX.greedy(state)
                    else:
                        move = statesX.explore(state) 
                if playerA == "h":
                    move = legitMoveP(state) 
                state[move] = 'X'
                turn = "B"
                if win(state,'X') == True:
                    board(state)
                    print("Congrats, Player A has won!")
                    givestates(playerA,playerB,statesX,statesO)
                    x = playAgain()
                    state = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
                    turn = "A"
                    
                if win(state,'O') == True:
                    board(state)
                    print( "Congrats, Player B has won!")
                    givestates(playerA,playerB,statesX,statesO)
                    x= playAgain()
                    state = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
                    turn = "A"
                if (tie(state) == True) and not(win(state,'X') or win(state,'O')):
                    board(state)
                    print( "It's a tie."  )
                    givestates(playerA,playerB,statesX,statesO)
                    x= playAgain()
                    state = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
                    turn = "A"
                    
                # assign turn to "B", and this goes back and forth  to switch turns
            if turn == "B":
                board(state)
                print("It's Player B's turn.")
                if playerB == "c":
                    x = randrange(0,101)
                    if x <75:
                        move = statesO.greedy(state)
                    else:
                        move = statesO.explore(state) 
                if playerB == "h":
                    move = legitMoveP(state) 
                state[move] = 'O'
                turn = "A"
                if win(state,'X') == True:
                    board(state)
                    print("Congrats, Player A has won!")
                    givestates(playerA,playerB,statesX,statesO)
                    x= playAgain()
                    state = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
                if win(state,'O') == True:
                    board(state)
                    print( "Congrats, Player B has won!")
                    givestates(playerA,playerB,statesX,statesO)
                    x= playAgain()
                    state = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
                if (tie(state) == True) and not(win(state,'X') or win(state,'O')):
                    board(state)
                    print("It's a tie.")
                    givestates(playerA,playerB,statesX,statesO)
                    x= playAgain()
                    state = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
                    
def givestates(playerA,playerB,statesX,statesO):
    if playerA == "c":
        print(statesX.statesdict)
    if playerB =="c":
        print(statesO.statesdict)
        
def convertCoord(move):
    # converts the given coordinates to the board position 
    if move == '(0,0)': move = 0
    if move == '(0,1)': move = 1
    if move == '(0,2)': move = 2
    if move == '(1,0)': move = 3
    if move == '(1,1)': move = 4
    if move == '(1,2)': move = 5
    if move == '(2,0)': move = 6
    if move == '(2,1)': move = 7
    if move == '(2,2)': move = 8
    return move

def convertCoordFromInt(move):
    # converts the given coordinates to the board position 
    if move == 0: move = '(0,0)'
    if move == 1: move = '(0,1)'
    if move == 2: move = '(0,2)'
    if move == 3: move = '(1,0)'
    if move == 4: move = '(1,1)'
    if move == 5: move = '(1,2)'
    if move == 6: move = '(2,0)'
    if move == 7: move = '(2,1)'
    if move == 8: move = '(2,2)'
    return move

def tie(state):
    count = 0
    #game tied if all spaces are filled
    #state is a list 
    for i in state:
        if i == 'X' or i=='O':
            count = count + 1
    if count == 9:
        return True
    else: return False
    
def win(s,p):
    # s is state, p is player
    # checking for winning state
    if ( (s[6] == p and s[7] == p and s[8] == p)or
    (s[3] == p and s[4] == p and s[5] == p)or
    (s[0] == p and s[1] == p and s[2] == p)or
    (s[6] == p and s[3] == p and s[0] == p)or
    (s[7] == p and s[4] == p and s[1] == p)or
    (s[8] == p and s[5] == p and s[2] == p)or
    (s[0] == p and s[4] == p and s[8] == p)or
    (s[2] == p and s[4] == p and s[6] == p)):
        return True
    else: return False


