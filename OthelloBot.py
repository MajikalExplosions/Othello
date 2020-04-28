# File: OthelloBot.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module implements an Othello bot, using a Minimax algorithm.

from Minimax import Minimax
import random

class OthelloBot:

    def __init__(self, team, board, discMultiplier, mobilityMultiplier, stabilityMultiplier):
        self.team = team
        #Minimax is basically a simulator
        self.minimax = Minimax(board, discMultiplier, mobilityMultiplier, stabilityMultiplier)
        self.board = board
        self.d = False
    
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
        
        #If we're in the endgame, look further ahead based on the number of moves remaining.
        if self.board.movesRemaining() <= 8:
            print("Searching at depth 8")
            move = self.minimax.minimax(self.team, 8, -1000000, 1000000)
        elif self.board.movesRemaining() <= 10:
            print("Searching at depth 5")
            move = self.minimax.minimax(self.team, 5, -1000000, 1000000)
        elif self.board.movesRemaining() <= 12:
            print("Searching at depth 4")
            move = self.minimax.minimax(self.team, 4, -1000000, 1000000)
        else:
            #If we're not in the endgame, use the number of valid moves to decide how deep to search
            moveCount = self.board.getMoveCount(self.team)
            if moveCount <= 5:
                print("Searching at depth 5")
                move = self.minimax.minimax(self.team, 5, -1000000, 1000000)
            elif moveCount <= 9:
                print("Searching at depth 4")
                move = self.minimax.minimax(self.team, 4, -1000000, 1000000)
            else:
                print("Searching at depth 3")
                move = self.minimax.minimax(self.team, 3, -1000000, 1000000)
        
        #Something wrong with the move returned
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
