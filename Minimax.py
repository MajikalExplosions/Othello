# File: Minimax.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module implements the Minimax algorithm with alpha-beta pruning, used as part of the AI.

from Board import Board
from random import random
from time import time

#White is 1, and wants to maximize. Black is -1, and wants to minimize.  None is 0.
class Minimax:

    def __init__(self, board, discMultiplier, mobilityMultiplier, stabilityMultiplier):
        #Multipliers for utility function
        self.discMultiplier = discMultiplier
        self.mobilityMultiplier = mobilityMultiplier
        self.stabilityMultiplier = stabilityMultiplier
        #Very Large Number TM
        self.INF = 1000000
        #Dictionary, works as a hash table
        self.table = {}
        self.board = board
        self.old = False

    #Board is the board object, player is the current player, depth is the current depth, target is the depth I want to search to, alpha/beta is for pruning
    def minimax(self, player, depth, alpha, beta, start):
        #Base case: game over, or depth is too large
        if self.board.gameOver():
            #If someone won, then this scenario is infinite points for them
            b, w = self.board.countPieces(False), self.board.countPieces(True)
            if w > b:
                return [self.INF, []]
            elif w < b:
                return [-1 * self.INF, []]
            #0 points if tie
            return [0, []]

        elif depth == 0 or (depth >= 4 and time() - start > 7):
            #If we've searched through depth moves, then return the current board's utility
            return [self._getUtility(self.board.getMoveNumber()), []]
        

        #Initial best is to lose
        best = [player * self.INF * -1, []]

        #Simulate all moves that the player can move
        for move in self.board.getMoves(player):
            
            #Move
            flips = self.board.move(move, player)

            #Recurse and simulate moves after this move for the opposite player (who wants to do as well as possible)
            res = self.minimax(-1 * player, depth - 1, alpha, beta, start)

            #Undo move
            for flip in flips:
                self.board.setPiece(flip[0], flip[1])
            self.board.updateStability()
            
            #Update alpha-beta
            #Alpha is basically the guaranteed best move you can have - no matter what score the moves after your current move get, you have AT LEAST alpha.
            #Beta is the same for the opposite player
            #See https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
            if player == 1:
                #White wants to maximize
                if best[0] < res[0] or (best[0] == res[0] and random() < 0.3):
                    best[0] = res[0]
                    best[1] = [move]
                
                #Update alpha, because you can always pick the current move
                if best[0] > alpha:
                    alpha = best[0]
                
            #Opposite of above
            else:
                if best[0] > res[0] or (best[0] == res[0] and random() < 0.3):
                    best[0] = res[0]
                    best[1] = [move]
                
                if best[0] < beta:
                    beta = best[0]
            
            #If you're guaranteed a score higher than the best score that you can get from the rest of the moves, then break
            if alpha >= beta:
                break
        
        #Return the best move you find and its utility
        return best

    #Never called if it's game over, so assume the game is still running
    def _getUtility(self, depth):
        #Factors for utility:
        #Current coin count
        #Mobility (move count)
        #Stability (number of stable pieces)

        #Use a "hash table" aka dictionary, only computing new utilities if necessary
        boardHash = self._hash(depth)
        if boardHash in self.table:
            return self.table[boardHash]
        
        utility = 0
        #It's not in the table yet, so find the utility

        discM = max(self.discMultiplier[0] + (self.discMultiplier[1] - self.discMultiplier[0]) / 60 * self.board.getMoveNumber(), 0)
        mobilityM = max(self.mobilityMultiplier[0] + (self.mobilityMultiplier[1] - self.mobilityMultiplier[0]) / 60 * self.board.getMoveNumber(), 0)
        stabilityM = max(self.stabilityMultiplier[0] + (self.stabilityMultiplier[1] - self.stabilityMultiplier[0]) / 60 * self.board.getMoveNumber(), 0)

        if self.old:
            utility = discM * (self.board.countPieces(1) - self.board.countPieces(-1))
        else:
            utility = 2 * discM * (self.board.getScore(1) - self.board.getScore(-1))
        utility += stabilityM * (self.board.countStablePieces(1) - self.board.countStablePieces(-1))
        utility += 0.5 * mobilityM * (self.board.getMoveCount(1) - self.board.getMoveCount(-1))

        #Now add it to hash table so we don't have to recalculate it anymore and return
        self.table[boardHash] = utility
        return utility

    def _hash(self, depth):
        #Converts each unique board state to a unique number as a key for the dictionary
        val = depth + 1
        for i in range(8):
            for j in range(8):
                square = self.board.getPiece((i, j)) + 1
                val = val * 3 + square
        return val