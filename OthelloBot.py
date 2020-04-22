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
        return 0

    def getDebugMove(self):
        options = self.board.getMoves(self.team)
        for option in options:
            self.board.board[option[0]][option[1]] = 3
        self.board._printBoard()
        for option in options:
            self.board.board[option[0]][option[1]] = 0
        return options[random.randrange(len(options))]
