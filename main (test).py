import re
import numpy as np
from fractions import Fraction
from dataclasses import dataclass
from matrix_gauss_jordan import GaussJordanMatrix


# Testing class
# Example equations for testing
equations: list[str] = [
    "x+y+z+a=6",
    "2x-y+3z+a=9",
    "-x+2y-z+a=2",
    "2x-3y+z-2a=12"
]

matrix = GaussJordanMatrix(equations)

# NOTES: Change NumPy arrays to Fraction objects
fraction_str_result = [[str(Fraction(x)) for x in row] for row in matrix.solved]

num_cols = matrix.size.n
col_widths = [0] * num_cols
for j in range(num_cols):
    col_widths[j] = max(len(row[j]) for row in fraction_str_result)

for row in fraction_str_result:
    row_str = "  ".join(f"{val:{col_widths[i]}}" for i, val in enumerate(row[:-1]))
    print(f"{row_str} | {row[-1]}")

print(matrix)
print(matrix.size)
print(matrix.variables)
