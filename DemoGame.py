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
    #Black (-1) is the good bot, white (1) is the bad bot.  Don't worry about the last three tuples because those are AI utility parameters.
    players = [OthelloBot(-1, b, (-2, 1), (0.75, 0.5), (1, 1)), OthelloBot(1, b, (1, 1), (0.1, 0.1), (0, 0))]
    p = 0
    longest = 0
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
        longest = max(longest, round((time() - t) * 1000))
        print("-----------------------------------------------")
    b._printBoard()
    print("White:", b.countPieces(1), " | Black:", b.countPieces(-1))
    print("Longest turn:", longest, "ms")
main()