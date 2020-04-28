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
    bot = OthelloBot(human*-1,board,(0,1),(1,1),(2,2))
    
    running=True
    turn = 1
    while running == True:
        whiteScore = board.countPieces(1)
        blackScore = board.countPieces(-1)
        gui.updateScore(1,whiteScore)
        gui.updateScore(-1,blackScore)
        
        turn*=-1
        validMoves = board.getMoves(turn)

        # no valid moves, go to other player's turn
        if len(validMoves)==0:
            gui.updateMessage(turn,True,False)
            running = gui.clickAnywhere()
            break

        gui.updateMessage(turn,True,True)

        # human player turn
        if turn==human:
            clickPt = gui.click()
            if clickPt=="Quit":
                running = False
                break
            else:
                if validMoves.count(clickPt)!=0:
                    gui.newPiece(board,turn,clickPt,True)
                else:
                    gui.updateMessage(turn,False,True)
                    turn*=-1

        # AI turn
        else:
            sleep(1.5)
            move = bot.getMove()
            gui.highlightSquare(move)
            gui.newPiece(board,turn,move,True)
            sleep(1.5)
            gui.unhighlightSquare()
            

main()
