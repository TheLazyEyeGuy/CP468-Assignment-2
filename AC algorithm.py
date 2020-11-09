"""
Input:
   A set of variables X
   A set of domains D(x) for each variable x in X. D(x) contains vx0, vx1... vxn, the possible values of x
   A set of unary constraints R1(x) on variable x that must be satisfied
   A set of binary constraints R2(x, y) on variables x and y that must be satisfied

 Output:
   Arc consistent domains for each variable.

 function ac3 (X, D, R1, R2)
     // Initial domains are made consistent with unary constraints.
     for each x in X
         D(x) := { vx in D(x) | vx satisfies R1(x) }
     // 'worklist' contains all arcs we wish to prove consistent or not.
     worklist := { (x, y) | there exists a relation R2(x, y) or a relation R2(y, x) }

     do
         select any arc (x, y) from worklist
         worklist := worklist - (x, y)
         if arc-reduce (x, y)
             if D(x) is empty
                 return failure
             else
                 worklist := worklist + { (z, x) | z != y and there exists a relation R2(x, z) or a relation R2(z, x) }
     while worklist not empty

 function arc-reduce (x, y)
     bool change = false
     for each vx in D(x)
         find a value vy in D(y) such that vx and vy satisfy the constraint R2(x, y)
         if there is no such vy {
             D(x) := D(x) - vx
             change := true
         }
     return change
"""
"""
function ac3 (sudoku, sudoku.domains, [1,2,3,4,5,6,7,8,9], x != columnx and x != rowx and x != boxx)
     // Initial domains are made consistent with unary constraints.
     for i=0: i+1: i<80
         sudoku.domains[i] := [1,2,3,4,5,6,7,8,9] # the domain for every square is 1-9
        
     // 'worklist' contains all arcs we wish to prove consistent or not.
     worklist := { sudoku.number[x] not in COLUMNX AND ROWX AND BOXX}
     
     #run through sudoku.list and put every value that isnt 0(nothing) as the domain for that index
     for i in range(9):
        for j in range(9):
            if sudoku.list[i][j] != 0:
                sudoku.domain[i][j] = sudoku.list[i][j]

     do
         select any arc (x, y) from worklist  # implement a queue data type? or would a list work as well?
         worklist := worklist - (x, y)
         if arc-reduce (x, sudoku.boxes[x],sudoku.rows[x],sudoku.columns[x])
             if sudoku.domain[x] is empty  # if this happens the sudoku is invalid, go to next arangement in frontier
                 return false
             else
                 worklist := worklist + { (z, x) | z != y and there exists a relation R2(x, z) or a relation R2(z, x) } #no clue what z would be
     while worklist not empty

 function arc-reduce (x, y)
     bool change = false
     for each vx in sudoku.domains[x]
         find a value vy in D(y) such that vx and vy satisfy the constraint R2(x, y)
         #this should be the checking of every value in the domain to see if it is viable
         if there is no such vy {
             D(x) := D(x) - vx
             change := true
         }
     return change

"""