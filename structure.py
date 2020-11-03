#List of indexes for each box, used to calc box location for each num
BOX0 = [0, 1, 2, 9, 10, 11, 18, 19, 20]
BOX1 = [3, 4, 5, 12, 13, 14, 21, 22, 23]
BOX2 = [6, 7, 8, 15, 16, 17, 24, 25, 26]
BOX3 = [27, 28, 29, 36, 37, 38, 45, 46, 47]
BOX4 = [30, 31, 32, 39, 40, 41, 48, 49, 50]
BOX5 = [33, 34, 35, 42, 43, 44, 51, 52, 53]
BOX6 = [54, 55, 56, 63, 64, 65, 72, 73, 74]
BOX7 = [57, 58, 59, 66, 67, 68, 75, 76, 77]
BOX8 = [60, 61, 62, 69, 70, 71, 78, 79, 80]
BOXLIST = [BOX0, BOX1, BOX2, BOX3, BOX4, BOX5, BOX6, BOX7, BOX8]

class Sudoku:

    #  List = [[number, box, domain], ..., [number, box, domain]]
    #  Pairs = [[i1, i2]]
    """
    board = grid [puzzle] # numbers
    cells = list [coord] # Indexes for board, all coords in grid
    poss = dict [0: D(0)] # Dict for domains, all possible values of key
    #unary = list [rowC + colC + squareC] -> just for init, tell use related cells
    binary = list len # of constains, [[x, y], [x, z]] -> List of constraints -> WorkList
    related_cells = dict{x: y, z. y: x, z. z: x, y} -> Quick lookup for related cells
    skim = dict{x: list() if grid[i] = '0' else list(int(grid[i])) for i, x in enumerate(self.cells)}:
    """
    def __init__(self, numbers):
        d = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.list = []
        self.arcs = []
        for i in range(len(numbers)):
            for j in range(len(BOXLIST)):
                if i in BOXLIST[j]:
                    b = j #Index of what box this number belongs to
            if numbers[i] != 0:
                self.list.append([numbers[i], b, numbers[i]])
            else:
                self.list.append([0, b, d])

            temp = []
            for k in range(9):
                row = i//9
                col = i % 9
                if 9 * k + col != i: # appends every column to the list
                    temp.append(9 * k + col)

                if row * 9 + k != i:
                    temp.append(row*9+k)
            for k in BOXLIST[b]:
                if k != i and k not in temp:
                    temp.append(k)
            self.arcs.append(temp)  # List of all arcs, arcs[0] is a list of all indexs related with index 0
        self.boxes = BOXLIST  # a list containing the boxes of the sudoku with their indexes
        print(self.arcs)


    """
    print_sud
    ------------------------------------
    prints the numbers contained in the sudoku class
    ------------------------------------
    self - the sudoku object
    ____________________________________
    use: sudoku.printsud()
    """

    def print_sud(self):
        boxx = 0
        boxy = 0
        for i in range(81):
            if boxy == 3:
                print("------+-------+-----")
                boxy = 0
            for j in range(9):
                if boxx == 3:
                    print("|", end=" ")
                    boxx = 0
                print(self.list[i][j], end=" ")
                boxx += 1
            print()
            boxy += 1
            boxx = 0



