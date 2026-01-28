"""
Part 1: Mini exercises
"""

import z3
import pytest

from helper import prove, solve, SAT, UNSAT, PROVED, COUNTEREXAMPLE, UNKNOWN

"""
A. Writing specifications

Consider the absolute value function
that we discussed in lecture:
"""

def abs(x):
    return z3.If(x >= 0, x, -x)

"""
Write a specification for the following properties using Z3.

You can use the PROVED, FAILED, and COUNTEREXAMPLE
constants for assertions in your tests.
For example, if a property fails, use
    assert prove(spec) == COUNTEREXAMPLE

1. If x is greater than or equal to 0, then the absolute value of x is equal to x.

2. If x is less than y, then the absolute value of x is less than the absolute value of y.

3. If x is equal to y + 1, then the absolute value of x is equal to 1 plus the absolute value of y.

4. The absolute value applied twice (absolute value of the absolute value of x) is equal to the absolute value of x.

5. The absolute value of (x + y) is less than or equal to (the absolute value of x) + (the absolute value of y).

The first one is written for you.
"""

def test_abs_1():
    x = z3.Int('x')
    spec = z3.Implies(x >= 0, abs(x) == x)
    assert prove(spec) == PROVED

def test_abs_2():
    x, y = z3.Int('x'), z3.Int('y')
    spec = z3.Implies(x < y, abs(x) < abs(y))
    assert prove(spec) == COUNTEREXAMPLE

def test_abs_3():
    x, y = z3.Int('x'), z3.Int('y')
    spec = z3.Implies(x == y + 1, abs(x) == abs(y) + 1)
    assert prove(spec) == COUNTEREXAMPLE

def test_abs_4():
    x = z3.Int('x')
    spec = abs(abs(x)) == abs(x)
    assert prove(spec) == PROVED

def test_abs_5():
    x, y = z3.Int('x'), z3.Int('y')
    spec = abs(x + y) <= abs(x) + abs(y)
    assert prove(spec) == PROVED

"""
B. Proving assertions

One of the useful things about Z3 is that instead of relying
on testing and assert statements, we can *prove* that an
assertion is true. Once we have a proof, we can omit the assertion
from production code.

6. In the following example we have a player level function that is
supposed to always be between 1 and 100. Rewrite the function
in Z3 and use it to prove that the assertion always holds,
and therefore is safe to omit in production.
You may assume as a precondition that the player level is previously
between 1 and 100 when the function is called.
"""

def update_player_level(player_level, delta):
    if delta < 0:
        result = player_level
    elif player_level + delta > 100:
        result = 100
    else:
        result = player_level + delta

    # This line is the assertion that we want to prove
    assert result >= 1 and result <= 100

    return result

def update_player_level_z3(player_level, delta):
    return z3.If(delta < 0, player_level, z3.If(player_level + delta > 100, 100, player_level + delta))

def test_proving_assertion():
    l, d = z3.Int('l'), z3.Int('d')
    res = update_player_level_z3(l, d)
    spec = z3.Implies(z3.And(1 <= l, l <= 100), z3.And(1 <= res, res <= 100))
    assert prove(spec) == PROVED

"""
7. Based on this experience, do you think it would it be possible to
automatically do the translation from update_player_level to Z3?

Why or why not?
===== ANSWER Q7 BELOW =====
The translation was easy to do here since only conditionals and arithmetic were involved, but it might be harder if the function involved a loop or other logic that would be hard to efficiently implement in Z3.
===== END OF Q7 ANSWER =====
"""

"""
C. Rectangle collision calculator

Let's write a function that is able to calculate
whether two rectangles collide.

Each rectangle is given by its center (x, y) and its width and height.
The circle is given by its center (x, y) and its radius.
Both shapes have a velocity (vx, vy) that describes how much they
move in the x- and y-directions every second.

8. Write a function rectangle_position that calculates
the position of a rectangle at a given time t,
as a Z3 expression.

9. Write a function rectangles_overlap that creates a formula
that is satisfiable if the two rectangles overlap,
and unsatisfiable otherwise.

**Important additional instructions:**
To make this part more interesting: instead of checking for
overlap directly, create new variables for the point of overlap.
(This is a more general technique that
can be used for any shape, not just rectangles!)

10. Write a function rectangles_collide that checks whether
two rectangles collide at any point in time t >= 0.
It should return a Python boolean (True or False).
"""

def rectangle_position(x, y, vx, vy, t):
    """
    x, y, vx, vy: Python integers
    t: a Z3 real number

    returns: a tuple of two Z3 expressions
        (x, y)
    that represents the center of the rectangle at time t.
    """
    # TODO
    raise NotImplementedError

def rectangles_overlap(
    x1, y1, width1, height1,
    x2, y2, width2, height2,
):
    """
    x1, y1, width1, height1: Z3 expressions
    x2, y2, width2, height2: Z3 expressions

    returns: a Z3 expression that is satisfiable if the two
    rectangles overlap.

    Note: the time is not given as an argument, because it should be
    included in the expressions for the rectangle's position.
    """
    # TODO
    raise NotImplementedError

def rectangles_collide(
    x1, y1, width1, height1, vx1, vy1,
    x2, y2, width2, height2, vx2, vy2,
):
    """
    x1, y1, width1, height1, vx1, vy1: Python integers
    x2, y2, width2, height2, vx2, vy2: Python integers

    returns: True if the two rectangles collide at any point in time.

    This function should use our solve function.
    """
    # TODO
    raise NotImplementedError

"""
11. Write a unit test for rectangles_collide to
check if it seems to be working.
"""

@pytest.mark.skip
def test_rectangles_collide():
    # TODO
    raise NotImplementedError

"""
12. Do you think this is the best way to check for collisions in general?
For example, for collision detection in a game?
What about for a simple prototype?
Discuss one benefit and one drawback of this approach.
"""

"""
13. (Extra credit)
Generalize your functions in parts 8-11 to work for any shape
(for example, a circle or a triangle), using Python classes.
Implement one other shape in this system.
"""
