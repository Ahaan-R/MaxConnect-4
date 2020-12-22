'''

Main file. It has the two mode; one-move mode and interactive mode. It calls the functions in the other py file MaxConnect4Game.py
'''
import sys  #importing all system file
from MaxConnect4Game import MaxConnect4game     #used for creating object of other file    

def humanPlay(GameBoard):       # human function taking the input and putting the element in it
    while GameBoard.getPieceCount() != 42:  # checking if the board is empty or not
        print(" Human's turn") 
        print(" ------- ----")
        UsersMove = int(input("Enter a column number (1-7): "))  # taking input which column number should be enter
        if not 0 < UsersMove < 8:    # checking if it is valid input or not
            print("Column invalid! Enter Again.")
            continue
        if not GameBoard.playPiece(UsersMove - 1):
            print("Column number: %d is full. Try other column." % UsersMove)
            continue
        print("Your made move: " + str(UsersMove))
        GameBoard.displayGB()   # displaying the game board
        GameBoard.gameFile = open("human.txt", 'w')  # displaying it in the txt file
        GameBoard.printGameBoardToFile()
        GameBoard.gameFile.close()  # file closing
        if GameBoard.getPieceCount() == 42:     # checking if the borad is full
            print("No more moves possible, Game Over!")
            GameBoard.scoreCount()  # printing the score
            print('Score: PlayerA = %d, PlayerB = %d\n' % (GameBoard.player1Score, GameBoard.player2Score))
            break
        else:   # computer move
            print("Computer is conputing based on next " + str(GameBoard.depth) + " steps...")
            GameBoard.changeMove()  # changing the player to other player
            GameBoard.aiPlay()  # computing the computer move with the minmax alpha beta puring
            GameBoard.displayGB()   # displaying game borad
            GameBoard.gameFile = open('computer.txt', 'w')  # printing output to file
            GameBoard.printGameBoardToFile()
            GameBoard.gameFile.close()  # file closing
            GameBoard.scoreCount()  # printing score count
            print('Score: PlayerA = %d, PlayerB = %d\n' % (GameBoard.player1Score, GameBoard.player2Score))

def interactiveMode(GameBoard, nextPlayer):     # interactive mode
    print('Current Board state')
    GameBoard.displayGB()   # displaying game board
    GameBoard.scoreCount()  # displaying score
    print('Score: PlayerA = %d, PlayerB = %d\n' % (GameBoard.player1Score, GameBoard.player2Score))
    if nextPlayer == 'human-next':  # checking who is the next player from argv
        humanPlay(GameBoard)    # human function 
    else:
        GameBoard.aiPlay()  # computign the computer move
        GameBoard.gameFile = open('computer.txt', 'w')  # printing the result into the file
        GameBoard.printGameBoardToFile()
        GameBoard.gameFile.close()  # closing the file
        GameBoard.displayGB()   # dislaying the game board
        GameBoard.scoreCount()  # displaying the score 
        print('Score: PlayerA = %d, PlayerB = %d\n' % (GameBoard.player1Score, GameBoard.player2Score))
        humanPlay(GameBoard)    # human turn next

    if GameBoard.getPieceCount() == 42: # displaying the final result after all the piece in the borad is full
        if GameBoard.player1Score > GameBoard.player2Score:
            print("Player 1 wins")
        if GameBoard.player1Score == GameBoard.player2Score:
            print("The game is a Tie")
        if GameBoard.player1Score < GameBoard.player2Score:
            print("Player 2 wins")
        print("Game Over")


def oneMoveMode(GameBoard):     # one move mode
    if GameBoard.pieceCount >= 42:  # checking if all the piece are filled, then exit
        print('Game board is full !\n Game Over...')
        sys.exit(0)
    print ('GameBoard state before move:')
    GameBoard.displayGB()   # displaying game board
    GameBoard.aiPlay()      # Computing the computer move
    print ('GameBoard state after move:')
    GameBoard.displayGB()   # displaying game board
    GameBoard.scoreCount()  # displaying score
    print('Score: PlayerA = %d, PlayerB = %d\n' % (GameBoard.player1Score, GameBoard.player2Score))
    GameBoard.printGameBoardToFile()    # printing the game board into file
    GameBoard.gameFile.close()      # close file

def main(argv): 
    GameBoard = MaxConnect4game()   #object of other file
    try:
        GameBoard.gameFile = open(argv[2], 'r')     #reading the input file
        fileLines = GameBoard.gameFile.readlines()
        GameBoard.GameBoard = [[int(char) for char in line[0:7]] for line in fileLines[0:-1]]
        GameBoard.currentMove = int(fileLines[-1][0])
        GameBoard.gameFile.close()
    except:
        print('File not found, begin new game.')
        GameBoard.currentMove = 1
    GameBoard.checkPieceCount()     # checking all the elements added is true or not
    GameBoard.depth = argv[4]   # depth taken from argv
    if argv[1] == 'one-move':   #for one move mode
        try:
            GameBoard.gameFile = open(argv[3], 'w')
        except:
            sys.exit('Error while opening output file.')
        oneMoveMode(GameBoard)
    else:   # for interactive mode
        interactiveMode(GameBoard, argv[3])

main(sys.argv)
# main function
