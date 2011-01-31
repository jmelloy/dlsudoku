class Node:
    """A single node in the dlx matrix"""
    def __init__(self):
        self.val = 1
        self.l = None
        self.r = None
        self.u = None
        self.d = None
        self.col = None
        self.row = None

    def __str__(self):
        return " " + str(self.val)

    def printName(self):
        """Returns the location of the node."""
        return "(" + str(self.col.name) + ", " + str(self.row.name) + ")"

    def info(self):
        """Returns the location and each link of the node."""
        ret = self.printName() + " " + str(self.val) + " R->"
        if self.r != None:
            ret = ret + self.r.printName()
        else:
            ret = ret + "None"
        ret = ret + " L->"
        if self.l != None:
            ret = ret + self.l.printName()
        else:
            ret = ret + "None"

        ret = ret + " U->"
        if self.u != None:
            ret = ret + self.u.printName()
        else:
            ret = ret + "None"

        ret = ret + " D->"
        if self.d != None:
            ret = ret + self.d.printName()
        else:
            ret = ret + "None"

        return ret
    
class ColumnHeader:
    """Stores the head of the column."""
    def __init__(self, name):
        self.n = 0
        self.name = name
        self.l = None
        self.r = None
        self.d = None
        self.u = None
        self.j = 0

    def __str__(self):
        return self.name

    def info(self):
        """Returns the name, count, and links to other columns."""
        ret = "%s %s R->" % (self.name, self.n)
        if self.r != None:
            ret = ret + self.r.printName()
        else:
            ret = ret + "None"
        ret = ret + " L->"

        if self.l != None:
            ret = ret + self.l.printName()
        else:
            ret = ret + "None"

        ret = ret + " U->"
        if self.u != None:
            ret = ret + self.u.printName()
        else:
            ret = ret + "None"
        
        ret = ret + " D->"
        if self.d != None:
            ret = ret + self.d.printName()
        else:
            ret = ret + "None"
            
        return ret
        
    def printName(self):
        return self.name
    
