class Board:

    def __init__(self):
        self.board = []
        self.stable = []
        self.count = [[2, 0], [2, 0]]
        for i in range(8):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0])
            self.stable.append([False, False, False, False, False, False, False, False])
        
        self.board[3][3], self.board[4][4] = 1, 1
        self.board[3][4], self.board[4][3] = -1, -1

    def gameOver(self):
        return False

    def countPieces(self, player):
        pass
    
    def countStablePieces(self, player):
        pass

    def getPiece(self, location):
        return self.board[location[0]][location[1]]

    def getMoves(self, player):
        pass

    def setPiece(self, location, player):
        directions = [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1], [-1, 0], [-1, 1], [1, -1]]
        locOpposites = []
        for d in directions:
            locTemp, index = [], [], 1
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
        
        return locOpposites


    def _updateStability(self, location):
        pass
    
    def _inRange(self, number):
        return number >= 0 and number <= 7
