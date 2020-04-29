# File: HeuristicTuner.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module attempts to find good values for the heuristic/utility function for the player.


from Minimax import Minimax
from OthelloBot import OthelloBot
from OthelloBotB import OthelloBotB
from Board import Board
from time import sleep, time

from random import random

#[-6.443624860176121, 4.457514907722221], [-0.1997017497463351, -2.9108142937614483], [1.804628451228265, 8.48468570765157]
#[-8.454348459405498, -3.2157696983264197], [-10.417346156664173, -0.020439015712805597], [0.7715599482309163, -16.21946879743112]
#[-2, 1], [0.75, 0.5], [5, 5]

def main():
    b = Board()
    
    players = [OthelloBotB(-1, b, (-6,2.5),(1,-2.2),(2.6,0.9)), OthelloBot(1, b, [3, -1], [2.35, 3], [-0.6, -2.9])]
    #players[1].setDebug(True)
    p = 0
    longest = [0, 0]
    average = [0, 0]
    turns = [0, 0]
    while not b.gameOver():
        print("Move", b.getMoveNumber(), "-", ["Black", "White"][p])
        if len(b.getMoves(players[p].getTeam())) == 0:
            p = (p + 1) % 2
            print("No move.")
            continue
        
        t = time()
        move = players[p].getMove()
        b.move(move, players[p].getTeam())
        total = (time() - t) * 1000

        longest[p] = max(longest[p], total)
        average[p] += total
        turns[p] += 1
        p = (p + 1) % 2
        
        b._printBoard()
        print("White:", b.countPieces(1), " | Black:", b.countPieces(-1))
        print("Time spent to move:", total, "ms\n")
        print("New board utility:", players[0].minimax._getUtility(0))
        print("-----------------------------------------------")

    b._printBoard()
    print("White:", b.countPieces(1), " | Black:", b.countPieces(-1))
    for i in range(2):
        average[i] /= turns[i]
    print("Longest turns:", longest, "ms")
    print("Average turns:", average, "ms")
    print("Average depth:", players[1].depthTotal / turns[1])
main()