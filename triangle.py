#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Triangle Project Code.


# triangle(a, b, c) analyzes the lengths of the sides of a triangle
# (represented by a, b and c) and returns the type of triangle.
#
# It returns:
#   'equilateral'  if all sides are equal
#   'isosceles'    if exactly 2 sides are equal
#   'scalene'      if no sides are equal
#
# The tests for this method can be found in
#   about_triangle_project.py
# and
#   about_triangle_project_2.py
#
def triangle(x, y, z):
    # DELETE 'PASS' AND WRITE THIS CODE
    if x + y >= z > 0 and y + z >= x > 0 and x + z > y:
        if x==y==z and x != 0:
            return 'equilateral'
        elif x == y or y == z or z == x:
            return 'isosceles'
        elif x != y and x != z and y != z:
            return 'scalene'
        else:
            raise TriangleError
    else:
        raise TriangleError

# Error class used in part 2.  No need to change this code.
class TriangleError(StandardError):
    pass
