# File: OthelloBot.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module implements an Othello bot, using a Minimax algorithm.

from Minimax import Minimax

class OthelloBot:

    def __init__(self, team, board, discMultiplier, mobilityMultiplier, stabilityMultiplier):
        self.team = team
        self.minimax = Minimax(board, discMultiplier, mobilityMultiplier, stabilityMultiplier)
    
    def getMove(self, state):
        return 0