LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
POS = 4

COL = 5
ROW = 6

NAME = 5
N = 6

class Record():
    def __init__(self, lvl, selection, parent, sol):
        self.lvl = lvl
        self.selection = selection
        self.parent = parent
        self.children = 0
        self.state = sol

    def __str__(self):
        return " " * self.lvl + str(self.lvl) + " " + str(self.selection) #+ " " + str(self.parent) + " " + str(self.children)

class RecursionRecord():
    def __init__(self):
        self.records = []
        self.records.append(Record(-1, "Start", 0, None))

    def add(self, lvl, selection, sol):
        i = 0
        found = False
        for i in range(len(self.records) - 1, -1, -1):
            if self.records[i].lvl == lvl - 1:
                found = True
                break
        if lvl == 0:
            i = 0

        self.records.append(Record(lvl, selection, i, sol))
        self.records[i].children += 1

    def __str__(self):
        a = []
        for i in range(len(self.records)):
            a.append("%4d%s" % (i, self.records[i]))
        return "\n".join(a)

class MaxSolutionsExceeded(Exception):
    pass

class RowHeader:
    """Contains a row's name and row number."""
    def __init__(self, name, i = 0, first = 0):
        self.name = name
        self.i = i
        self.first = first

    def __str__(self):
        return str(self.name)

    def info(self):
        return str(self.name)

    def printName(self):
        return str(self.name)

class DLMatrix:
    def __init__(self, columns=[]):

        self.columnNames = {}
        self.nodes = []
        self.lastColumn = [0 for i in range(len(columns) + 1)]
        self.currSol = []
        self.firstNode = 0
        self.keepSolutions = True
        self.printProgress = False
        self.keepRecord = False
        self.maxSolutions = 0
        self.picks = 0
        self.solutions = []
        self.count = 0
        self.rows = []
        self.rec = RecursionRecord()

