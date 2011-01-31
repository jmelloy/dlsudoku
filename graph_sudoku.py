import time
import sudoku
import dlx

board = "...6...7...418..6..6..5...8..9...5..18.....46..3...8..8...7..5..7..492...3...5..."
#board = "1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3.."
#board = "1.......2.9.4...5...6...7...5.9.3.......7.......85..4.7.....6...3...9.8...2.....1"
#board = "7.6.........635...5.....2.3.7.2..9....2..9...9..8.1...........1...7.8.9...3.4...6"
#board = "....1.6....5...3.762.7....1....6.4..8..3....9..1.2..8.2...53....34....2..9......."

#board = sudoku.generate(9)
print board
s = sudoku.Sudoku(board)
print s
t = time.clock()
dl = s.generateDancingLinksMatrix()
dl.maxSolutions = True
dl.keepRecord = True
try:
    dl.solve()
except dlx.MaxSolutionsExceeded:
    pass

for el in dl.solutions:
    print sudoku.Sudoku(s.size, el)
print 'Took %.3f seconds' % (time.clock() - t)

f = open("rec.dot", "w")

f.write("digraph dlsudoku {\n")
f.write("rankdir=LR;\n")
f.write("/* %s */\n" % board)
prev_rec = None
records = dl.rec.records
parents = {}

orig = sudoku.Sudoku(board)

for i in range(len(records)):
    r = records[i]
    node_id = "%s_%d" % (r.selection, i)

    display = False

    next = r
    next_node = None
    prev_node = None

    if parents.has_key(r.parent):
        display = True
        prev_node = parents.get(r.parent)

    if r.lvl == 0:
        display = True

    distance = 0

    if display:
        for j in range(i, len(records)):
            next = records[j]
            check = str(next.selection)
            if next.children > 1 or \
                check == "Success" or \
                check.startswith("Failure"):
                next_node = "%s_%d" % (next.selection, j)
                if next.children > 1 and check != "Success" and not check.startswith("Failure"):
                    parents[j] = next_node
                distance = j - i - 1
                break

    node_filename = "boards/%s.%s.png" % (orig.filename(),
        node_id.replace("(", "").replace(")", "").replace(" ", "").replace(",", "-"))

    if next_node:
        next_filename = "boards/%s.%s.png" % (orig.filename(),
            next_node.replace("(", "").replace(")", "").replace(" ", "").replace(",", "-"))

        if display:
            f.write('"%s" [label = "%s",URL="%s"];\n' % (node_id, r.selection, node_filename))
            if next.selection == "Success":
                f.write('"%s" [label = "%s",color="green",URL="%s" ];\n' %
                    (next_node, next.selection, next_filename))
            elif str(next.selection).startswith("Failure"):
                f.write('"%s" [label = "%s",color="red",URL="%s"];\n' %
                    (next_node, next.selection.replace(" ", "\\n", 1), next_filename))
            else:
                f.write('"%s" [label = "%s",URL="%s"];\n' %
                    (next_node, next.selection, next_filename))

    if display:
        s = sudoku.Sudoku(9, r.state)
        s.createPNG(node_filename, board, r.state[-1])

        if next_node != node_id:
            f.write('"%s" -> "%s" [label= %d];\n' % (node_id, next_node, distance))
            s = sudoku.Sudoku(9, next.state)
            s.createPNG(next_filename, board, next.state[-1])
        if prev_node:
            f.write('"%s" -> "%s";\n' % (prev_node, node_id))

f.write("}")
f.close()

f = open("rec.txt", "w")
f.write(str(dl.rec))
f.close()
print "Done"
