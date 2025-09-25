from fractions import Fraction
from ..utils.matrix_size import MatrixSize
from ..core.exceptions import MatrixExistsError, MatrixDimensionError

class Matrix():
    # Define basic attributes for matrix
    __size: MatrixSize
    __matrix: list[list[Fraction]]

    # Initialize
    def __init__(self, matrix: list[list[Fraction]] | None = None):
        if matrix:
            if len({len(row) for row in matrix}) == 1:
                self.__matrix = matrix

                self.__size = MatrixSize(len(matrix), len(matrix[0]))
            else:
                raise MatrixDimensionError(
                    "Rows must contain the same number of elements"
                )
        else:
            raise MatrixExistsError(
                "Matrix not found"
            )

    def __repr__(self) -> list[list[Fraction]]:
        # Add a nice str formatting
        return self.__matrix

    # Getters y setters
    @property
    def dim(self):
        return self.__size