#        self.covered = set()
        self.zeroes = set()

        nodes = self.nodes

        nodes.append([None, None, None, None, 0, "#", 0])

        i = 0
        for col in columns:
            i += 1
            nodes.append([None, None, None, None, i, col, 0])
            self.columnNames[col] = i
            nodes[i][LEFT] = i - 1
            nodes[i - 1][RIGHT] = i

        #nodes[0][UP] = 0
        #nodes[0][DOWN] = 0

        nodes[-1][RIGHT] = 0
        nodes[0][LEFT] = len(nodes) - 1

        self.firstNode = len(nodes)

    def printReduced(self):
        r = []
        ret = []

        cols = []
        rows = {}
        nodes = self.nodes

        h = nodes[0]
        c = nodes[h[RIGHT]]

        while(c != h):
            cols.append(c[POS])
            i = nodes[c[DOWN]]
            while(i != c):
                rows[i[ROW].i] = 1
                i = nodes[i[DOWN]]
            c = nodes[c[RIGHT]]

        for el in cols:
            r.append(nodes[el][NAME])
        r.append("#")

        ret.append(" ".join(r))
        r = []

        sortedRows = rows.keys()
        sortedRows.sort()
        nCounter = self.firstNode

        for row in sortedRows:
            while(nCounter < len(nodes) and nodes[nCounter][ROW].i < row):
                nCounter += 1
            for col in cols:
                while(nCounter < len(nodes) and nodes[nodes[nCounter][COL]][POS] < col and nodes[nCounter][ROW].i == row):
                    nCounter += 1
                if nCounter < len(nodes) and nodes[nodes[nCounter][COL]][POS] == col:
                    r.append(str(1))
                else:
                    r.append(str(0))

            r.append(str(self.rows[row].name))
            ret.append(" ".join(r))
            r = []
        return "\n".join(ret)

    def __str__(self):
        r = []
        ret = []
        nCounter = self.firstNode
        nodes = self.nodes

        for col in self.nodes[1:self.firstNode]:
            r.append(str(col[NAME]))
        r.append("#")
        ret.append(" ".join(r))
        r = []
        for i in range(len(self.rows)):
            for j in range(1, len(self.columnNames) + 1):

                #print i, j, nCounter, nodes[nodes[nCounter][COL]][POS], nodes[nCounter][ROW].i
                if nCounter < len(nodes) and nodes[nodes[nCounter][COL]][POS] == j and nodes[nCounter][ROW].i == i:
                    r.append(str(1))
                    nCounter += 1
                else:
                    r.append(str(0))

            r.append(str(self.rows[i]))
            ret.append(" ".join(r))
            r = []
        return "\n".join(ret)

    def addRow(self, data=[], name=None):

        nodes = self.nodes
        rows = self.rows
        lastColumn = self.lastColumn
        columnNames = self.columnNames

        if name == None:
            name = len(rows)

        rowName = RowHeader(name, len(rows), len(nodes))

        retVal = len(rows)

        rows.append(rowName)

        sortedData = []
        for el in data:
            sortedData.append(columnNames.get(el))
        sortedData.sort()
        #print sortedData

        prevIndex = -1
        firstIndex = -1
        for index in sortedData:
            n = [len(nodes), len(nodes), None, None, len(nodes), None, None]
            currVal = len(nodes)
            #print index, prevIndex, firstIndex

            if firstIndex == -1:
                firstIndex = currVal
            else:
                n[RIGHT] = firstIndex
                nodes[firstIndex][LEFT] = currVal

            if prevIndex != -1:
                n[LEFT] = prevIndex
                nodes[prevIndex][RIGHT] = currVal
            #print COL, index
            n[COL] = index
            n[ROW] = rows[-1]

            if nodes[index][DOWN] == None:
                nodes[index][DOWN] = currVal
                n[UP] = index
                n[DOWN] = index
            else:
                n[UP] = lastColumn[index]
                n[DOWN] = index

                nodes[lastColumn[index]][DOWN] = currVal

            nodes[index][UP] = currVal
            lastColumn[index] = currVal

            nodes[index][N] += 1

            prevIndex = len(nodes)

            nodes.append(n)

        return retVal

    def addGivens(self, given = []):
        nodes = self.nodes
        rows = self.rows
        for row in given:
            self.coverColumn(nodes[nodes[rows[row].first][COL]])
            self.currSol.append(rows[row])

            j = nodes[nodes[rows[row].first][RIGHT]]
            while(j != nodes[rows[row].first]):
                self.coverColumn(nodes[j[COL]])
                j = nodes[j[RIGHT]]

    def solve(self, lvl=0):
        if lvl == 0:
            self.solutions = []
            self.count = 0

        nodes = self.nodes
        h = self.nodes[0]

        if nodes[h[RIGHT]] == h:
            if self.keepRecord:
                self.rec.add(lvl, "Success", [row.name for row in self.currSol])
            if self.printProgress:
                print "Success:",
                for el in self.currSol:
                    print el,
                print ""
            if self.keepSolutions:
                self.solutions.append([row.name for row in self.currSol])
            self.count += 1
            if self.maxSolutions and self.count >= self.maxSolutions:
                raise MaxSolutionsExceeded

            return 1

        if len(self.zeroes) > 0:
            if self.keepRecord:
                self.rec.add(lvl, "Failure (%s)" % ", ".join([str(el) for el in self.zeroes]),
                    [row.name for row in self.currSol])
            if self.printProgress:
                print "Failure (%s)" % ", ".join([str(el) for el in self.zeroes])
            return 0

        col = nodes[h[RIGHT]]
        test = len(self.rows)
        idx = 0
        while(col != h and (self.maxSolutions == 0 or self.count < self.maxSolutions)):

            if col[N] < test:
                test = col[N]
                idx = col[POS]

            if col[N] == 0:
                if self.keepRecord:
                    self.rec.add(lvl, "Failure (%s)" % col[NAME], [row.name for row in self.currSol])
                if self.printProgress:
                    print "Failure (%s)" % col[NAME]
                return 0

            if col[N] == 1:
                break

            col = nodes[col[RIGHT]]

        c = self.nodes[idx]
        self.coverColumn(c)

        r = nodes[c[DOWN]]
        while(r != c):
            if self.printProgress:
                print "Selected: ", nodes[r[COL]][NAME], r[ROW]

            self.picks += 1
            self.currSol.append(r[ROW])
            #cover columns
            if self.keepRecord:
                self.rec.add(lvl, r[ROW].name, [row.name for row in self.currSol])

            j = nodes[r[RIGHT]]
            while(j != r):
                self.coverColumn(nodes[j[COL]])
                j = nodes[j[RIGHT]]

            if self.printProgress:
                print self.printReduced()

            self.solve(lvl+1)
            self.currSol.pop()

            j = nodes[r[LEFT]]
            while (j != r):
                self.uncoverColumn(nodes[j[COL]])
                j = nodes[j[LEFT]]

            r = nodes[r[DOWN]]
        self.uncoverColumn(c)


    def coverColumn(self, c):
        self.zeroes.discard(c[NAME])
        nodes = self.nodes
        nodes[c[RIGHT]][LEFT] = c[LEFT]
        nodes[c[LEFT]][RIGHT] = c[RIGHT]

        i = nodes[c[DOWN]]

        while(i != c):
            j = nodes[i[RIGHT]]
            while(j != i):
                nodes[j[DOWN]][UP] = j[UP]
                nodes[j[UP]][DOWN] = j[DOWN]

                nodes[j[COL]][N] -= 1
                if nodes[j[COL]][N] == 0:
                    self.zeroes.add(nodes[j[COL]][NAME])

                j = nodes[j[RIGHT]]
            i = nodes[i[DOWN]]

    def uncoverColumn(self, c):
        self.zeroes.discard(c[NAME])
        nodes = self.nodes
        i = nodes[c[UP]]

        while (i != c):
            j = nodes[i[LEFT]]
            while(j != i):
                nodes[j[COL]][N] += 1
                self.zeroes.discard(nodes[j[COL]][NAME])

                nodes[j[DOWN]][UP] = j[POS]
                nodes[j[UP]][DOWN] = j[POS]

                j = nodes[j[LEFT]]

            i = nodes[i[UP]]
        nodes[c[RIGHT]][LEFT] = c[POS]
        nodes[c[LEFT]][RIGHT] = c[POS]
