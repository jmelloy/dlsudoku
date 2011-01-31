from board import Board
import time

for i in range(2, 13):
    b = Board(i)
    dl = b.generateDancingLinksMatrix()
    dl.keepSolutions = 0
    t = time.clock()
    dl.solve()
    print "%3d Found %d solutions in %.3f seconds." % (i, dl.count, time.clock() - t)
    
    for b in dl.solutions:
        print Board(i, b)