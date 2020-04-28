# File: Minimax.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module implements the Minimax algorithm with alpha-beta pruning, used as part of the AI.

from Board import Board
from random import random

#White is 1, and wants to maximize. Black is -1, and wants to minimize.  None is 0.
class Minimax:

    def __init__(self, board, discMultiplier, mobilityMultiplier, stabilityMultiplier):
        self.discMultiplier = discMultiplier
        self.mobilityMultiplier = mobilityMultiplier
        self.stabilityMultiplier = stabilityMultiplier
        self.INF = 1000000
        #Dictionary, works as a hash table
        self.table = {}
        self.board = board

    #Board is the board object, player is the current player, depth is the current depth, target is the depth I want to search to, alpha/beta is for pruning
    def minimax(self, player, depth, alpha, beta):
        #Base case: game over, or depth is too large
        if self.board.gameOver():
            b, w = self.board.countPieces(False), self.board.countPieces(True)
            if w > b:
                return [self.INF, []]
            elif w < b:
                return [-1 * self.INF, []]
            return [0, []]
        elif depth == 0:
            return [self._getUtility(self.board.getMoveNumber()), []]
        
        #print(player, depth)

        #Initial best is to lose
        best = [player * self.INF * -1, []]

        for move in self.board.getMoves(player):
            
            #Move
            flips = self.board.move(move, player)

            #Recurse
            res = self.minimax(-1 * player, depth - 1, alpha, beta)

            #Undo move
            for flip in flips:
                self.board.setPiece(flip[0], flip[1])
            self.board.updateStability()
            
            #Update alpha-beta
            if player == 1:
                if best[0] < res[0] or (best[0] == res[0] and random() < 0.3):
                    best[0] = res[0]
                    best[1] = [move]
                
                if best[0] > alpha:
                    alpha = best[0]
                
            else:
                if best[0] > res[0] or (best[0] == res[0] and random() < 0.3):
                    best[0] = res[0]
                    best[1] = [move]
                
                if best[0] < beta:
                    beta = best[0]
            
            #Sign flipped?
            if alpha >= beta:
                break
        return best

    #Never called if it's game over, so assume the game is still running
    def _getUtility(self, depth):
        #Factors for heuristic:
        #Current coin count
        #Mobility (actual or potential?  I think I want to use actual which is number of moves currently but idk.)
        #Stability (can a square be captured at any point in the rest of the game?  This also includes corners)

        #Weights should be static, because that means I can cache the board's states and use it to look up utilities if they already exist
        #Use a "hash table" aka dictionary, only computing new utilities if necessary
        boardHash = self._hash(depth)
        if boardHash in self.table:
            return self.table[boardHash]
        
        utility = 0
        #It's not, so find the utility
        # TODO find the utility.  Perhaps also rotate it 3 times and find those utilities too?
        discM = max(self.discMultiplier[0] + (self.discMultiplier[1] - self.discMultiplier[0]) / 60 * self.board.getMoveNumber(), 0)

        #Mobility is (on average) 8
        mobilityM = max(self.mobilityMultiplier[0] + (self.mobilityMultiplier[1] - self.mobilityMultiplier[0]) / 60 * self.board.getMoveNumber(), 0) * 5

        #Stability is (on average) 20
        stabilityM = max(self.stabilityMultiplier[0] + (self.stabilityMultiplier[1] - self.stabilityMultiplier[0]) / 60 * self.board.getMoveNumber(), 0) * 2

        utility = discM * (self.board.countPieces(1) - self.board.countPieces(-1))
        utility += stabilityM * (self.board.countStablePieces(1) - self.board.countStablePieces(-1))
        utility += mobilityM * (len(self.board.getMoves(1)) - len(self.board.getMoves(-1)))
        #Now add it to hash table so we don't have to look it up anymore and return
        self.table[boardHash] = utility
        return utility

    def _hash(self, depth):
        val = depth + 1
        for i in range(8):
            for j in range(8):
                square = self.board.getPiece((i, j)) + 1
                val = val * 3 + square
        return val