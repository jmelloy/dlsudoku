from copy import copy
class Board:
    def __init__(self, size, pieces = []):

        self.board = []
        self.size = size
        self.dashes = []
        self.boardPieces = []

        self.pieces = 0
        
        allowedPieces = []
        for i in range(0, size):
            allowedPieces.append(1)

        for i in range(0, size):
            self.board.append(copy(allowedPieces))

        for i in range(0, self.size * 4 + 1):
            self.dashes.append("-")
            
        if len(pieces) > 0:
            for el in [i for i in pieces if type(i) == tuple]:
                self.addQueen(el[0], el[1])

    def __str__(self):
        ret = []
        retLine = []
        retLine.append("  ")
        for i in range(0, self.size):
            retLine.append(" " + str(i) + " ")
        ret.append(" ".join(retLine))
        
        ret.append("  " + "".join(self.dashes))
        for i in range(self.size - 1, -1, -1):
            retLine = []
            retLine.append(str(i))
            for j in range(0, self.size):
                retLine.append("|")
                if self.board[i][j] == 0:
                    retLine.append("-")
                else:
                    retLine.append(str(self.board[i][j]))
            retLine.append("|")
            ret.append(" ".join(retLine))
            ret.append("  " + "".join(self.dashes))

        return "\n".join(ret)

    def addQueen(self, a = ()):
        self.addQueen(a[0], a[1])
        
    def addQueen(self, x, y):
        temp = x
        x = y
        y = temp

        if x > self.size:
            raise ValueError("Input value off the board")

        if y > self.size:
            raise ValueError("Input value off the board")

        if self.board[x][y] != 1 and self.board[x][y] != 0:
            raise ValueError("Piece already placed at that position")

        if self.board[x][y] == 0:
            raise ValueError("Piece threatened.")

        for i in range(0, self.size):
            self.threatenSquare(i, y)

            self.threatenSquare(x, i)

            xGreater = (x + i, x)[x + i < 0 or x + i >= self.size]
            yGreater = (y + i, y)[y + i < 0 or y + i >= self.size]
            xLess = (x - i, x)[x - i < 0 or x - i >= self.size]
            yLess = (y - i, y)[y - i < 0 or y - i >= self.size]

            self.threatenSquare(xGreater, yLess)

            self.threatenSquare(xGreater, yGreater)

            self.threatenSquare(xLess, yLess)

            self.threatenSquare(xLess, yGreater)

        self.board[x][y] = "Q"
        self.pieces += 1
        self.boardPieces.append((y, x))
    
    def threatenSquare(self, x, y):
        try:
            self.board[x][y] = 0
        except: IndexError
        pass
    
    def generateDancingLinksMatrix(self):
        from dlx import DLMatrix
        
        columns = []
        
        for i in range(self.size):
            median = self.size / 2
            med_plus  = median + i
            med_minus = median - i
            if med_plus < self.size:
                r = "R%s" % med_plus
                f = "F%s" % med_plus     
                
                columns.append(r)
                columns.append(f)
            if med_minus > -1  and med_plus != med_minus:
                r = "R%s" % med_minus
                f = "F%s" % med_minus
                
                columns.append(r)
                columns.append(f)
            
            if med_minus < 0 and med_plus >= self.size:
                break
            
        
        for i in range(1, self.size * 2 - 2):
            a = "A%s" % i
            b = "B%s" % i
            columns.append(a)
            columns.append(b)
            
        #print columns
        dl = DLMatrix(columns)
        h = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[j][i] != 0:
                    h = []
                    h.append("R%s" % (i))
                    h.append("F%s" % (j))
                    a = "A%s" % (i + j)
                    b = "B%s" % (self.size - 1 - i + j)
                    try:
                        columns.index(a)
                        h.append(a)
                    except: ValueError
                    pass
                
                    try:
                        columns.index(b)
                        h.append(b)
                    except: ValueError
                    pass
                    #print h
                    dl.addRow(h, (i, j))
        for i in range(1, self.size * 2 - 2):
            a = "A%s" % i
            b = "B%s" % i
            dl.addRow([a])
            dl.addRow([b])
        
        return dl