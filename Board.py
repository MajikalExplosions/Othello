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
                self.stable[i].append([False, False, False, False, False, False, False, False])
        
        #If stable[x][y][i] = true, that means if you travel in direction dir[i] you will only find friendly pieces and then a wall
        for i in range(8):
            #Top (+y)
            self.stable[i][7][0] = True
            self.stable[i][7][1] = True
            self.stable[i][7][3] = True

            #Down (-y)
            self.stable[i][0][4] = True
            self.stable[i][0][5] = True
            self.stable[i][0][7] = True

            #Left (-x)
            self.stable[0][i][5] = True
            self.stable[0][i][6] = True
            self.stable[0][i][3] = True

            #Right (+x)
            self.stable[7][i][1] = True
            self.stable[7][i][2] = True
            self.stable[7][i][7] = True
        
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
                if self.getPiece((i, j)) == player and self._isStable((i, j)):
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
                for k in range(8):
                    self.stable[i][j][k] = False

    def updateStability(self):
        self.resetStability()

        for i in range(8):
            #Vertical
            initBot = self.getPiece((i, 0))
            initTop = self.getPiece((i, 7))

            index, lastOpposite = 0, (-1, -1)
            while initBot != 0 and index < 8 and self.getPiece((i, index)) != 0:
                self.stable[i][index][4] = True
                index += 1
            
            index, lastOpposite = 0, (-1, -1)
            while initTop != 0 and index < 8 and self.getPiece((i, 7 - index)) != 0:
                self.stable[i][7 - index][0] = True
                index += 1
            
            #Horizontal
            initLeft = self.getPiece((0, i))
            initRight = self.getPiece((7, i))

            index, lastOpposite = 0, (-1, -1)
            while initLeft != 0 and index < 8 and self.getPiece((index, i)) != 0:
                self.stable[index][i][6] = True
                index += 1
            
            index, lastOpposite = 0, (-1, -1)
            while initRight != 0 and index < 8 and self.getPiece((7 - index, i)) != 0:
                self.stable[7 - index][i][2] = True
                index += 1

            #Diagonal Bots
            #Diagonal up (5, 1)
            initLeft = self.getPiece((i, 0))
            initRight = self.getPiece((7, 7 - i))

            index, lastOpposite = 0, (-1, -1)
            while initLeft != 0 and index < 8 - i and self.getPiece((i + index, index)) != 0:
                self.stable[i + index][index][5] = True
                index += 1
            
            index, lastOpposite = 0, (-1, -1)
            while initRight != 0 and index < 8 - i and self.getPiece((7 - index, 7 - i - index)) != 0:
                self.stable[7 - index][7 - i - index][1] = True
                index += 1

            #Diagonal down (7, 3)
            initLeft = self.getPiece((0, 7 - i))
            initRight = self.getPiece((7 - i, 0))

            index, lastOpposite = 0, (-1, -1)
            while initLeft != 0 and index < 8 - i and self.getPiece((index, 7 - index - i)) != 0:
                self.stable[index][7 - index - i][3] = True
                index += 1
            
            index, lastOpposite = 0, (-1, -1)
            while initRight != 0 and index < 8 - i and self.getPiece((7 - i - index, index)) != 0:
                self.stable[7 - i - index][index][7] = True
                index += 1

            #Diagonal Tops
            #Diagonal up (5, 1)
            initLeft = self.getPiece((0, i))
            initRight = self.getPiece((7 - i, 7))

            index, lastOpposite = 0, (-1, -1)
            while initLeft != 0 and index < 8 - i and self.getPiece((index, i + index)) != 0:
                self.stable[index][i + index][5] = True
                index += 1
            
            index, lastOpposite = 0, (-1, -1)
            while initRight != 0 and index < 8 - i and self.getPiece((7 - index - i, 7 - index)) != 0:
                self.stable[7 - index - i][7 - index][1] = True
                index += 1

            #Diagonal down
            initLeft = self.getPiece((i, 7))
            initRight = self.getPiece((7, i))

            index, lastOpposite = 0, (-1, -1)
            while initLeft != 0 and index < 8 - i and self.getPiece((i + index, 7 - index)) != 0:
                self.stable[i + index][7 - index][3] = True
                index += 1
            
            index, lastOpposite = 0, (-1, -1)
            while initRight != 0 and index < 8 - i and self.getPiece((7 - index, i + index)) != 0:
                self.stable[7 - index][i + index][7] = True
                index += 1

    def _inRange(self, number):
        return number >= 0 and number <= 7
    
    def _isStable(self, location):
        return (self.stable[location[0]][location[1]][0] or self.stable[location[0]][location[1]][4]) and (self.stable[location[0]][location[1]][1] or self.stable[location[0]][location[1]][5]) and (self.stable[location[0]][location[1]][2] or self.stable[location[0]][location[1]][6]) and (self.stable[location[0]][location[1]][3] or self.stable[location[0]][location[1]][7])
    
    def _printBoard(self):
        print("\nBoard State:\n")
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
        print("\n")
