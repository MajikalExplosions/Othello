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
        for x in range(8):
            for y in range(8):
                directions = [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1], [-1, 0], [-1, 1], [1, -1]]
                for i in range(len(directions)):
                    d = directions[i]
                    index = 1
                    while self._inRange(x + d[0] * index) and self._inRange(y + d[1] * index):
                        x2, y2 = x + d[0] * index, y + d[1] * index

                        if self.getPiece(x, y) == player:
                            validMoves.append((x, y))
                            break
                        if self.getPiece(x, y) == 0:
                            break
                        
                        index += 1
        return validMoves

    def setPiece(self, location, player):
        if self.board[location[0]][location[1]] == -1 * player:
            self.count[1 - (player + 1) // 2] -= 1
        self.count[(player + 1) // 2] += 1
        self.board[location[0]][location[1]] = player

        directions = [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1], [-1, 0], [-1, 1], [1, -1]]
        locOpposites = []
        for i in range(len(directions)):
            d = directions[i]
            locTemp, index = [], 1
            while self._inRange(location[0] + d[0] * index) and self._inRange(location[1] + d[1] * index):
                x, y = location[0] + d[0] * index, location[1] + d[1] * index

                if self.getPiece(x, y) == player * -1:
                    locTemp.append((x, y))

                if self.getPiece(x, y) == player:
                    for move in locTemp:
                        locOpposites.append(move)
                    break
                if self.getPiece(x, y) == 0:
                    break
                
                index += 1
            #Now check if it quit because of index errors, if it did update stability of chips that were moved through
        return locOpposites
    
    def _inRange(self, number):
        return number >= 0 and number <= 7
