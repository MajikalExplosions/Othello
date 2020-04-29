# File: OthelloBot.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module implements an Othello bot, using a Minimax algorithm.  Uses time to decide depth

from Minimax import Minimax
import random
from time import time
class OthelloBot:

    def __init__(self, team, board, discMultiplier, mobilityMultiplier, stabilityMultiplier):
        self.team = team
        #Minimax is basically a simulator
        self.minimax = Minimax(board, discMultiplier, mobilityMultiplier, stabilityMultiplier)
        self.board = board
        self.d = False
        self.depthTotal = 0
    
    def setDebug(self, d):
        #Debug flag (random move)
        self.d = d

    def setTeam(self, team):
        self.team = team

    def getTeam(self):
        return self.team
    
    def getMove(self):
        
        if self.d:
            return self.getDebugMove()

        move = []
        start, depth = time(), 2
        while (time() - start) < 3 and depth <= self.board.movesRemaining() and depth <= 12:
            depth += 1
            #print("Searching at depth", depth)
            start = time()
            #The following function also breaks if it goes over the time limit
            move2 = self.minimax.minimax(self.team, depth, -1000000, 1000000, start)
            if time() - start < 0.05 and depth <= 12:
                depth = min(depth + 2, 12)
            elif time() - start < 0.5 and depth <= 12:
                depth = min(depth + 1, 12)
            elif time() - start < 7 and depth <= 12:
                move = move2
            else:
                #print("Search truncated.")
                depth -= 1
                break
            
            #print("Search took:", (time() - start) * 1000, "ms\n")
        self.depthTotal += depth
        if depth > self.board.movesRemaining() and self.board.movesRemaining() > 12:
            self.depthTotal -= 1
        #Something wrong with the move returned
        if len(move) == 0 or len(move[1]) == 0:
            #print("Getting debug move.")
            return self.getDebugMove()
        
        return move[1][-1]

    def getDebugMove(self):
        options = self.board.getMoves(self.team)
        #There's a chance that there are no valid moves
        if len(options) == 0:
            return (-1, -1)
        return options[random.randrange(len(options))]
