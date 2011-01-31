import dlx
dl = dlx.DLMatrix(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
dl.addRow(['C', 'E', 'F'])
dl.addRow(['A', 'D', 'G'])
dl.addRow(['B', 'C', 'F'])
dl.addRow(['A', 'D'])
dl.addRow(['B', 'G'])
dl.addRow(['D', 'E', 'G'])
print dl
print ""
dl.printProgress = 1
dl.printSolution = 1
dl.solve()