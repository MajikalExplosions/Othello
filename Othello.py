# File name: Othello.py
# Written by: Nikhita
# Date: April 19, 2020
# main runner

from GUI import *

def main():
    gui = GUI()
    human = gui.startGame()
    whiteScore = 0
    blackScore = 0
    
    running=True
    turn = 1
    while running == True:
        turn*=-1
        clickPt = gui.Click()
        if clickPt=="Quit":
            running=False
            break
        else:
            newPiece(turn,clickPt,True)

main()
            
