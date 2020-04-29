# File: OthelloBotB.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module implements an Othello bot, using a Minimax algorithm.

from Minimax import Minimax
import random
from time import time
class OthelloBotC:

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
        return self.getDebugMove()

    def getDebugMove(self):
        options = self.board.getMoves(self.team)
        #There's a chance that there are no valid moves
        if len(options) == 0:
            return (-1, -1)
        return options[random.randrange(len(options))]
