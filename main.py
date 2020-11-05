from structure import Sudoku
from functools import reduce
from ac3 import ac3, backtrack

f = open("sudoku", "r")
text = f

numbers = []
for line in f:
    numbers.append(line.strip().split())

f.close()

# Reduce list of numbers using inline lambda function lambda(z, y) = z + y for ever value in numbers
flatNums = reduce(lambda z, y :z + y, numbers)

# Convert flattened list into a sudoku puzzle
sudoku = Sudoku(flatNums)
print("ORIGINAL: ")
sudoku.printSud()
# Run ac3
if ac3(sudoku):
    if sudoku.solved():  # Check if each domain length is 1, if so puzzle solved using a3 algorithm alone
        print("Puzzle solved, print output: ")
        sudoku.printSol()
    else:
        assignment = {}

        for i in sudoku.cells:
            if len(sudoku.poss[i]) == 1:
                assignment[i] = sudoku.poss[i][0]  # If we found cell value already, assign it

            assignment = backtrack(assignment, sudoku)  # Use backtrack alg on ac3 reduced domain space

        for i in sudoku.poss:
            sudoku.poss[i] = assignment[i] if len(i) > 1 else sudoku.poss[i]

        if assignment:
            print("Solution has been found using backtracking algorithm: ")
            sudoku.printSol()
        else:
            print("There is no solution for this puzzle")
else:  # ac3 failed
    print("The puzzle entered was found to be arc inconsistent with the ac3 algorithm")
#sudoku.print_sud()

#sudoku.AC3()

#sudoku.print_sud()


"""
main.py -> Opens file, converts to sudoku object, calls ac3
AC alg.py -> ac3, arc_reduce, backtrack, select_unassigned, order_domain_value
sudoku.py -> sudoku_class -> init(self.list, self.domains, self.skimmed, self.contraints, self.poss
    -> build_constraints, build_possibilities, solved, complete, consistent, assign, unassign, forward_check, 
    premutate, combine, compare, conflict
"""


