#Variables used to create coordinate system of cells
from itertools import permutations

colChars = 'ABCDEFGHI'
rowChars = '123456789'

class Sudoku:

    """
    board = grid [puzzle] # numbers
        List of numbers in raw representation of sudoku puzzle
    cells = list [coord] # Indexes for board, all coords in grid
        Organizes each square into chess coordinates with Cols as A-I and rows as 1-9
    poss = dict [0: D(0)] # Dict for domains, all possible values of key
        Dictionary to keep track of domain at each cell (cell used as keys A1, A2, A3, ..., I8, I9)
    binary = list len # of constains, [[x, y], [x, z]] -> List of constraints -> WorkList
        List of al binary constraints, used as the workList from pseudocode
    related_cells = dict{x: y, z. y: x, z. z: x, y} -> Quick lookup for related cells
        Dictionary of related cells aka neighbors aka all cells sharing a row/col/box in the sudoku puzzle
    skim = dict{x: list() if grid[i] = '0' else list(int(grid[i])) for i, x in enumerate(self.cells)}:
        Dictionary of all cells who had values removed from their domain due to the assignment of cell x to a value
    """
    def __init__(self, numbers):
        self.board = numbers
        self.cells = self.create_cells(colChars, rowChars)

        # For each cell set domain to 1-9 if not filled in, else set domain to current integer inside cell
        self.poss = {a: list(range(1,10)) if numbers[i] == '0' else [int(numbers[i])] for i, a in enumerate(self.cells)}

        # Create skimmed/pruned dicts for use in unassigning cell values
        # (reverts domain changes cause by original assignment)
        self.skim = {a: list() if numbers[i] == '0' else [int(numbers[i])] for i, a in enumerate(self.cells)}

        # List of binary contraints, same as work list from pseudo code
        self.binary = []
        self.create_bi_constraints()

        # Dictionary of related cells (Neighbors)
        self.relCells = {}
        self.create_rel_cells()

    """
    create_bi_constraints
    -----------------------------------------
    Creates list of all binaryContraints (work list)
    -----------------------------------------
    Use:
        self.create_bi_constraints()
    """
    def create_bi_constraints(self):
        # Create list of all squares in puzzle
        relatedRows = [self.create_cells(colChars, i) for i in rowChars]  # All related rows (A1, B1... I1), (A2, B2...)
        relatedCols = [self.create_cells(j, rowChars) for j in colChars]  # All related cols (A1, A2, ...A9), (B1...B9)
        # All related Boxes (A1, A2, A3, B1, B2, B3, C1, C2, C3), (A4, A5, A6, B4, ..., C6), ...
        relatedBoxes = [self.create_cells(j, i) for j in ('ABC', 'DEF', 'GHI') for i in ('123', '456', '789')]

        squares = (relatedRows + relatedCols + relatedBoxes)
        #iterate through list of squares
        for square in squares:
            # List of permutations in square aka: a list of arcs
            combos = self.permutate(square)  # Create all permutations of a square
            for combo in combos:
                # Loop through all arcs, if they arent already found then add them to list of arcs/biConstraints
                if [combo[0], combo[1]] not in self.binary: # If item already in binary don't add it to binary
                    self.binary.append([combo[0], combo[1]])

    """
    create_rel_cells
    ------------------------------------------------
    Sets up self.relCells
    ------------------------------------------------
    self - Access to current instance of sudoku object
    ------------------------------------------------
    Edits self.relCells to create list of related cells aka neighbors
    ------------------------------------------------
    Use:
        self.create_rel_cells()
    """
    def create_rel_cells(self):
        for i in self.cells:
            self.relCells[i] = []  # Set dict at key i to blank list, used to create list of related cells
            for j in self.binary:
                if i == j[0]:  # Check each binary constraint to see if its x value is teh same as the current cell i
                    self.relCells[i].append(j[1])  # Binary constraint y value must be neighbors to cell i

    """
    solved
    ------------------------------------------------
    Checks the length of all domains to see if puzzle has been solved
    ------------------------------------------------
    self - Access to current instance of sudoku object
    ------------------------------------------------
    Returns True if solved, False if not solved
    ------------------------------------------------
    Use:
        if sudoku.solved(): print solution else: backtrack
    """
    def solved(self):
        for i in self.cells:  # Loop through all cells
            if len(self.poss[i]) > 1:  # Solved iff every cells is assigned a singular value (domain of len 1)
                return False

        return True

    """
    complete
    ------------------------------------------------
    Checks the length of domains and if they have been assigned in backtrack algorithm
    ------------------------------------------------
    self - Access to current instance of sudoku object
    assignment - Dict of all cells with their assigned values
    ------------------------------------------------
    Returns True if assignment complete, False if not
    ------------------------------------------------
    Use:
        if sudoku.complete(assignment): print solution else: backtrack
    """
    def complete(self, assignment):
        for i in self.cells:  # Loop through all cells
            # All domains must be of len 1 AND all cells in assignment dictionary must be assigned a value
            if len(self.poss[i]) > 1 and i not in assignment:
                return False

        return True

    """
    consistent
    ------------------------------------------------
    Checks key (cell) and v (value) for each cell in assignment to see if
    they are not arc consistent with all related cells. Used to check if
    we should backtrack or continue on this path in the tree
    ------------------------------------------------
    self - Access to current instance of sudoku object
    assignment - Dict of all cells with their assigned values
    var - variable/cell we are checking (A1, B2, etc)
    val - value of the cell we are checking (0-9)
    ------------------------------------------------
    Returns True if assignment consistent, false otherwise
    ------------------------------------------------
    Use:
        if sudoku.consistent(assignment, v, val):
            Assign value val to cell v in assignment
        else:
            Move onto next v in domain values
    """
    def consistent(self, assignment, var, val):
        consistent = True

        # assignment.items() returns list of all (key, value) pairs in the assignment dictionary
        for key, v in assignment.items():
            # If an item has the same value as var cell (val) and the cell containing that value is related to var
            # Then an inconsistency is detected
            if v == val and key in self.relCells[var]:
                consistent = False

        return consistent

    """
    assign
    -----------------------------------------------
    assigns cell var to value val in assignment dict, forward checks
    to not allow for errors
    -----------------------------------------------
    var - variable/cell we are assigning
    val - value to assign to that cell
    assignment - assignment dict used in backtracking
    """
    def assign(self, var, val, assignment):
        assignment[var] = val  # assign cell the value

        self.forward_check(var, val, assignment)  # Do forward check to see if there are new conflicts


    """
    unassign
    --------------------------------------------------
    unassigns a given cell (var), deleteing it from the assignment dict.
    Reverses the forward checking done when the cell (var) was assigned its value
    by going through skim dict and removing all forward checked cells, appending their values
    back into their domains.
    --------------------------------------------------
    var - cell/variable we are unassigning
    assignment - dict used for back tracking alg
    """
    def unassign(self, var, assignment):
        if var in assignment:
            # Loop through all variables whos domain was changed due to the assignment of cell var
            for (d, v) in self.skim[var]:  # d is domain/key, v is value of d
                self.poss[d].append(v)  # Append previously removed values back onto domain of cell d

            self.skim[var] = []  # Set skim dict at var to empty as its assignments were all reversed

            del assignment[var]  # Delete var key from assignment dict

    """
    forward_check
    ----------------------------------------------
    Does forward checking technique, looks through all cells related
    to given cell var, checks if those cells have been assigned yet. If not
    then check if the val that was assigned to cell var is in the domain. If so
    remove it from the domain to prevent arc inconsistency, append to skimmed dict
    for possible unassignment
    ----------------------------------------------
    var - variable/cell we are forward checking after it has been assigned a value
    val - value that the cell var has been assigned
    assignment - dict of assigned cells used to backtracking alg
    ----------------------------------------------
    Use:
        self.forward_check(var, val, assignment)
    """
    def forward_check(self, var, val, assignment):

        for i in self.relCells[var]:  # Loop through all cells related to var
            if i not in assignment:  # if cell i not yet assigned
                if val in self.poss[i]:  # if val is in the domain of i
                    self.poss[i].remove(val)  # Remove val from domain of i (as it was just assigned)
                    self.skim[var].append((i, val))  # Append to list of domain changes caused by assignment of var

    """
    print_sol
    ------------------------------------
    Prints the domains in self.poss in the format of a sudoku board
    ------------------------------------
    self - the sudoku object
    ____________________________________
    use: sudoku.print_sol()
    """
    def print_sol(self):
        count = 1
        print("-----------------------")
        print("|", end="")
        for i in self.poss.items():  # Use .items() to get all value pairs in dictionary i[0] is cellID i[1] is value
            if count % 3 == 0:  # Every 3 values add | to separate boxes
                print(i[1], end=" | ")
            else:
                print(i[1], end=" ")
            if count % 9 == 0:  # Every 9 values make a new line to rep the next row
                print("")
                if count % 27 == 0:
                    print("-----------------------")  # Every 27 values add lines to rep bottom of a box
                if count % 81 != 0:  # Exists to avoid printing an extra | in the last loop
                    print("|", end="")
            count += 1

    """
    print_sud
    ------------------------------------
    Prints the sudoku puzzle from the list in self.board()
    ------------------------------------
    self - the sudoku object
    ____________________________________
    use: sudoku.print_sud()
    """
    def print_sud(self):
        count = 1
        print("-----------------------")
        print("|", end="")
        for i in self.board:
            if count % 3 == 0:  # Every 3 values add | to separate boxes
                print(i, end=" | ")
            else:
                print(i, end=" ")
            if count % 9 == 0:  # Every 9 values make a new line to rep the next row
                print("")
                if count % 27 == 0:
                    print("-----------------------")  # Every 27 values add lines to rep bottom of a box
                if count % 81 != 0:  # Exists to avoid printing an extra | in the last loop
                    print("|", end="")
            count += 1

    """
    create_cells
    ------------------------------------------
    Creates list of cell coordinates for sudoku board
    ------------------------------------------
    chars - list of characters for column cell ID
    nums - list of numbers for row cell ID
    ------------------------------------------
    cells - List of all cell ID's A1, A2, ..., I8, I9
    ------------------------------------------
    Use:
        self.cells = self.create_cells(chars, nums)
    """
    @staticmethod  # Static methods do not use or change self directly, do not pass in self
    def create_cells(chars, nums):
        cells = []
        for a in chars:
            for b in nums:
                cells.append(a + b)  # Appends col and row values to create list of cells A1, A2, ..., I8, I9 in order
        return cells

    """
    permutate
    ------------------------------------------
    Creates list of permutations from iterable item
    ------------------------------------------
    item - iterable item such as a list, in our case it's always a square/box of cells
    ------------------------------------------
    result - All permutations of the iterable item
    ------------------------------------------
    Use:
        perms = self.permutate(numList)
    """

    @staticmethod
    def permutate(item):
        result = []

        for i in range(0, len(item) + 1):  # Loop through all cells in item
            if i == 2:  # Wait until i is 2 to create all permutations of length 2
                for j in permutations(item, i):  # loop though al permutations of item with length of i == 2
                    result.append(j)  # Append each permutation onto the result list

        return result

    """
    constraint
    ------------------------------------------
    Simple check for contraint violation
    ------------------------------------------
    x - value one
    y - value two
    ------------------------------------------
    flag - True if no violation, false if violation
    ------------------------------------------
    Use:
        if puzzle.constraint(x, y): pass
    """
    @staticmethod
    def constraint(x, y):
        return x != y  # If x != y then there is no constraint/violation, return True


    """
    conflicts
    --------------------------------------
    Counts # of conflicts to be used as a heuristic
    in the backtracking algorithm
    --------------------------------------
    sudoku - the sudoku board
    v - the variable (A1, B2, etc) we are counting conflicts for
    val - the value of the cell at var v, (1-9)
    --------------------------------------
    count - the total number of conflicts at variable v
    --------------------------------------
    Use:
        sudoku.conflicts(sudoku, v, val)
    """
    @staticmethod
    def conflicts(sudoku, v, val):
        count = 0  # Count # of conflicts

        for i in sudoku.relCells[v]:  # Loop through all cells related/neighboring cell v
            if len(sudoku.poss[i]) > 1 and val in sudoku.poss[i]:
                # Conflict if neighbor cell i has domain len > 1 AND value assigned to cell v is in the domain of i
                count += 1

        return count
