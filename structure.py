BOX1 = [0, 1, 2, 9, 10, 11, 18, 19, 20]
BOX2 = [3, 4, 5, 12, 13, 14, 21, 22, 23]
BOX3 = [6, 7, 8, 15, 16, 17, 24, 25, 26]
BOX4 = [27, 28, 29, 36, 37, 38, 45, 46, 47]
BOX5 = [30, 31, 32, 39, 40, 41, 48, 49, 50]
BOX6 = [33, 34, 35, 42, 43, 44, 51, 52, 53]
BOX7 = [54, 55, 56, 63, 64, 65, 72, 73, 74]
BOX8 = [57, 58, 59, 66, 67, 68, 75, 76, 77]
BOX9 = [60, 61, 62, 69, 70, 71, 78, 79, 80]
BOXLIST = [BOX1, BOX2, BOX3, BOX4, BOX5, BOX6, BOX7, BOX8, BOX9]

ROW1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
ROW2 = [9, 10, 11, 12, 13, 14, 15, 16, 17]
ROW3 = [18, 19, 20, 21, 22, 23, 24, 25, 26]
ROW4 = [27, 28, 29, 30, 31, 32, 33, 34, 35]
ROW5 = [36, 37, 38, 39, 40, 41, 42, 43, 44]
ROW6 = [45, 46, 47, 48, 49, 50, 51, 52, 53]
ROW7 = [54, 55, 56, 57, 58, 59, 60, 61, 62]
ROW8 = [63, 64, 65, 66, 67, 68, 69, 70, 71]
ROW9 = [72, 73, 74, 75, 76, 77, 78, 79, 80]
ROWLIST = [ROW1, ROW2, ROW3, ROW4, ROW5, ROW6, ROW7, ROW8, ROW9]

COLUMN1 = [0, 9, 18, 27, 36, 45, 54, 63, 72]
COLUMN2 = [1, 10, 19, 28, 37, 46, 55, 64, 73]
COLUMN3 = [2, 11, 20, 29, 38, 47, 56, 65, 74]
COLUMN4 = [3, 12, 21, 30, 39, 48, 57, 66, 75]
COLUMN5 = [4, 13, 22, 31, 40, 49, 58, 67, 76]
COLUMN6 = [5, 14, 23, 32, 41, 50, 59, 68, 77]
COLUMN7 = [6, 15, 24, 33, 42, 51, 60, 69, 78]
COLUMN8 = [7, 16, 25, 34, 43, 52, 61, 70, 79]
COLUMN9 = [8, 17, 26, 35, 44, 53, 62, 71, 80]
COLUMNLIST = [COLUMN1, COLUMN2, COLUMN3, COLUMN4, COLUMN5, COLUMN6, COLUMN7, COLUMN8, COLUMN9]


class Sudoku:

    def __init__(self, numbers):
        self.list = numbers  # the numbers for the sudoku
        self.boxes = BOXLIST  # a list containing the boxes of the sudoku with their indexes
        self.rows = ROWLIST  # a list containing the rows of the sudoku with their indexes
        self.columns = COLUMNLIST  # a list containing the columns of the sudoku with their indexes
        self.domains = []  # will be length of 81, contains the domain for every cell

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
        for i in range(9):
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

    """
    find_location
    ------------------------------------
    finds the box that the index resides in for easier comparisons
    ------------------------------------
    indexx = the x index for the location of the number
    indexy = the y index for the location of the number
    box = the box that the index resides in
    ____________________________________
    use: box = sudoku.find_location(indexx, indexy)
    """

    def find_location(self,indexx, indexy):
        box = 0
        for x in self.boxes:
            if 9*indexy + indexx in x:
                #  print(9*indexy + indexx) can alsobe used to find domain index for a given [x][y]
                box = x
        return box
