# File: HeuristicTuner.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module attempts to find good values for the heuristic/utility function for the player.


from Minimax import Minimax
from OthelloBot import OthelloBot
from Board import Board
from time import sleep, time

from random import random

def main():
    b = Board()
    players = [OthelloBot(-1, b, (-2, 0.75), (0.5, 0.25), (1, 0.5)), OthelloBot(1, b, (0.1, 0.1), (0.1, 0.1), (0.1, 0.1))]
    p = 0
    while not b.gameOver():
        if len(b.getMoves(players[p].getTeam())) == 0:
            p = (p + 1) % 2
            print("No move.")
            continue
        t = time()
        print("Move", b.getMoveNumber())
        move = players[p].getMove()
        b.move(move, players[p].getTeam())
        p = (p + 1) % 2
        
        b._printBoard()
        print("White:", b.countPieces(1), " | Black:", b.countPieces(-1))
        print("Time spent to move:", round((time() - t) * 1000), "ms\n")
        print("-----------------------------------------------")
    b._printBoard()
    print("White:", b.countPieces(1), " | Black:", b.countPieces(-1))
main()