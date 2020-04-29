# File: HeuristicTuner.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module attempts to find good values for the heuristic/utility function for the player.

from OthelloBot import OthelloBot
from Board import Board
from time import time
from random import random, randrange

THREAD_COUNT = 1
LEARNING_RATE = 0.5

class BotInstance:
    
    def __init__(self, botID, args):
        self.id = botID
        self.args = args
        self.games = []
        self.bot = 0
    
    def deepCopy(self, newID):
        a = []
        for i in range(6):
            a = args[i] + (random() - 0.5) * 2 * LEARNING_RATE
        return BotInstance(newID, a)
    
    def createBot(self, team, board):
        self.bot = OthelloBot(team, board, (self.args[0], self.args[1]), (self.args[2], self.args[3]), (self.args[4], self.args[5]))
        return self.bot
    
    def addRecentGame(self, res):
        self.games.append(res)
    
    def clearGames(self):
        self.games = []
    
    def kdr(self):
        total = 0
        for game in self.games:
            total += game
        return total / len(self.games)
    

class GameManager:
    
    def __init__(self):
        self.players = []
        self.boards = []
        self.pairs = []
    
    def runGeneration(self):        
        if len(self.players) == 0:
            #New, so generate new players
            for i in range(THREAD_COUNT * 2):
                self.players.append(BotInstance(i, [randomWeight(), randomWeight(), randomWeight(), randomWeight(), randomWeight(), randomWeight()]))
            self.players[0] = BotInstance(0, [-2, 1, 0.75, 0.5, 5, 5])
            self.players[1] = BotInstance(1, [-1, 0.5, 5, 0, 5, 5])
        print("Simulating games.")
        for gameNum in range(7):
            self.boards, self.pairs, playerIDs = [], [], []
            
            for i in range(THREAD_COUNT):
                self.boards.append(Board())

            for i in range(THREAD_COUNT * 2):
                playerIDs.append(i)
            
            #Now we have players and new boards, so run games
            for i in range(THREAD_COUNT):
                self.pairs.append((playerIDs.pop(randrange(0, len(playerIDs))), playerIDs.pop(randrange(0, len(playerIDs)))))

            for index in range(THREAD_COUNT):
                print("Running game", gameNum, "-", index, ":", self.pairs[index])
                runGame([self.players[self.pairs[index][0]], self.players[self.pairs[index][1]]], self.boards[index], self, index)
        
        self.players.sort(key=kdrKey)
        print("Winner", self.players[-1].id, "KDR:", self.players[-1].kdr())

    def updateGameResult(self, gameID, time, winner):
        b, w = self.players[self.pairs[gameID][0]], self.players[self.pairs[gameID][1]]
        if winner == -1:
            b.addRecentGame(1)
            w.addRecentGame(0)
        elif winner == 1:
            b.addRecentGame(0)
            w.addRecentGame(1)
        elif winner == 0:
            b.addRecentGame(0.5)
            w.addRecentGame(0.5)
        self.boards[gameID]._printBoard()
        print("Game", gameID, "took", time, "ms. ", winner, "won.\n")
    
    def getPlayers(self, gameID):
        return [self.players[self.pairs[gameID][0]], self.players[self.pairs[gameID][1]]]

    def getBoard(self, gameID):
        return self.boards[gameID]

def kdrKey(o):
    return o.kdr()

def randomWeight():
    #Returns between -10 and 10
    return (random() - 0.5) * 2 * 10

def runGame(players, board, gm, gameID):

    for i in range(2):
        players[i] = players[i].createBot(i * 2 - 1, board)
    start = time()
    player = 0
    counter = 1
    while not board.gameOver():
        print("Turn", counter)
        counter += 1
        move = players[player].getMove()
        if move == (-1, -1):
            player = (player + 1) % 2
            continue
        board.move(move, players[player].getTeam())

        player = (player + 1) % 2
    gameTime = round((time() - start) * 1000)

    if board.countPieces(-1) > board.countPieces(1):
        winner = -1
    elif board.countPieces(-1) < board.countPieces(1):
        winner = 1
    else:
        winner = 0
    
    gm.updateGameResult(gameID, gameTime, winner)

def main():
    gm = GameManager()
    for i in range(1):
        gm.runGeneration()

main()