from structure import Sudoku

f = open("sudoku", "r")
text = f

numbers = []
for line in f:
    nine = line.strip()
    numbers.append(nine.split())
f.close()
sudoku = Sudoku(numbers)
box = sudoku.find_location(4, 4)
print(box)

sudoku.print_sud()


