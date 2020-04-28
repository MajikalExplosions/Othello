# File: OthelloBot.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module implements an Othello bot, using a Minimax algorithm.

from Minimax import Minimax
import random

class OthelloBot:

    def __init__(self, team, board, discMultiplier, mobilityMultiplier, stabilityMultiplier):
        self.team = team
        self.minimax = Minimax(board, discMultiplier, mobilityMultiplier, stabilityMultiplier)
        self.board = board
        self.d = False
    
    def setDebug(self, d):
        self.d = d

    def setTeam(self, team):
        self.team = team

    def getTeam(self):
        return self.team
    
    def getMove(self):
        
        if self.d:
            return self.getDebugMove()
        if self.board.movesRemaining() <= 8:
            move = self.minimax.minimax(self.team, 8, -1000000, 1000000)
        elif self.board.movesRemaining() <= 10:
            move = self.minimax.minimax(self.team, 5, -1000000, 1000000)
        elif self.board.movesRemaining() <= 12:
            move = self.minimax.minimax(self.team, 4, -1000000, 1000000)
        else:
            move = self.minimax.minimax(self.team, 3, -1000000, 1000000)
        if len(move) == 0 or len(move[1]) == 0:
            return self.getDebugMove()
            
        return move[1][-1]

    def getDebugMove(self):
        options = self.board.getMoves(self.team)
        if len(options) == 0:
            return (-1, -1)
        return options[random.randrange(len(options))]
