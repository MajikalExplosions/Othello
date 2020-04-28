# File name: Othello.py
# Written by: Nikhita
# Date: April 19, 2020
# main runner

from GUI import *
from OthelloBot import *
from time import *

def main():
    board = Board()
    gui = GUI(board)
    human = gui.startGame()
    bot = OthelloBot(human*-1,board,(-6,2.5),(1,-2.2),(2.6,0.9))
    
    running=True
    turn = 1
    while running == True:
        # update score board
        whiteScore = board.countPieces(1)
        blackScore = board.countPieces(-1)
        gui.updateScore(1,whiteScore)
        gui.updateScore(-1,blackScore)

        # flip whose turn it is
        turn*=-1

        # get all the valid moves for that turn
        validMoves = board.getMoves(turn)

        # no valid moves, go to other player's turn
        if len(validMoves)==0:
            gui.updateMessage(turn,True,False,False)
            running = gui.clickAnywhere()

        # there are valid moves
        else:

            gui.updateMessage(turn,True,True,False)

            # human player turn
            if turn==human:
                clickPt = gui.click()
                if clickPt=="Quit":
                    running = False
                    break
                else:
                    # selected move valid
                    if validMoves.count(clickPt)!=0:
                        gui.newPiece(board,turn,clickPt,True)
                    # selected move invalid
                    else:
                        gui.updateMessage(turn,False,True,False)
                        turn*=-1
                        sleep(1.5)

            # AI turn
            else:
                move = bot.getMove()
                gui.highlightSquare(move)
                gui.newPiece(board,turn,move,True)
                sleep(1.5)
                gui.unhighlightSquare()

            # game is over
            if board.gameOver():
                whiteScore = board.countPieces(1)
                blackScore = board.countPieces(-1)
                gui.updateScore(1,whiteScore)
                gui.updateScore(-1,blackScore)

                # check who won
                if board.countPieces(1) > board.countPieces(-1):
                    color = 1
                else:
                    color = -1
                gui.updateMessage(color,False,True,True)

                # keep clicking until quit
                click = gui.clickAnywhere()
                while click:
                    click = gui.clickAnywhere()
                break
            

main()
