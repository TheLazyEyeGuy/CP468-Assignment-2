"""
PSUEDO CODE FOR AC3 ALGORITHM
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
ac3
------------------------------------------
performs arc consistency 3 algorithm on a given sudoku puzzle
------------------------------------------
sudoku - Sudoku object defined in structure.py
------------------------------------------
Returns True if ac3 does not detect inconsistency, False otherwise
------------------------------------------
Use:
    if ac3(sudoku):
        #  cell domains reduced, check if solved. Either print if solved or backtrack if more work needed
    else:
        #  Arc inconsistent, cannot be solved
"""
def ac3(sudoku):
    workList = sudoku.binary  # Set up the work list queue

    while workList:
        print(len(workList))
        x, y = workList.pop(0)  # Pop x and y ID from worklist

        if arc_reduce(sudoku, x, y):
            if len(sudoku.poss[x]) == 0:  # If domain is at 0 for any x puzzle cannot be solved
                return False

            for i in sudoku.relCells[x]:
                if i != x:
                    workList.append([i, x])  # Append all related cells to x (besides those equal to x) to workList

    return True


"""
arc_reduce
--------------------------------------------------
Removes value from the domain of x if it is also in the domain of y
--------------------------------------------------
sudoku - Sudoku object we are working with
x - CellID for item x (A1-I9)
y - CellID for item y (A1-I9)
    x =/= y
--------------------------------------------------
change - True if value removed from domain of x, false if x domain remains unchanged
--------------------------------------------------
use:
    if arc_reduce(sudoku, x, y): Check if domain x == 0, if so alg failed. Else continue code
"""
def arc_reduce(sudoku, x, y):
    change = False

    for i in sudoku.poss[x]: # For all cells in coord x (A1, B1, C1, ..., I9) check contraints with y
        if not any([sudoku.constraint(i, j) for j in sudoku.poss[y]]):  # If domains x and y have conflict remove conflict from domain of x
            sudoku.poss[x].remove(i)
            change = True

    return change


"""
back_track
------------------------------------------------
Backtracking alg for when ac3 fails to solve the puzzle and each
cell has a domain > 0. Recursive.
------------------------------------------------
Base Case: Length of assignment dict == # of cells in puzzle (81)
------------------------------------------------
assignment - Dictonary, uses cellID as key and their assigned value as values
sudoku - Sudoku puzzle object after running through ac3 successfully
------------------------------------------------
result - Returns the finished puzzle
"""
def back_track(assignment, sudoku):
    if len(assignment) == len(sudoku.cells):  # The len of backtrack puzzle == # of cells means we are done BASE CASE
        return assignment

    v = sel_unassigned_var(assignment, sudoku)  # Find unassigned variable

    for value in order_domain_values(sudoku, v):  # For each value in the domain of cellID v
        if sudoku.consistent(assignment, v, value):  # Check if value is consistent
            sudoku.assign(v, value, assignment)  # If consistent assign cell v to value
            result = back_track(assignment, sudoku)  # Recurse algorithm, len(assignment) had increase by 1
            if result:  # Unloads all recursions with value of final assignment
                return result

            # Only here if assignment is None aka: dead end. Backtrack by unassigning cellID v
            sudoku.unassign(v, assignment)

    return False


"""
sel_unassigned_var
---------------------------------------------------
Selects a cell/variable from sudoku that hasnt been assigned a value in assignment dict
---------------------------------------------------
assignment - dict of assigned values to key cellID
sudoku - Sudoku object we are working with
---------------------------------------------------
Returns unassigned cell with least/minimum number of neighbors using lambda function
"""
def sel_unassigned_var(assignment, sudoku):
    unassigned = [i for i in sudoku.cells if i not in assignment]  # All cells i that are not in assignment
    return min(unassigned, key=lambda v: len(sudoku.poss[v]))  # Min cell (aka cell with smallest domain)


"""
lambda v: len(sudoku.poss[v]) is equal to making a function
def func(v):
    return len(sudoku.poss[v])

all above return does is sort the pick the item in unassigned with the fewest neighbors returned by the lambda function
"""

"""
order_domain_values
---------------------------------------------------
Sorts values in the domain of cellID v based on number of conflicts presented by each domain value
---------------------------------------------------
sudoku - Sudoku object we are working with
v - Variable containing cell ID
---------------------------------------------------
return domain of v sorted with lambda function based on # of conflicts
"""
def order_domain_values(sudoku, v):
    if len(sudoku.poss[v]) == 1:
        return sudoku.poss[v]

    return sorted(sudoku.poss[v], key=lambda val: sudoku.conflicts(sudoku, v, val))


"""
Lambda val: sudoku.conflicts(sudoku, v, val) is equal to making a function
def func(val):
    return sudoku.conflicts(sudoku, v, val)
    
all above return does is sort the list sudoku.poss[v] based on the values returned for each v conflict count
in the inline lambda function
"""