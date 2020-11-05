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


def ac3(sudoku):
    workList = sudoku.binary  # Set up the work list queue

    while workList:
        x, y = workList.pop(0)  # Pop x and y ID from worklist

        if arc_reduce(sudoku, x, y):
            if len(sudoku.poss[x]) == 0:  # If domain is at 0 for any x puzzle cannot be solved
                return False

            for i in sudoku.relCells[x]:
                if i != x:
                    workList.append([i, x])  # Append all related cells to x (besides those equal to x) to workList

    return True


def arc_reduce(sudoku, x, y):
    change = False

    for i in sudoku.poss[x]: # For all cells in coord x (A, B, C, ..., I) check contraints with y
        if not any([sudoku.constraint(i, j) for j in sudoku.poss[y]]):  # If domains x and y have conflict remove conflict from domain of x
            sudoku.poss[x].remove(i)
            change = True

    return change

def backtrack(assignment, sudoku):
    if len(assignment) == len(sudoku.cells):  # The len of backtrack puzzle == # of cells means we are done BASE CASE
        return assignment

    v = selUnassignedVar(assignment, sudoku)

    for value in orderDomainValues(sudoku, v):
        if sudoku.consistent(assignment, v, value):
            sudoku.assign(v, value, assignment)
            result = backtrack(assignment, sudoku)
            if result:
                return result

            sudoku.unassign(v, assignment)

    return False

def selUnassignedVar(assignment, sudoku):
    unassigned = [i for i in sudoku.cells if i not in assignment]
    return min(unassigned, key=lambda v: len(sudoku.poss[v]))

def orderDomainValues(sudoku, v):
    if len(sudoku.poss[v]) == 1:
        return sudoku.poss[v]

    return sorted(sudoku.poss[v], key=lambda val: sudoku.conflicts(sudoku, v, val))