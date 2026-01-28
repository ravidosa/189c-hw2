"""
Four numbers game solver

In the second part of the homework, we will implement
a solver for the four numbers game.

=== Four numbers game ===

The game works as follows:
First, I secretly think of two positive integers x and y.
I don't tell you what they are, but instead I give you four
numbers:
    a, b, c, d
and tell you that they are the values of the sum, difference,
product, and quotient (x+y, x-y, xy, and x/y), in an unknown order.
Assume that the difference is nonnegative and the quotient is a whole number.

Can you figure out what x and y are?

=== Examples ===

Four numbers: 20, 95, 105, 500
Solution: x = 100, y = 5.

Four numbers: 2, 6, 18, 72
Solution: x = 12, y = 6.

Four numbers: 0, 1, 1, 2
Solution: x = 1, y = 1.

=== Input ===

Your solver should take 4 numbers as input from the user.
For simplicity, assume that all 4 numbers are nonnegative integers.
You can get input in Python using the `input` function:
    num1 = int(input("First number: "))

=== Output, Stage 1 ===

Use Z3 to output the
solution (x and y), if it finds one,
or say that there are no solutions.
You can assume that x and y are positive integers.

The first function

    solve_stage1(a, b, c, d)

should, when given four integers a, b, c, d, return a solution

    x, y

if there is at least one solution, or None if there is no solution.

Second, the function

    run_interactive()

should provide an interactive version: it should prompt the user for 4 numbers, then display as output the correct answers x and y.
It should use an auxiliary function `get_input()` to get the input from the user.

=== Output, Stage 2 ===

Use Z3 to determine whether there are any *other* solutions, besides
the one that you found in the first stage.

The function

    solve_stage2(a, b, c, d, x, y)

should return a Python string

    "multiple", "unique", or "none"

depending on whether multiple solutions exist.
Update your run_interactive() version to also show the output of solve_stage2.

=== Helper function ===

Please use the helper function get_solution
in helper.py that will be useful for this part.
If the spec is satisfiable (SAT), it will return
a solution that you can use to get the values of x and y:
    x = Int('x')
    x_val = get_solution(spec)[x]

=== Try it out! ===

Try out your game by running
    python3 part2.py

to see if it works!

If you like, you can also write unit tests, but this
is not required for this part.
"""

import z3
import pytest

from helper import solve, get_solution, SAT, UNSAT, UNKNOWN
from itertools import permutations

def get_input():
    a = input("a: ")
    b = input("b: ")
    c = input("c: ")
    d = input("d: ")
    return a, b, c, d

def solve_stage1(a, b, c, d):
    x, y = z3.Int('x'), z3.Int('y')
    pos_constr = z3.And(x > 0, y > 0)
    sum_val = x + y
    diff_val = x - y
    prod_val = x * y
    quot_val = z3.Int('q')
    div_constr = z3.And(x == quot_val * y, quot_val > 0)

    for perm in permutations([a, b, c, d]):
        spec = z3.And(pos_constr, sum_val == perm[0], diff_val == perm[1], prod_val == perm[2], quot_val == perm[3], div_constr)
        model = get_solution(spec)
        if model:
            return (model[x], model[y])

def run_interactive():
    print("=== Input ===")
    a, b, c, d = get_input()
    print("=== Stage 1 ===")
    prev_sol = solve_stage1(a, b, c, d)
    if prev_sol:
        x1, y1 = prev_sol
        print(f"Solution 1: x = {x1}, y = {y1}")
        print("=== Stage 2 ===")
        new_sol = solve_stage2(a, b, c, d, (x1, y1))
        if new_sol:
            x2, y2 = new_sol
            print(f"Solution 2: x = {x2}, y = {y2}")
        else:
            print("Unique solution")
    else:
        print("No solutions")

def solve_stage2(a, b, c, d, prev_sol):
    x_, y_ = prev_sol
    x, y = z3.Int('x'), z3.Int('y')
    pos_constr = z3.And(x > 0, y > 0)
    sum_val = x + y
    diff_val = x - y
    prod_val = x * y
    quot_val = z3.Int('q')
    div_constr = z3.And(x == quot_val * y, quot_val > 0)
    unique_constr = z3.Or(x != x_, y != y_)

    for perm in permutations([a, b, c, d]):
        spec = z3.And(pos_constr, unique_constr, sum_val == perm[0], diff_val == perm[1], prod_val == perm[2], quot_val == perm[3], div_constr)
        model = get_solution(spec)
        if model:
            return (model[x], model[y])

if __name__ == "__main__":
    run_interactive()
