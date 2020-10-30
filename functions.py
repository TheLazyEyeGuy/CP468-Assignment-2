def printsud(sudoku):
    boxx = 0
    boxy = 0
    for i in range(9):
        if boxy == 3:
            print("------+-------+-----")
            boxy=0
        for j in range(9):
            if boxx == 3:
                print("|", end=" ")
                boxx=0
            print(sudoku[i][j], end=" ")
            boxx+=1
        print()
        boxy+=1
        boxx=0