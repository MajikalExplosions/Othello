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
        clickPt = gui.click()
        if clickPt=="Quit":
            running=False
            break
        else:
            gui.newPiece(board,turn,clickPt,True)

main()
