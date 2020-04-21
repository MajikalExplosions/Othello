# File: Minimax.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module implements the Minimax algorithm with alpha-beta pruning, used as part of the AI.

from Board import Board

#White is 1, and wants to maximize. Black is -1, and wants to minimize.  None is 0.
class Minimax:

    def __init__(self, board, discMultiplier, mobilityMultiplier, stabilityMultiplier):
        self.multipliers = [discMultiplier, mobilityMultiplier, stabilityMultiplier]
        self.INF = 1000000
        #Dictionary, works as a hash table
        self.table = {}
        self.board = board

    #Board is the board object, player is the current player, depth is the current depth, target is the depth I want to search to, alpha/beta is for pruning
    def minimax(self, player, depth, target, alpha, beta):

        #Base case: game over, or depth is too large
        if self.board.gameOver():
            b, w = self.board.countPieces(False), self.board.countPieces(True)
            if w > b:
                return self.INF
            elif w < b:
                return -1 * self.INF
            return 0
        elif depth >= target:
            return [self._getUtility(player, depth), []]
        
        #Initial best is to not move
        best = [self._getUtility(player, depth), []]
        
        for move in self.board.getMoves(player):
            
            self.board.move(player, move)
            res = self.minimax(-1 * player, depth + 1, target, alpha, beta)
            self.board.move(0, move)

            if player == 1:
                best[0] = max(best[0], res[0])
                alpha = max(best[0], alpha)
                best[1] = move
                if best[0] == res[0]:
                    best[1].append(move)
            else:
                best[0] = min(best[0], res[0])
                beta = min(best[0], beta)
                if best[0] == res[0]:
                    best[1].append(move)
            
            if beta <= alpha:
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
        # TODO find the utility

        #Now add it to hash table so we don't have to look it up anymore and return
        self.table[boardHash] = utility
        return utility

    def _hash(self, depth):
        val = depth + 1
        for i in range(8):
            for j in range(8):
                square = self.board.getPiece(i, j) + 1
                val = val * 3 + square
        return val
    
    def _getStability(self, team):
        pass