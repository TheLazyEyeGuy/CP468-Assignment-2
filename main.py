from structure import Sudoku
from functools import reduce

f = open("sudoku", "r")
text = f

numbers = []
for line in f:
    numbers.append(line.strip().split())

f.close()

flatNums = reduce(lambda z, y :z + y, numbers)

sudoku = Sudoku(flatNums)
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


