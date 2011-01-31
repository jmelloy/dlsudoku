def safe_remove(a, num = 0):
    if num in a:
        a.remove(num)

class BadPartialSolve(Exception):
    pass

class Sudoku:

    def __init__(self, board, sol=[]):

        if type(board) == int:
            self.size = board
        else:
            self.size = int(pow(len(board), .5))
            self.board = board.replace("0", ".")

        if type(board) == int:

            a = ["."] * self.size * self.size

            for coords, val in sol:
                a[coords[1] * self.size + coords[0]] = str(val)

            #print a
            self.board = "".join(a)

    def solved(self):
        for i in self.board:
            if i == ".":
                return False
        
        return True

    def __str__(self):
        ret = []
        retLines = []
        a = ""
        r = int(pow(self.size, .5))
        for i in range(self.size):
            for j in range(self.size):
                if j % r == 0:
                    ret.append("|")
                ret.append(self.board[i * self.size + j])
            ret.append("|")
            a = " ".join(ret)
            if i % r == 0:
                retLines.append("-" * len(a))
            retLines.append(a)
            ret = []
        retLines.append("-" * len(a))

        return "\n".join(retLines)

    def partialSolve(self):
        cols = [set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9])]

        rows = [set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9])]
        blocks = [set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9]),set([1,2,3,4,5,6,7,8,9])]
        
        b = list(self.board)
        #print "".join(b)
        r = int(pow(self.size, .5))
        nums = range(self.size * self.size)
        for i in range(self.size):
            for j in range(self.size):
                n = b[i + j * self.size]
                if n != ".":
                    num = int(n)
                    safe_remove(nums, i + j * self.size)
                    #print "Removing %d from row %d, col %d, block %d" % (num, j, i, i / r + j - j % r)
                    safe_remove(cols[i], num)
                    safe_remove(rows[j], num)
                    safe_remove(blocks[i / r + j - j % r], num)
                    
        changed = True
        count = 1
        #print nums
        while(changed):
            changed = False
            print count, len(nums)
            count += 1
            for var in nums:
                    i = var % self.size
                    j = var / self.size
                    
                    opts = rows[j] & cols[i] & blocks[i / r + j - j % r]
                    #print j, i, opts
                    
                    if len(opts) == 0:
                        print "BAD PARTIAL"
                        raise BadPartialSolve
                        
                    if len(opts) == 1:
                        num = opts.pop()
                        safe_remove(nums, var)
                        b[i + j * self.size] = str(num)
                        safe_remove(cols[i], num)
                        safe_remove(rows[j], num)
                        safe_remove(blocks[i / r + j - j % r], num)
                        
                        #print "".join(b)
                        changed = True
                        
        #print "".join(b)
        return "".join(b)
        
    def generateDancingLinksMatrix(self):
        from dlx import DLMatrix

        l = []

        # Position

        for i in range(self.size):
            for j in range(self.size):
                l.append("P.%s,%s" % (j, i))

        for i in range(self.size):
            for j in range(1, self.size + 1):
                l.append("B.%s-%s" % (i, j)) # Blocks
                l.append("R.%s-%s" % (i, j)) # Rows
                l.append("C.%s-%s" % (i, j)) # Columns

        dl = DLMatrix(l)

        sq = int(pow(self.size, .5))
        given = []
        for i in range(self.size):
            for j in range(self.size):
                k = self.board[i * self.size + j]
                if k != ".":
                    r = []
                    r.append("P.%s,%s" % (j, i))
                    r.append("R.%s-%s" % (i, k))
                    r.append("C.%s-%s" % (j, k))
                    r.append("B.%s-%s" % ((int(i / sq) * sq + int(j/sq)), str(k)))

                    #print r, ((j, i), k)
                    given.append(dl.addRow(r, ((j, i), str(k))))

                else:
                    for k in range(1, self.size + 1):
                        r = []
                        r.append("P.%s,%s" % (j, i))
                        r.append("R.%s-%s" % (i, k))
                        r.append("C.%s-%s" % (j, k))
                        r.append("B.%s-%s" % ((int(i / sq) * sq + int(j/sq)), str(k)))

                        dl.addRow(r, ((j, i), k))
        dl.addGivens(given)
        return dl

    def createPNG(self, filename, orig=None, recent=None):
        from PIL import Image, ImageFont, ImageDraw
        size = self.size
        board = self.board

        im = Image.open("blank.png")
        font = ImageFont.truetype("/Library/Fonts/Times New Roman.ttf", 24)
        draw = ImageDraw.Draw(im)
        pos = -1

        if recent != None:
            coords = recent[0]
            pos = coords[1] * 9 + coords[0]

        for i in range(len(board)):
            if board[i] != '.':
                row = i / size
                col = i % size

                if orig == None or (orig != None and len(orig) > i and orig[i] != '.'):
                    draw.text((col * 33 + 15 + col / 3 * 2, row * 33 + 8),
                        str(board[i]), fill="black", font=font)
                elif i == pos:
                    draw.text((col * 33 + 15 + col / 3 * 2, row * 33 + 8),
                        str(board[i]), fill="red", font=font)
                else:
                    draw.text((col * 33 + 15 + col / 3 * 2, row * 33 + 8),
                        str(board[i]), fill="steelblue", font=font)
        im.save(filename, "PNG")

    def filename(self):
        val = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ret = []
        current = int(self.board.replace('.', ''))
        while (current != 0):
            rem = current % len(val)
            ret.insert(0, val[rem])
            current = current / len(val)
        return "".join(ret)

