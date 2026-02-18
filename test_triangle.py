# test_triangle.py
import unittest
import math
from triangle import classify_triangle

class TestTriangle(unittest.TestCase):

    def test_equilateral(self):
        self.assertEqual(classify_triangle(3, 3, 3), "Equilateral")

    def test_isosceles(self):
        self.assertEqual(classify_triangle(5, 5, 8), "Isosceles")

    def test_scalene(self):
        self.assertEqual(classify_triangle(4, 5, 6), "Scalene")

    def test_right_scalene(self):
        self.assertEqual(classify_triangle(3, 4, 5), "Scalene Right")

    def test_isosceles_right(self):
        self.assertEqual(classify_triangle(1, 1, math.sqrt(2)), "Isosceles Right")

    def test_not_a_triangle_zero(self):
        self.assertEqual(classify_triangle(0, 1, 1), "NotATriangle")

    def test_not_a_triangle_inequality(self):
        self.assertEqual(classify_triangle(1, 2, 3), "NotATriangle")

if __name__ == "__main__":
    unittest.main()
