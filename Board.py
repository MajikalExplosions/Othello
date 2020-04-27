# File: Board.py
# Written By: Joseph Liu
# Date: 4/14/20
# This module keeps track of the board's state as well as variables that the AI uses, such as stability and count.


class Board:

    def __init__(self):
        self.board = []
        self.stable = []
        for i in range(8):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0])
            self.stable.append([])
            self.count = [2, 2]
            for j in range(8):
                self.stable[i].append(False)
        
        self.board[3][3], self.board[4][4] = 1, 1
        self.board[3][4], self.board[4][3] = -1, -1

    def gameOver(self):
        return len(self.getMoves(-1)) == 0 and len(self.getMoves(1)) == 0

    def movesRemaining(self):
        return 64 - self.count[0] - self.count[1]

    def getMoveNumber(self):
        return 60 - self.movesRemaining()

    def countPieces(self, player):
        return self.count[(player + 1) // 2]
    
    def countStablePieces(self, player):
        count = 0
        for i in range(8):
            for j in range(8):
                if self.getPiece((i, j)) == player and self.stable[i][j]:
                    count += 1
        
        return count

    def getPiece(self, location):
        return self.board[location[0]][location[1]]

    def getMoves(self, player):
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
        oldPlayer = self.board[location[0]][location[1]]
        if player == 0 and oldPlayer != 0:
            self.count[(oldPlayer + 1) // 2] -= 1
        if oldPlayer == 0:
            self.count[(player + 1) // 2] += 1
        elif oldPlayer == player * -1:
            self.count[1 - (player + 1) // 2] -= 1
            self.count[(player + 1) // 2] += 1
        
        self.board[location[0]][location[1]] = player

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
        
        self.updateStability()
        return old

    def resetStability(self):
        for i in range(8):
            for j in range(8):
                self.stable[i][j] = False

    def updateStability(self):
        self.resetStability()
        self._runStability(-1)
        self._runStability(1)
    
    def _runStability(self, player):
        queue = []
        if self.getPiece((0, 0)) == player:
            queue.append((0, 0))
            self.stable[0][0] = True

        if self.getPiece((7, 0)) == player:
            queue.append((7, 0))
            self.stable[7][0] = True

        if self.getPiece((0, 7)) == player:
            queue.append((0, 7))
            self.stable[0][7] = True

        if self.getPiece((7, 7)) == player:
            queue.append((7, 7))
            self.stable[7][7] = True
        
        while len(queue) > 0:
            disc = queue.pop()
            #Update all adjacent squares for stability
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    #If either dx or dy are non-zero then it's not the center square
                    #If in range AND not center square AND not stable
                    x, y = disc[0] + dx, disc[1] + dy
                    if self._inRange(x) and self._inRange(y) and (dx != 0 or dy != 0) and not self._isStable((x, y)) and self.getPiece((x, y)) == player:
                        horizontal = self._checkStable((x + 1, y), player) or self._checkStable((x - 1, y), player)
                        vertical = self._checkStable((x, y + 1), player) or self._checkStable((x, y - 1), player)
                        diagDown = self._checkStable((x + 1, y - 1), player) or self._checkStable((x - 1, y + 1), player)
                        diagUp = self._checkStable((x + 1, y + 1), player) or self._checkStable((x - 1, y - 1), player)
                        if horizontal and vertical and diagDown and diagUp:
                            self.stable[x][y] = True
                            queue.append((x, y))

    def _inRange(self, number):
        return number >= 0 and number <= 7
    
    def _checkStable(self, location, player):
        if not self._inRange(location[0]) or not self._inRange(location[1]):
            return True
        return self._isStable(location) and self.getPiece(location) == player

    def _isStable(self, location):
        return self.stable[location[0]][location[1]]
    
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
