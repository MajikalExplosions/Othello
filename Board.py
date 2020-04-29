# File: Board.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module keeps track of the board's state as well as variables that the AI uses, such as stability and count.


class Board:

    def __init__(self):
        #Board is the board state (8x8)
        self.board = []
        #Board is whether each piece is stable (8x8)
        self.stable = []
        for i in range(8):
            self.board.append([])
            self.stable.append([])
            for j in range(8):
                self.stable[i].append(False)
                self.board[i].append(0)
        
        self.scoreMatrix = [0, 0, 0, 0, 0, 0, 0, 0]

        self.scoreMatrix[0] = [1.00, -0.2, 0.10, 0.05, 0.05, 0.10, -0.2, 1.00]
        self.scoreMatrix[1] = [-0.2, -0.4, 0.00, 0.00, 0.00, 0.00, -0.4, -0.2]
        self.scoreMatrix[2] = [0.10, 0.00, 0.10, 0.02, 0.02, 0.10, 0.00, 0.10]
        self.scoreMatrix[3] = [0.05, 0.00, 0.02, 0.02, 0.02, 0.02, 0.00, 0.05]
        self.scoreMatrix[4] = [0.05, 0.00, 0.02, 0.02, 0.02, 0.02, 0.00, 0.05]
        self.scoreMatrix[5] = [0.10, 0.00, 0.10, 0.02, 0.02, 0.10, 0.00, 0.10]
        self.scoreMatrix[6] = [-0.2, -0.4, 0.00, 0.00, 0.00, 0.00, -0.4, -0.2]
        self.scoreMatrix[7] = [1.00, -0.2, 0.10, 0.05, 0.05, 0.10, -0.2, 1.00]
        
        #The two below are the count of each player's pieces
        self.stableCount = [0, 0]
        self.count = [2, 2]

        #Start of game
        self.board[3][3], self.board[4][4] = 1, 1
        self.board[3][4], self.board[4][3] = -1, -1

    def gameOver(self):
        #Neither player can move
        return len(self.getMoves(-1)) == 0 and len(self.getMoves(1)) == 0

    def movesRemaining(self):
        return 64 - self.count[0] - self.count[1]

    def getMoveNumber(self):
        return 60 - self.movesRemaining()

    def countPieces(self, player):
        #Black is 0, white is 1
        return self.count[(player + 1) // 2]
    
    def countStablePieces(self, player):
        return self.stableCount[(player + 1) // 2]

    def getPiece(self, location):
        return self.board[location[0]][location[1]]

    def getMoveCount(self, player):
        count = 0
        #For each cell on the board
        directions = [[0, 1], [1, 1], [1, 0], [-1, 1], [0, -1], [-1, -1], [-1, 0], [1, -1]]
        for x in range(8):
            for y in range(8):
                canMove = False
                if self.getPiece((x, y)) != 0:
                    #If the cell isn't empty then you can't play there
                    continue
                
                #For each direction, if you can capture a piece then you can move on the square. As soon as you find one you're done.
                for i in range(len(directions)):
                    if (canMove):
                        break
                    d = directions[i]
                    index = 2

                    #Only move if the adjacent square is an enemy square
                    if self._inRange(x + d[0]) and self._inRange(y + d[1]) and self.getPiece((x + d[0], y + d[1])) == player * -1:
                        
                        #Go down the line and look for an enemy piece
                        while self._inRange(x + d[0] * index) and self._inRange(y + d[1] * index):
                            x2, y2 = x + d[0] * index, y + d[1] * index

                            if self.getPiece((x2, y2)) == player:
                                count += 1
                                canMove = True
                                break
                            if self.getPiece((x2, y2)) == 0:
                                break
                            
                            index += 1
        return count

    def getMoves(self, player):
        #See above, except instead of adding to count it adds the moves to a list
        validMoves = []
        directions = [[0, 1], [1, 1], [1, 0], [-1, 1], [0, -1], [-1, -1], [-1, 0], [1, -1]]
        for x in range(8):
            for y in range(8):
                canMove = False
                if self.getPiece((x, y)) != 0:
                    continue

                for i in range(len(directions)):
                    if (canMove):
                        #print(x, y, "can move.")
                        break
                    d = directions[i]
                    index = 2
                    #Only move if the adjacent square is an enemy square
                    if self._inRange(x + d[0]) and self._inRange(y + d[1]) and self.getPiece((x + d[0], y + d[1])) == player * -1:
                        while self._inRange(x + d[0] * index) and self._inRange(y + d[1] * index):
                            x2, y2 = x + d[0] * index, y + d[1] * index

                            if self.getPiece((x2, y2)) == player:
                                validMoves.append((x, y))
                                canMove = True
                                break
                            if self.getPiece((x2, y2)) == 0:
                                break
                            
                            index += 1
        return validMoves

    def setPiece(self, location, player):

        #Set the piece itself
        oldPlayer = self.board[location[0]][location[1]]

        #Update count variable
        if player == 0 and oldPlayer != 0:
            self.count[(oldPlayer + 1) // 2] -= 1
        if oldPlayer == 0:
            self.count[(player + 1) // 2] += 1
        elif oldPlayer == player * -1:
            self.count[1 - (player + 1) // 2] -= 1
            self.count[(player + 1) // 2] += 1
        
        self.board[location[0]][location[1]] = player

        #Get the list of the pieces that need to be flipped, like the getMoves()
        directions = [[0, 1], [1, 1], [1, 0], [-1, 1], [0, -1], [-1, -1], [-1, 0], [1, -1]]
        locOpposites = []
        for i in range(len(directions)):
            d = directions[i]
            locTemp, index = [], 1
            while self._inRange(location[0] + d[0] * index) and self._inRange(location[1] + d[1] * index):
                x, y = location[0] + d[0] * index, location[1] + d[1] * index

                if self.getPiece((x, y)) == player * -1:
                    locTemp.append((x, y))

                if self.getPiece((x, y)) == player:
                    for move in locTemp:
                        locOpposites.append(move)
                    break
                if self.getPiece((x, y)) == 0:
                    break
                index += 1
        return locOpposites
    
    def move(self, location, player):
        old = [(location, self.getPiece(location))]
        flips = self.setPiece(location, player)
        for f in flips:
            old.append((f, self.getPiece(f)))
            self.setPiece(f, player)
        
        #Move then update stability
        self.updateStability()
        return old

    def resetStability(self):
        for i in range(8):
            for j in range(8):
                self.stable[i][j] = False
        self.stableCount[0] = 0
        self.stableCount[1] = 0

    def updateStability(self):
        self.resetStability()
        self._runStability(-1)
        self._runStability(1)
    
    def _runStability(self, player):
        queue = []
        if self.getPiece((0, 0)) == player:
            queue.append((0, 0))
            self.stable[0][0] = True
            self.stableCount[(player + 1) // 2] += 1

        if self.getPiece((7, 0)) == player:
            queue.append((7, 0))
            self.stable[7][0] = True
            self.stableCount[(player + 1) // 2] += 1

        if self.getPiece((0, 7)) == player:
            queue.append((0, 7))
            self.stable[0][7] = True
            self.stableCount[(player + 1) // 2] += 1

        if self.getPiece((7, 7)) == player:
            queue.append((7, 7))
            self.stable[7][7] = True
            self.stableCount[(player + 1) // 2] += 1
        
        while len(queue) > 0:
            disc = queue.pop()
            #Update all adjacent squares for stability
            #Uses flood fill with disc as the queue
            #See https://en.wikipedia.org/wiki/Flood_fill
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    #If either dx or dy are non-zero then it's not the center square
                    #If in range AND not center square AND not stable
                    x, y = disc[0] + dx, disc[1] + dy
                    if self._inRange(x) and self._inRange(y) and (dx != 0 or dy != 0) and not self._isStable((x, y)) and self.getPiece((x, y)) == player:
                        #If none of the four lines can be flipped then it's stable.
                        horizontal = self._checkStable((x + 1, y), player) or self._checkStable((x - 1, y), player)
                        vertical = self._checkStable((x, y + 1), player) or self._checkStable((x, y - 1), player)
                        diagDown = self._checkStable((x + 1, y - 1), player) or self._checkStable((x - 1, y + 1), player)
                        diagUp = self._checkStable((x + 1, y + 1), player) or self._checkStable((x - 1, y - 1), player)
                        if horizontal and vertical and diagDown and diagUp:
                            self.stable[x][y] = True
                            self.stableCount[(player + 1) // 2] += 1
                            queue.append((x, y))

    def _inRange(self, number):
        return number >= 0 and number <= 7
    
    def _checkStable(self, location, player):
        if not self._inRange(location[0]) or not self._inRange(location[1]):
            return True
        return self._isStable(location) and self.getPiece(location) == player

    def _isStable(self, location):
        return self.stable[location[0]][location[1]]
    
    def getScore(self, player):
        score = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == player:
                    #+0.4 because I don't want to return a negative number.
                    score += self.scoreMatrix[i][j] + 0.4
        
        return score

    def _printBoard(self):
        print("\nBoard State:")
        for i in range(8):
            for j in range(8):
                val = self.getPiece((i, j))
                if val == 0:
                    print("-", end="")
                
                elif val == -1:
                    if self._isStable((i, j)):
                        print("B", end="")
                    else:
                        print("b", end="")
                
                elif val == 1:
                    if self._isStable((i, j)):
                        print("W", end="")
                    else:
                        print("w", end="")
                
                elif val == 3:
                    print("O", end="")
            
            print()
