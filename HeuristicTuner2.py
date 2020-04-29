# File: HeuristicTuner.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module attempts to find good values for the heuristic/utility function for the player.

from OthelloBot import OthelloBot
from OthelloBotB import OthelloBotB
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
        #print("Turn", counter, "-", pn[player])
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
    #bestArgs = [[-2, 1], [0.75, 0.5], [5, 5]]
    bestArgs = [[3, -1], [2.35, 3], [-0.6, -2.9]]
    newArgs = [[3, -1], [2.35, 3], [-0.6, -2.9]]
    bestScore = 0
    
    #P1 is benchmark - P2 tries to maximize their winrate against P1
    players = [0, 0]
    #[game 1 - p1, game 1 + p2]
    players[0] = [OthelloBotB(-1, board, (-6,2.5),(1,-2.2),(2.6,0.9)), OthelloBot(1, board, newArgs[0], newArgs[1], newArgs[2])]

    #[game 2 - p2, game2 + p1]
    players[1] = [OthelloBot(-1, board, newArgs[0], newArgs[1], newArgs[2]), OthelloBotB(1, board, (-6,2.5),(1,-2.2),(2.6,0.9))]
    
    wins = [0, 0]
    for i in range(1000000):
        for game in range(200):
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
        
        for game in range(200, 400):
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
        
        print("\nFinal Series Stats: P1 (Benchmark)", wins[0], "| P2 (New)", wins[1], "\n")
        #If the new player won at least 5 more games than the old player (1.25%)
        if wins[1] > bestScore + 5:
            #The new best score!
            #Offset for randomness
            bestScore = wins[1]
            bestArgs = [players[0][1].minimax.discMultiplier, players[0][1].minimax.mobilityMultiplier, players[0][1].minimax.stabilityMultiplier]
            newArgs = randomArgs()
            players[0][1] = OthelloBot(1, board, newArgs[0], newArgs[1], newArgs[2])
            players[1][0] = OthelloBot(-1, board, newArgs[0], newArgs[1], newArgs[2])
            wins = [0, 0]
        else:
            #Find a new player
            newArgs = randomArgs()
            players[0][1] = OthelloBot(1, board, newArgs[0], newArgs[1], newArgs[2])
            players[1][0] = OthelloBot(-1, board, newArgs[0], newArgs[1], newArgs[2])
            wins = [0, 0]
        
        print("New args:", newArgs)
        print("Best args:", bestArgs)
        print("Best score:", bestScore)
        

def modifyArgs(args):
    nA = [[0, 0], [0, 0], [0, 0]]
    for i in range(3):
        for j in range(2):
            nA[i][j] = args[i][j]
    i, j = randrange(0, 3), randrange(0, 2)
    nA[i][j] = nA[i][j] + getRandom()
    i2, j2 = i, j
    while i == i2 and j == j2:
        i2, j2 = randrange(0, 3), randrange(0, 2)
    nA[i2][j2] = nA[i2][j2] + getRandom()
    return nA

def randomArgs():
    nA = [[0, 0], [0, 0], [0, 0]]
    for i in range(3):
        for j in range(2):
            nA[i][j] = getRandom() * 5
    return nA

def getRandom():
    if random() < 0.5:
        return -1 * random()
    return random()

main()