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
        while (time() - start) < 9.5 and depth <= self.board.movesRemaining():

            cTime = time()
            move2 = self.minimax.minimax(self.team, depth, -1000000, 1000000, start)

            #First check for base case
            if depth == self.board.movesRemaining():
                if time() - start < 9.5:
                    move = move2
                break
            
            #Check for increasing depths
            if time() - cTime < 0.03:
                depth += 2
            elif time() - cTime < 0.3:
                depth += 1
            
            #If search wasn't truncated
            if time() - start < 9.5:
                move = move2
            else:
                #Search was truncated, so last search was -1 depth (probably)
                depth -= 1
                break
            
            move = move2
            #Do not allow higher depth than remaining move count
            depth = min(depth + 1, self.board.movesRemaining())
            
        print("Search took:", (time() - start) * 1000, "ms and went to depth", depth,"\n")
        #Following 3 lines is for averages
        self.depthTotal += depth
        if depth > self.board.movesRemaining() and self.board.movesRemaining() > 12:
            self.depthTotal -= 1
        #Something wrong with the move returned
        if not len(move) == 0 and len(move[1]) == 0:
            print("No valid move.")
        
        if len(move) == 0 or len(move[1]) == 0:
            print("Getting debug move.")
            return self.getDebugMove()
        

        return move[1][-1]

    def getDebugMove(self):
        options = self.board.getMoves(self.team)
        #There's a chance that there are no valid moves
        if len(options) == 0:
            return (-1, -1)
        return options[random.randrange(len(options))]
