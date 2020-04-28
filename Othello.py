# File name: Othello.py
# Written by: Nikhita
# Date: April 19, 2020
# main runner

from GUI import *

def main():
    board = Board()
    gui = GUI(board)
    human = gui.startGame()
    whiteScore = 0
    blackScore = 0
    
    running=True
    turn = 1
    while running == True:
        turn*=-1
        validMoves = board.getMoves(turn)

        # no valid moves, go to other player's turn
        if len(validMoves)==0:
            gui.updateMessage(turn,True,False)
            break
        
        clickPt = gui.click()
        if clickPt=="Quit":
            running=False
            break
        else:
            if validMoves.index(clickPt)!=0:
                gui.newPiece(board,turn,clickPt,True)
            else:
                gui.updateMessage(turn,False,True)
                turn*=-1

main()
