'''

MaxConnect4Game.py contains the minmax, alpha beta, beta aplha and eval functions. it also contains all the required function to calculate the streak of a given function
'''
import copy # using deepcopy to copy the object
import random   # 
import sys  # importing all sys file

utilityVal = {}     # storing the utility val
infinity = float('inf')     # defining a infinite val

class MaxConnect4game:  # 
    def __init__(self): # intilising the function
        self.GameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentMove = 0
        self.pieceCount = 0
        self.player1Score = 0
        self.player2Score = 0
        self.gameFile = None
        self.computerColumn = None
        self.depth = 1

    def checkPieceCount(self):  # checking if count the number of piece already played
        self.pieceCount = sum(1 for row in self.GameBoard for piece in row if piece)

    def getPieceCount(self):    # returning the total piece of the borad which are occupied
        return sum(1 for row in self.GameBoard for piece in row if piece)

    def displayGB(self):    # function for diplaying the game borad
        print(' -----------------')
        for i in range(6):
            print(' |'),
            for j in range(7):
                print('%d' % int(self.GameBoard[i][j])),
            print('| ')
        print(' -----------------')

    def printGameBoardToFile(self): # function for printing the game borad to file
        for row in self.GameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r')
        self.gameFile.write('%s\r' % str(self.currentMove))

    def playPiece(self, column):    # function for placing the current player piece in the column
        if not self.GameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.GameBoard[i][column]:
                    self.GameBoard[i][column] = self.currentMove
                    self.pieceCount += 1
                    return 1

    def checkPiece(self, column, opponent):     # function for checking if the piece is valid or not
        if not self.GameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.GameBoard[i][column]:
                    self.GameBoard[i][column] = opponent
                    self.pieceCount += 1
                    return 1

    def maxVal(self, currentNode):  # function for resturing the state for the maximun value
        node = copy.deepcopy(currentNode)
        childNode = []
        for i in range(7):
            currentState = self.playPiece(i)
            if currentState != None:
                childNode.append(self.GameBoard)
                self.GameBoard = copy.deepcopy(node)
        return childNode

    def minVal(self, currentNode):  # function for returning the state for the minimun value
        node = copy.deepcopy(currentNode)
        if self.currentMove == 1:
            opponent = 2
        elif self.currentMove == 2:
            opponent = 1
        childNode = []
        for i in range(7):
            currentState = self.checkPiece(i, opponent)
            if currentState != None:
                childNode.append(self.GameBoard)
                self.GameBoard = copy.deepcopy(node)
        return childNode

    def alphaBeta(self, currentNode, alpha, beta, depth):   # function for alpha beta puring (max val)
        value = -infinity
        childNode = self.maxVal(currentNode)
        if childNode == [] or depth == 0:
            self.scoreCount()
            return self.evalCalc(self.GameBoard)
        else:
            for node in childNode:
                self.GameBoard = copy.deepcopy(node)
                value = max(value, self.betaAlpha(node, alpha, beta, depth - 1))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

    def betaAlpha(self,currentNode, alpha, beta, depth):    # function for beta alpha puring (min val)
        value = infinity
        childNode = self.minVal(currentNode)
        if childNode == [] or depth == 0:
            self.scoreCount()
            return self.evalCalc(self.GameBoard)
        else:
            for node in childNode:
                self.GameBoard = copy.deepcopy(node)
                value = min(value, self.alphaBeta(node, alpha, beta, depth - 1))
                if value <= alpha:
                    return value
                beta = min(beta, value)
        return value

    def minMax(self, depth):    # plain min max algorithm
        currentState = copy.deepcopy(self.GameBoard)
        for i in range(7):
            if self.playPiece(i) != None:
                if self.pieceCount == 42 or self.depth == 0:
                    self.GameBoard = copy.deepcopy(currentState)
                    return i
                else:
                    val = self.betaAlpha(self.GameBoard, -infinity, infinity, depth - 1)
                    utilityVal[i] = val
                    self.GameBoard = copy.deepcopy(currentState)
        maxUtilityVal = max([i for i in utilityVal.values()])
        for i in range(7):
            if i in utilityVal:
                if utilityVal[i] == maxUtilityVal:
                    utilityVal.clear()
                    return i

    def verticalCheck(self, row, column, state, streak):    # checking the vertical piece in the row
        consecutiveCount = 0
        for i in range(row, 6):
            if state[i][column] == state[row][column]:
                consecutiveCount += 1
            else:
                break
        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalCheck(self, row, column, state, streak):  # checking for the horizontal piece in the column
        count = 0
        for j in range(column, 7):
            if state[row][j] == state[row][column]:
                count += 1
            else:
                break
        if count >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, row, column, state, streak):    # checking for the diagonal check in the borad
        total = 0
        count = 0
        j = column
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        count = 0
        j = column
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j] == state[row][column]:
                count += 1
            else:
                break
            j += 1
        if count >= streak:
            total += 1
        return total

    def streakCalc(self, state, color, streak):     # function for checking which type of connectfour goes
        count = 0
        for i in range(6):
            for j in range(7):
                if state[i][j] == color:
                    count += self.verticalCheck(i, j, state, streak)
                    count += self.horizontalCheck(i, j, state, streak)
                    count += self.diagonalCheck(i, j, state, streak)
        return count

    def playerEvalCalc(self, state):    # calculating the streak for the non computer player
        playerFours = self.streakCalc(state, self.currentMove, 4)
        playerThrees = self.streakCalc(state, self.currentMove, 3)
        playerTwos = self.streakCalc(state, self.currentMove, 2)
        return (playerFours * 37044 + playerThrees * 882 + playerTwos * 21) # numbers are the permutation for each fours in a row, threes in a row and twos in a row

    def evalFunc(self): # function for the which next color is 
        if self.currentMove == 1:
            oneMoveColor = 2
        elif self.currentMove == 2:
            oneMoveColor = 1
        return oneMoveColor

    def compEvalCalc(self, state):  # calculating the streak for the computer
        oneMoveColor = self.evalFunc()
        compFours = self.streakCalc(state, oneMoveColor, 4)
        compThrees = self.streakCalc(state, oneMoveColor, 3)
        compTwos = self.streakCalc(state, oneMoveColor, 2)
        return (compFours * 37044 + compThrees * 882 + compTwos * 21)

    def evalCalc(self, state):  #function for calucating the difference in the steak of computer vs non computer
        return self.playerEvalCalc(state) - self.compEvalCalc(state)

    def changeMove(self):   # function for changing to next player 
        if self.currentMove == 1:
            self.currentMove = 2
        elif self.currentMove == 2:
            self.currentMove = 1

    def aiPlay(self):   # function for computing the computer move
        randomCol = self.minMax(int(self.depth))
        result = self.playPiece(randomCol)
        if not result:
            print('No Result')
        else:
            print('Player: %d, Column: %d\n' % (self.currentMove, randomCol + 1))
            self.changeMove()

    def scoreCount(self):   # function for returning the score count i.e. fours in a row
        self.player1Score = 0;
        self.player2Score = 0;
        # Check horizontally
        for row in self.GameBoard:
            # Check player 1
            if row[0:4] == [1] * 4:
                self.player1Score += 1
            if row[1:5] == [1] * 4:
                self.player1Score += 1
            if row[2:6] == [1] * 4:
                self.player1Score += 1
            if row[3:7] == [1] * 4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2] * 4:
                self.player2Score += 1
            if row[1:5] == [2] * 4:
                self.player2Score += 1
            if row[2:6] == [2] * 4:
                self.player2Score += 1
            if row[3:7] == [2] * 4:
                self.player2Score += 1
        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.GameBoard[0][j] == 1 and self.GameBoard[1][j] == 1 and
                    self.GameBoard[2][j] == 1 and self.GameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.GameBoard[1][j] == 1 and self.GameBoard[2][j] == 1 and
                    self.GameBoard[3][j] == 1 and self.GameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.GameBoard[2][j] == 1 and self.GameBoard[3][j] == 1 and
                    self.GameBoard[4][j] == 1 and self.GameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.GameBoard[0][j] == 2 and self.GameBoard[1][j] == 2 and
                    self.GameBoard[2][j] == 2 and self.GameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.GameBoard[1][j] == 2 and self.GameBoard[2][j] == 2 and
                    self.GameBoard[3][j] == 2 and self.GameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.GameBoard[2][j] == 2 and self.GameBoard[3][j] == 2 and
                    self.GameBoard[4][j] == 2 and self.GameBoard[5][j] == 2):
                self.player2Score += 1
        # Check diagonally
        # Check player 1
        if (self.GameBoard[2][0] == 1 and self.GameBoard[3][1] == 1 and
                self.GameBoard[4][2] == 1 and self.GameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.GameBoard[1][0] == 1 and self.GameBoard[2][1] == 1 and
                self.GameBoard[3][2] == 1 and self.GameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.GameBoard[2][1] == 1 and self.GameBoard[3][2] == 1 and
                self.GameBoard[4][3] == 1 and self.GameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.GameBoard[0][0] == 1 and self.GameBoard[1][1] == 1 and
                self.GameBoard[2][2] == 1 and self.GameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.GameBoard[1][1] == 1 and self.GameBoard[2][2] == 1 and
                self.GameBoard[3][3] == 1 and self.GameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.GameBoard[2][2] == 1 and self.GameBoard[3][3] == 1 and
                self.GameBoard[4][4] == 1 and self.GameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.GameBoard[0][1] == 1 and self.GameBoard[1][2] == 1 and
                self.GameBoard[2][3] == 1 and self.GameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.GameBoard[1][2] == 1 and self.GameBoard[2][3] == 1 and
                self.GameBoard[3][4] == 1 and self.GameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.GameBoard[2][3] == 1 and self.GameBoard[3][4] == 1 and
                self.GameBoard[4][5] == 1 and self.GameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.GameBoard[0][2] == 1 and self.GameBoard[1][3] == 1 and
                self.GameBoard[2][4] == 1 and self.GameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.GameBoard[1][3] == 1 and self.GameBoard[2][4] == 1 and
                self.GameBoard[3][5] == 1 and self.GameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.GameBoard[0][3] == 1 and self.GameBoard[1][4] == 1 and
                self.GameBoard[2][5] == 1 and self.GameBoard[3][6] == 1):
            self.player1Score += 1
        if (self.GameBoard[0][3] == 1 and self.GameBoard[1][2] == 1 and
                self.GameBoard[2][1] == 1 and self.GameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.GameBoard[0][4] == 1 and self.GameBoard[1][3] == 1 and
                self.GameBoard[2][2] == 1 and self.GameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.GameBoard[1][3] == 1 and self.GameBoard[2][2] == 1 and
                self.GameBoard[3][1] == 1 and self.GameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.GameBoard[0][5] == 1 and self.GameBoard[1][4] == 1 and
                self.GameBoard[2][3] == 1 and self.GameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.GameBoard[1][4] == 1 and self.GameBoard[2][3] == 1 and
                self.GameBoard[3][2] == 1 and self.GameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.GameBoard[2][3] == 1 and self.GameBoard[3][2] == 1 and
                self.GameBoard[4][1] == 1 and self.GameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.GameBoard[0][6] == 1 and self.GameBoard[1][5] == 1 and
                self.GameBoard[2][4] == 1 and self.GameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.GameBoard[1][5] == 1 and self.GameBoard[2][4] == 1 and
                self.GameBoard[3][3] == 1 and self.GameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.GameBoard[2][4] == 1 and self.GameBoard[3][3] == 1 and
                self.GameBoard[4][2] == 1 and self.GameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.GameBoard[1][6] == 1 and self.GameBoard[2][5] == 1 and
                self.GameBoard[3][4] == 1 and self.GameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.GameBoard[2][5] == 1 and self.GameBoard[3][4] == 1 and
                self.GameBoard[4][3] == 1 and self.GameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.GameBoard[2][6] == 1 and self.GameBoard[3][5] == 1 and
                self.GameBoard[4][4] == 1 and self.GameBoard[5][3] == 1):
            self.player1Score += 1
        # Check player 2
        if (self.GameBoard[2][0] == 2 and self.GameBoard[3][1] == 2 and
                self.GameBoard[4][2] == 2 and self.GameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.GameBoard[1][0] == 2 and self.GameBoard[2][1] == 2 and
                self.GameBoard[3][2] == 2 and self.GameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.GameBoard[2][1] == 2 and self.GameBoard[3][2] == 2 and
                self.GameBoard[4][3] == 2 and self.GameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.GameBoard[0][0] == 2 and self.GameBoard[1][1] == 2 and
                self.GameBoard[2][2] == 2 and self.GameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.GameBoard[1][1] == 2 and self.GameBoard[2][2] == 2 and
                self.GameBoard[3][3] == 2 and self.GameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.GameBoard[2][2] == 2 and self.GameBoard[3][3] == 2 and
                self.GameBoard[4][4] == 2 and self.GameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.GameBoard[0][1] == 2 and self.GameBoard[1][2] == 2 and
                self.GameBoard[2][3] == 2 and self.GameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.GameBoard[1][2] == 2 and self.GameBoard[2][3] == 2 and
                self.GameBoard[3][4] == 2 and self.GameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.GameBoard[2][3] == 2 and self.GameBoard[3][4] == 2 and
                self.GameBoard[4][5] == 2 and self.GameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.GameBoard[0][2] == 2 and self.GameBoard[1][3] == 2 and
                self.GameBoard[2][4] == 2 and self.GameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.GameBoard[1][3] == 2 and self.GameBoard[2][4] == 2 and
                self.GameBoard[3][5] == 2 and self.GameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.GameBoard[0][3] == 2 and self.GameBoard[1][4] == 2 and
                self.GameBoard[2][5] == 2 and self.GameBoard[3][6] == 2):
            self.player2Score += 1
        if (self.GameBoard[0][3] == 2 and self.GameBoard[1][2] == 2 and
                self.GameBoard[2][1] == 2 and self.GameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.GameBoard[0][4] == 2 and self.GameBoard[1][3] == 2 and
                self.GameBoard[2][2] == 2 and self.GameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.GameBoard[1][3] == 2 and self.GameBoard[2][2] == 2 and
                self.GameBoard[3][1] == 2 and self.GameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.GameBoard[0][5] == 2 and self.GameBoard[1][4] == 2 and
                self.GameBoard[2][3] == 2 and self.GameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.GameBoard[1][4] == 2 and self.GameBoard[2][3] == 2 and
                self.GameBoard[3][2] == 2 and self.GameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.GameBoard[2][3] == 2 and self.GameBoard[3][2] == 2 and
                self.GameBoard[4][1] == 2 and self.GameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.GameBoard[0][6] == 2 and self.GameBoard[1][5] == 2 and
                self.GameBoard[2][4] == 2 and self.GameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.GameBoard[1][5] == 2 and self.GameBoard[2][4] == 2 and
                self.GameBoard[3][3] == 2 and self.GameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.GameBoard[2][4] == 2 and self.GameBoard[3][3] == 2 and
                self.GameBoard[4][2] == 2 and self.GameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.GameBoard[1][6] == 2 and self.GameBoard[2][5] == 2 and
                self.GameBoard[3][4] == 2 and self.GameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.GameBoard[2][5] == 2 and self.GameBoard[3][4] == 2 and
                self.GameBoard[4][3] == 2 and self.GameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.GameBoard[2][6] == 2 and self.GameBoard[3][5] == 2 and
                self.GameBoard[4][4] == 2 and self.GameBoard[5][3] == 2):
            self.player2Score += 1