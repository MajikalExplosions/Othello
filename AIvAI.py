# File: HeuristicTuner.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module attempts to find good values for the heuristic/utility function for the player.

from OthelloBot import OthelloBot
from Board import Board
from time import time
from random import random, randrange

def runGame(players, board):

    start = time()
    player = 0
    counter = 0
    pn = ["Black", "White"]
    while not board.gameOver():
        counter += 1
        move = players[player].getMove()
        if move == (-1, -1):
            player = (player + 1) % 2
            continue
        board.move(move, players[player].getTeam())
        player = (player + 1) % 2
    gameTime = round((time() - start) * 1000)

    if board.countPieces(-1) > board.countPieces(1):
        winner = -1
    elif board.countPieces(-1) < board.countPieces(1):
        winner = 1
    else:
        winner = 0
    
    print("Final Score: Black", board.countPieces(-1), "| White", board.countPieces(1))
    return winner

def main():
    board = Board()
    bestArgs = [[3, -1], [2.35, 3], [-0.6, -2.9]]
    bestArgs2 = [[3, 0], [0.25, 0.25], [1, 2]]
    #bestArgs2 = [[-0.4908588447878588, 0.7445917676345601], [2.4795991361621126, 1.33748709877603], [2.6214818754329414, 2.6081734329231616]]
    #bestArgs2 = [[-0.1319654790727236, 0.47409895661581647], [2.185869835046613, -0.1537808071565019], [1.6557078715434375, 1.0343744105119228]]
    #[game 1 - p1, game 1 + p2] [game 2 - p2, game2 + p1]
    players = [0, 0]
    players[0] = [OthelloBot(-1, board, bestArgs[0], bestArgs[1], bestArgs[2]), OthelloBot(1, board, bestArgs2[0], bestArgs2[1], bestArgs2[2])]
    players[1] = [OthelloBot(-1, board, bestArgs2[0], bestArgs2[1], bestArgs2[2]), OthelloBot(1, board, bestArgs[0], bestArgs[1], bestArgs[2])]
    
    wins = [0, 0]
    for i in range(1000000):
        for game in range(100):
            print("Running game", i + 1, "-", game + 1)
            w = runGame(players[0], board)
            if w == -1:
                wins[0] += 1
            if w == 0:
                wins[0] += 0.5
                wins[1] += 0.5
            if w == 1:
                wins[1] += 1

            board = Board()
            players[0][0].board = board
            players[0][1].board = board
            players[1][0].board = board
            players[1][1].board = board
        
        for game in range(100, 200):
            print("Running game", i + 1, "-", game + 1)
            w = runGame(players[1], board)
            if w == -1:
                wins[1] += 1
            if w == 0:
                wins[0] += 0.5
                wins[1] += 0.5
            if w == 1:
                wins[0] += 1

            board = Board()
            players[0][0].board = board
            players[0][1].board = board
            players[1][0].board = board
            players[1][1].board = board
        
        print("\nFinal Series Stats: P1", wins[0], "| P2", wins[1], "\n")

main()