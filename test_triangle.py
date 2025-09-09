# test_triangle.py
from triangle import classify_triangle
import math

def test_equilateral():
    assert classify_triangle(3, 3, 3) == "Equilateral"

def test_isosceles():
    assert classify_triangle(5, 5, 8) == "Isosceles"

def test_scalene():
    assert classify_triangle(4, 5, 6) == "Scalene"

def test_right_scalene():
    assert classify_triangle(3, 4, 5) == "Scalene Right"

def test_isosceles_right():
    assert classify_triangle(1, 1, math.sqrt(2)) == "Isosceles Right"

def test_not_a_triangle_zero():
    assert classify_triangle(0, 1, 1) == "NotATriangle"

def test_not_a_triangle_inequality():
    assert classify_triangle(1, 2, 3) == "NotATriangle"
