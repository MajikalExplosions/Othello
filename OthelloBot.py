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
    
    def getTeam(self):
        return self.team
    
    def getMove(self):
        move = self.minimax.minimax(self.team, 0, 4, -1000000, 1000000)
        if len(move) == 0 or len(move[1]) == 0:
            return self.getDebugMove()
        return move[1][-1]

    def getDebugMove(self):
        options = self.board.getMoves(self.team)
        if len(options) == 0:
            return (-1, -1)
        return options[random.randrange(len(options))]
