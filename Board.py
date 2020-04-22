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
        return len(getMoves(-1)) == 0 and len(getMoves(1)) == 0

    def countPieces(self, player):
        return self.count[(player + 1) // 2]
    
    def countStablePieces(self, player):
        pass

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
        if self.board[location[0]][location[1]] == -1 * player:
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
                        #For each move, update stability in this direction if applicable
                        locOpposites.append(move)
                    break
                if self.getPiece((x, y)) == 0:
                    break
                
                index += 1
            #Now check if it quit because of index errors, if it did update stability of chips that were moved through
            if not self._inRange(location[0] + d[0] * index) or not self._inRange(location[1] + d[1] * index):

                #Start at the same location and go backwards, updating stability
                index = index - 1
                while self._inRange(location[0] + d[0] * index) and self._inRange(location[1] + d[1] * index):
                    if self.getPiece(location[0] + d[0] * index, location[1] + d[1] * index) != player:
                        break
                    #If stable[x][y][i] = true, that means if you travel in direction dir[i] you will only find friendly pieces and then a wall
                    self.stable[location[0] + d[0] * index][location[1] + d[1] * index][d] = True

                    #Move one square back
                    index -= 1
        return locOpposites
    
    def _inRange(self, number):
        return number >= 0 and number <= 7
    
    def _isStable(self, location):
        return (self.stable[0] or self.stable[4]) and (self.stable[1] or self.stable[5]) and (self.stable[2] or self.stable[6]) and (self.stable[3] or self.stable[7])
    
    def _printBoard(self):
        print("\nBoard State:\n")
        for i in range(8):
            print(self.board[i])
        
        print("\n")

#b = Board()
#b._printBoard()
#for move in b.getMoves(-1):
#    b.setPiece(move, 2)
#b._printBoard()