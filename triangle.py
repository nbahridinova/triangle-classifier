"""Triangle classifier: classifies a triangle based on three side lengths."""
from math import isclose

def classify_triangle(a, b, c):
    """
    Return one of:
      - 'Equilateral'
      - 'Isosceles'
      - 'Scalene'
    and add ' Right' if it's also a right triangle.
    Return 'NotATriangle' for invalid inputs.
    """
    # convert/validate
    try:
        x, y, z = sorted(float(s) for s in (a, b, c))
    except (TypeError, ValueError):
        return "NotATriangle"
    if x <= 0 or y <= 0 or z <= 0:
        return "NotATriangle"
    if x + y <= z:  # triangle inequality
        return "NotATriangle"

    # side-type
    if isclose(x, y) and isclose(y, z):
        kind = "Equilateral"
    elif isclose(x, y) or isclose(y, z) or isclose(x, z):
        kind = "Isosceles"
    else:
        kind = "Scalene"

    # right check
    right = isclose(x*x + y*y, z*z, rel_tol=1e-9, abs_tol=1e-9)
    return f"{kind}{' Right' if right else ''}"