class RowHeader:
    """Contains a row's name and row number."""
    def __init__(self, name, i = 0):
        self.name = name
        self.i = i

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
        self.lastColumn = [Node() for i in range(len(columns))]
        self.currSol = []
        self.printSolution = 0
        self.keepSolutions = 1
        self.printProgress = 0
        self.solutions = []
        self.count = 0
        self.rows = []
        
        headerRow = []

        for i in range(len(columns)):
            headerRow.append(ColumnHeader(columns[i]))
            self.columnNames[columns[i]] = i
            if i > 0:
                headerRow[i].l = headerRow[i - 1]
                headerRow[i-1].r = headerRow[i]
            headerRow[i].j = i
        
        headerRow.append(ColumnHeader("#"))
        headerRow[-1].u = headerRow[-1]
        headerRow[-1].d = headerRow[-1]
        
        headerRow[0].l = headerRow[-1]
        headerRow[-1].r = headerRow[0]
        
        headerRow[-1].l = headerRow[-2]
        headerRow[-2].r = headerRow[-1]
        
        headerRow[-1].j = len(headerRow) - 1
                
        self.columns = headerRow

    def printReduced(self):
        r = []
        ret = []
        
        cols = []
        rows = {}
        h = self.columns[-1]
        c = h.r
        nodes = self.nodes
        while(c != h):
            cols.append(c.j)
            i = c.d
            while(i != c):
                rows[i.row.i] = 1
                i = i.d
            c = c.r
        
        for el in cols:
            r.append(self.columns[el].name)
        r.append("#")
        
        ret.append(" ".join(r))
        r = []

        sortedRows = rows.keys()
        sortedRows.sort()
        nCounter = 0
        
        for row in sortedRows:
            while(nCounter < len(nodes) and nodes[nCounter].row.i < row):
                nCounter += 1
            for col in cols:
                while(nCounter < len(nodes) and nodes[nCounter].col.j < col and nodes[nCounter].row.i == row):
                    nCounter += 1
                if nCounter < len(nodes) and nodes[nCounter].col.j == col:
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
        nCounter = 0
        nodes = self.nodes
        
        for col in self.columns:
            r.append(str(col.name))
        ret.append(" ".join(r))
        r = []
        for i in range(len(self.rows)):
            for j in range(len(self.columns) - 1):
                
                #print i, j, nCounter
                if nCounter < len(nodes) and nodes[nCounter].col.j == j and nodes[nCounter].row.i == i:
                    r.append(str(1))
                    nCounter += 1
                else:
                    r.append(str(0))
                
            r.append(str(self.rows[i]))
            ret.append(" ".join(r))
            r = []
        return "\n".join(ret)

    def addRow(self, data=[], name=None):
        if name == None:
            name = len(self.rows)
        rowName = RowHeader(name, len(self.rows))
        
        retVal = len(self.nodes)
        
        nodes = self.nodes
        rows = self.rows
        columns = self.columns
        lastColumn = self.lastColumn

        rows.append(rowName)
        
        sortedData = []
        for el in data:
            sortedData.append(self.columnNames.get(el))
        sortedData.sort()
        
        prevIndex = -1
        firstIndex = -1
        for el in sortedData:
            n = Node()
            index = el
            #print index, prevIndex, firstIndex
            
            if firstIndex == -1:
                firstIndex = len(nodes)
            else:
                n.r = nodes[firstIndex]
                nodes[firstIndex].l = n
                
            if prevIndex != -1:
                n.l = nodes[prevIndex]
                nodes[prevIndex].r = n
            
            n.col = columns[index]
            n.row = rows[-1]

            if columns[index].d == None:
                columns[index].d = n
                n.u = columns[index]
                n.d = columns[index]
            else:
                n.u = lastColumn[index]
                n.d = columns[index]
                
                lastColumn[index].d = n
            
            columns[index].u = n
            lastColumn[index] = n
            
            columns[index].n += 1

            prevIndex = len(nodes)
        
            nodes.append(n)

        return retVal

    def addGivens(self, given = []):
        nodes = self.nodes
        for el in given:
            self.coverColumn(nodes[el].col)
            self.currSol.append(nodes[el].row)
            
            j = nodes[el].r
            while(j != nodes[el]):
                self.coverColumn(j.col)
                j = j.r
        
    def solve(self, lvl=0):
        if lvl == 0:
            self.solutions = []
            self.count = 0
            
        h = self.columns[-1]
        
        if h.r == h:
            if self.printSolution or self.printProgress:
                print "Success:", 
                for el in self.currSol:
                    print el,
                print ""
            if self.keepSolutions:
                a = []
                for el in self.currSol:
                    a.append(el.name)
                self.solutions.append(a)
            self.count += 1
            return 1
        
        col = h.r
        test = len(self.rows)
        idx = 0
        while(col != h):
            
            if col.n < test:
                test = col.n
                idx = col.j
            
            if col.n == 0:
                if self.printProgress:
                    print "Failure"
                return 0
            
            if col.n == 1:
                break
            
            col = col.r
        
        c = self.columns[idx]
        self.coverColumn(c)
        
        r = self.columns[idx].d
        while(r != c):
            if self.printProgress:
                print "Selected: ", r.col, r.row

            self.currSol.append(r.row)
            
            #cover columns
            
            j = r.r
            while(j != r):
                self.coverColumn(j.col)
                j = j.r
            
            if self.printProgress:
                print self.printReduced()

            self.solve(lvl+1)
            self.currSol.pop()
            
            j = r.l
            while (j != r):
                self.uncoverColumn(j.col)
                j = j.l
            
            r = r.d
        self.uncoverColumn(c)
        
        if lvl == 0:
            print "Found %s solution(s)." % self.count
            
    def coverColumn(self, c):
        c.r.l = c.l
        c.l.r = c.r

        i = c.d

        while(i != c):
            j = i.r
            while(j != i):
                j.d.u = j.u
                j.u.d = j.d

                j.col.n -= 1

                j = j.r
            i = i.d
        
    def uncoverColumn(self, c):
        i = c.u

        while (i != c):
            j = i.l
            while(j != i):
                j.col.n += 1

                j.d.u = j
                j.u.d = j
                
                j = j.l
            
            i = i.u
        c.r.l = c
        c.l.r = c
    
    def info(self):
        for el in self.columns:
            print el.info()

        for n in self.nodes:
            print n.info()