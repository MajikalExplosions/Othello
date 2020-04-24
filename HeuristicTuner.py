# File: HeuristicTuner.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module attempts to find good values for the heuristic/utility function for the player.


from Minimax import Minimax
from OthelloBot import OthelloBot
from Board import Board
from time import sleep

from random import random

def main():
    b = Board()
    players = [OthelloBot(-1, b, 0, 0, 0), OthelloBot(1, b, 0, 0, 0)]
    p = 0
    while not b.gameOver():
        if len(b.getMoves(players[p].getTeam())) == 0:
            p = (p + 1) % 2
            print("No move.")
            continue
        #b._printBoard()
        move = players[p].getDebugMove()
        ret = b.setPiece(move, players[p].getTeam())
        for m in ret:
            b.setPiece(m, players[p].getTeam())
        p = (p + 1) % 2
        b._printBoard()
        #sleep(2)
    b._printBoard()
    #for move in b.getMoves(-1):
    #    b.setPiece(move, 2)
    #b._printBoard()

main()