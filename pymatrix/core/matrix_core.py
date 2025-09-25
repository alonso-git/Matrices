from fractions import Fraction
from ..utils.matrix_size import MatrixSize

class Matrix():
    __size: MatrixSize
    __matrix: list[list[Fraction]]

    def __init__(self, matrix: list[list[Fraction]] | None = None):
        if matrix:
            if len({len(row) for row in matrix}) == 1:
                self.__matrix = matrix

                self.__size = MatrixSize(len(matrix), len(matrix[0]))
            else:
                raise ValueError("Matrix is incomplete")
        else:
            raise ValueError("Matrix not found")

    def __repr__(self) -> list[list[Fraction]]:
        # Add a nice str formatting
        return self.__matrix
    
    def __iter__(self):
        return self.__matrix
    
    def __sub__(self, mat):
        pass

    # Getters y setters
    
    @property
    def dim(self):
        return self.__size