def generate(size = 9):
    from copy import copy
    from random import randint, shuffle
    from dlx import MaxSolutionsExceeded
    import sys

    sq = int(pow(size, .5))

    a = set([i + 1 for i in range(size)])
    validBoard = []

    for i in range(size * size):
        validBoard.append(copy(a))

    board = ["." for i in range(size * size)]

    multSol = True
    loops = 0
    while(multSol):
        loops += 1
        pos = randint(0, size * size - 1)
        while(board[pos] != "." or len(validBoard[pos]) == 0):
            pos = randint(0, size * size - 1)
        val = list(validBoard[pos])[randint(0, len(validBoard[pos]) - 1)]

        board[pos] = str(val)

        row = pos / size
        col = pos % size
        block = row / sq * sq + col / sq

        for i in range(size):
            validBoard[row * size + i].discard(val)
            validBoard[i * size + col].discard(val)

        for i in range(size):
            for j in range(size):
                if i / sq * sq + j / sq == block:
                    validBoard[i * size + j].discard(val)

        if loops > size:
            s = Sudoku("".join(board))
            dl = s.generateDancingLinksMatrix()
            dl.maxSolutions = 2
            try:
                dl.solve()
            except MaxSolutionsExceeded:
                pass

            if dl.count == 1:
                multSol = False
                s = Sudoku(size, dl.solutions[0])
                b = s.board
                for i in range(len(board)):
                    board[i] = b[i]
            elif dl.count == 0:
                board[pos] = "."
                for i in range(size):
                    validBoard[row * size + i].add(val)
                    validBoard[i * size + col].add(val)

                for i in range(size):
                    for j in range(size):
                        if i / sq * sq + j / sq == block:
                            validBoard[i * size + j].add(val)

    givens = [i for i in range(size * size) if board[i] != "."]
    shuffle(givens)

    for i in givens:
        val = board[i]
        board[i] = "."
        s = Sudoku("".join(board))
        dl = s.generateDancingLinksMatrix()
        dl.maxSolutions = 2
        try:
            dl.solve()
        except MaxSolutionsExceeded:
            pass

        if dl.count != 1:
            board[i] = val

    return "".join(board)

if __name__ == "__main__":
    from time import clock
    from dlx import MaxSolutionsExceeded
    from optparse import OptionParser
    from os.path import splitext

    import psyco
    psyco.full()

    usage = "usage: %prog [-ma] [-p puzzle] [-f filename] [-g]"

    parser = OptionParser(usage=usage)

    parser.add_option("-f", "--file", dest="filename",
                    help="Read puzzles from file", metavar="FILE")

    parser.add_option("-p", "--puzzle", dest="puzzle",
                    help="Solve single puzzle", type="string")

    parser.add_option("-g", "--generate", action="store_true", default=False)

    parser.add_option("-a", "--all", action="store_true", help="Find all solutions",default=False)

    parser.add_option("-m", "--max", type="int", help="Find first N solutions", default =1)

    parser.add_option("-w", "--write-png", type="string", help="Write out PNG of board")

    (options, args) = parser.parse_args()

    if not (options.puzzle or options.generate or options.filename):
        print parser.get_usage()

    if options.filename:
        f = open(options.filename, 'r')
        a = f.readlines()
        t = clock()
        count = 0
        for puzzle in a:
            s = Sudoku(puzzle[0:81])
            try:
                s.board = s.partialSolve()
            except BadPartialSolve:
                pass
            
            if not s.solved():
                dl = s.generateDancingLinksMatrix()
                dl.keepSolutions = False
                
                if not options.all:
                    dl.maxSolutions = options.max
                else:
                    dl.maxSolutions = 0

                try:
                
                    dl.solve()
                    #for el in dl.solutions:
                    #    s = Sudoku(s.size, el)
                    #    print s.board
                
                except MaxSolutionsExceeded:
                    pass

            count += 1

        print "%d puzzle(s) solved in %.3f seconds" % (count, clock() - t)

    if options.puzzle:
        s = Sudoku(options.puzzle)
        print s
        if options.write_png:
            (filename, extension) = splitext(options.write_png)
            if extension != '.png':
                extension += '.png'
            s.createPNG(filename + extension)

        t = clock()
        
        try:
            s.board = s.partialSolve()
            print s
        except BadPartialSolve:
            pass
        
        if not s.solved():
            dl = s.generateDancingLinksMatrix()
        
        
            if not options.all:
                dl.maxSolutions = options.max
            else:
                dl.maxSolutions = -1

            try:
                dl.solve()
            except MaxSolutionsExceeded:
                pass

            i = 1
            for el in dl.solutions:
                s = Sudoku(s.size, el)
                print s
                if options.write_png:
                    (filename, extension) = splitext(options.write_png)
                    if extension != '.png':
                        extension += '.png'
                    s.createPNG(filename + '-' + str(i) + extension, options.puzzle)

            print "Found %d solution(s) in %.3f seconds." % (dl.count, clock() - t)
        else:
            print "Found 1 solution in %.3f seconds." % (clock() - t)
            
    if options.generate:
        t = clock()
        g = generate(9)
        print g

        s = Sudoku(g)
        print s
        if options.write_png:
            (filename, extension) = splitext(options.write_png)
            if extension != '.png':
                extension += '.png'
            s.createPNG(filename + extension)
        dl = s.generateDancingLinksMatrix()
        dl.solve()
        print "Took %.3f seconds." % (clock() - t)
        if options.write_png:
            s = Sudoku(9, dl.solutions[0])
            (filename, extension) = splitext(options.write_png)
            if extension != '.png':
                extension += '.png'
            s.createPNG(filename + "-sol" + extension, g)
