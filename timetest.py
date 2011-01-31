import time
from sudoku import Sudoku
import dlx

#b = ["7.6.........635...5.....2.3.7.2..9....2..9...9..8.1...........1...7.8.9...3.4...6"]
b = ["1.......2.9.4...5...6...7...5.9.3.......7.......85..4.7.....6...3...9.8...2.....1"]
#b = [".....45.....8.....7.2..39..5.8....6.3.......7.9....2.1..16..3.8.....5.....429...."]
totalTime = time.clock()
for board in b:
    s = Sudoku(board)
    print s
    t = time.clock()
    dl = s.generateDancingLinksMatrix()
    print 'Generation took %.3f seconds.' % (time.clock() - t)
    t = time.clock()
    try:
        dl.maxSolutions = 1
        dl.solve()
    except dlx.MaxSolutionsExceeded:
        pass
    for el in dl.solutions:
        print Sudoku(s.size, el)
    print 'Took %.3f seconds and %d picks' % (time.clock() - t, dl.picks)

print 'Total: %.3f seconds' % (time.clock() - totalTime)
