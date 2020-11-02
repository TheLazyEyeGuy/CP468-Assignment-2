from functions import printsud
from structure import Sudoku

f = open("sudoku", "r")
text = f
numbers = []
for line in f:
    nine = line.strip()
    numbers.append(nine.split())
sudoku = Sudoku(numbers)

printsud(sudoku)


