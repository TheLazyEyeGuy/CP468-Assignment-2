from structure import Sudoku

f = open("sudoku", "r")
text = f

numbers = []
for line in f:
    numbers.append(line.strip().split())
f.close()
print(numbers)
"""
sudoku = Sudoku(numbers)
sudoku.print_sud()  # prints sudoku
box = sudoku.find_location(4, 4)
print(box)
"""



