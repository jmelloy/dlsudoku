import time
import board
import dlx

board = board.Board(8)
board.addQueen(0,1)
print board

t = time.clock()
dl = board.generateDancingLinksMatrix()
dl.maxSolutions = False
dl.keepRecord = True
dl.keepSolutions = True
dl.solve()
print dl.count

print 'Took %.3f seconds' % (time.clock() - t)

f = open("queens.dot", "w")

f.write("digraph queens {\n")
f.write("rankdir=LR;\n")
#f.write("/* %s */\n" % board)
prev_rec = None
records = dl.rec.records
parents = {}

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
            if next.children > 1 or \
                next.selection == "Success" or \
                next.selection == "Failure":
                next_node = "%s_%d" % (next.selection, j)
                if next.children > 1 and next.selection != "Success" and next.selection != "Failure":
                    parents[j] = next_node
                distance = j - i - 1
                break

#    node_filename = "boards/%s.%s.png" % (orig.filename(), 
#        node_id.replace("(", "").replace(")", "").replace(" ", "").replace(",", "-"))

    if next_node:
#        next_filename = "boards/%s.%s.png" % (orig.filename(), 
#            next_node.replace("(", "").replace(")", "").replace(" ", "").replace(",", "-"))
        
        if next.selection == "Success":
            f.write('"%s" [label = "%s",color="green" ];\n' % (next_node, "Success"))
        elif next.selection == "Failure":
            f.write('"%s" [label = "%s",color="red"];\n' % (next_node, "Failure"))

        if display:
            f.write('"%s" [label = "%s"];\n' % (node_id, r.selection))
            f.write('"%s" [label = "%s"];\n' % (next_node, next.selection))
        
    if display:
#        s = sudoku.Sudoku(9, r.state)
#        s.createPNG(node_filename, board, r.state[-1])
        
        if next_node != node_id:
            f.write('"%s" -> "%s" [label= %d];\n' % (node_id, next_node, distance))
#            s = sudoku.Sudoku(9, next.state)
#            s.createPNG(next_filename, board, next.state[-1])
        if prev_node:
            f.write('"%s" -> "%s";\n' % (prev_node, node_id))

f.write("}")
f.close()

f = open("rec.txt", "w")
f.write(str(dl.rec))
f.close()