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
    return (x + vx * t, y + vy * t)

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
    px = z3.Real("px")
    py = z3.Real("py")

    in_rect1_constr = z3.And(abs(px - x1) <= width1 / 2, abs(py - y1) <= height1 / 2)
    in_rect2_constr = z3.And(abs(px - x2) <= width2 / 2, abs(py - y2) <= height2 / 2)
    return z3.And(in_rect1_constr, in_rect2_constr)

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
    t = z3.Real("t")
    x1t, y1t = rectangle_position(x1, y1, vx1, vy1, t)
    x2t, y2t = rectangle_position(x2, y2, vx2, vy2, t)
    overlap_constr = rectangles_overlap(x1t, y1t, width1, height1, x2t, y2t, width2, height2)
    spec = z3.And(t >= 0, overlap_constr)
    return solve(spec) == SAT

"""
11. Write a unit test for rectangles_collide to
check if it seems to be working.
"""

def test_rectangles_collide():
    assert rectangles_collide(0, 0, 10, 10, 0, 0,
                              5, 0, 10, 10, 0, 0)
    assert not rectangles_collide(0, 0, 10, 10, 0, 0,
                              20, 0, 10, 10, 0, 0)
    assert rectangles_collide(0, 0, 10, 10, 1, 0,
                              30, 0, 10, 10, -1, 0)
    assert not rectangles_collide(0, 0, 10, 10, 1, 0,
                              0, 30, 10, 10, -1, 0)
    assert rectangles_collide(0, 0, 10, 10, 1, 0,
                              20, 0, 10, 10, 0, 0)
    assert not rectangles_collide(0, 0, 10, 10, -1, 0,
                              30, 0, 10, 10, 1, 0)

"""
12. Do you think this is the best way to check for collisions in general?
For example, for collision detection in a game?
What about for a simple prototype?
Discuss one benefit and one drawback of this approach.
===== ANSWER Q13 BELOW =====
One benefit would be that this implementation not only answers whether not not two rectangles collide, but finds the precise time of collision in the case where they do. However, this approach would be far too slow to be useful for real-time collision detection.
===== END OF Q13 ANSWER =====
"""

"""
13. (Extra credit)
Generalize your functions in parts 8-11 to work for any shape
(for example, a circle or a triangle), using Python classes.
Implement one other shape in this system.
"""
class Shape:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def position(self, t):
        return (self.x + self.vx * t, self.y + self.vy * t)
    def contains(self, px, py):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, x, y, w, h, vx, vy):
        super().__init__(x, y, vx, vy)
        self.w = w
        self.h = h
    def position(self, t):
        xt, yt = super().position(t)
        return Rectangle(xt, yt, self.w, self.h, self.vx, self.vy)
    def contains(self, px, py):
        return z3.And(abs(px - self.x) <= self.w / 2, abs(py - self.y) <= self.h / 2)

class Circle(Shape):
    def __init__(self, x, y, r, vx, vy):
        super().__init__(x, y, vx, vy)
        self.r = r
    def position(self, t):
        xt, yt = super().position(t)
        return Circle(xt, yt, self.r, self.vx, self.vy)
    def contains(self, px, py):
        return (px - self.x) ** 2 + (py - self.y) ** 2 <= self.r ** 2

def shapes_overlap(s1, s2):
    px = z3.Real("px")
    py = z3.Real("py")
    return z3.And(s1.contains(px, py), s2.contains(px, py))

def shapes_collide(s1, s2):
    t = z3.Real("t")
    s1t, s2t = s1.position(t), s2.position(t)
    overlap_constr = shapes_overlap(s1t, s2t)
    spec = z3.And(t >= 0, overlap_constr)
    return solve(spec) == SAT

def test_shapes_collide():
    r1 = Rectangle(0, 0, 10, 10, 1, 0)
    r2 = Rectangle(20, 0, 10, 10, -1, 0)
    assert shapes_collide(r1, r2)

    c1 = Circle(0, 0, 5, 1, 0)
    c2 = Circle(15, 0, 5, 0, 0)
    assert shapes_collide(c1, c2)

    assert shapes_collide(r1, c2)