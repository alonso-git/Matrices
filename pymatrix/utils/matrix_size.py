from dataclasses import dataclass
from ..core.exceptions import MatrixDimensionError
    
@dataclass(frozen=True)
class MatrixSize:
    # Declare both dimensions
    m: int
    n: int

    # Initialize with user input
    def __post_init__(self):
        # Validate input
        if self.m <= 0 or self.n <= 0:
            raise MatrixDimensionError(
                f"Matrix dimensions must be positive integers, but got ({self.m}, {self.n})"
            )

    def __repr__(self) -> str:
        return f"Matrix size: {self.m} rows x {self.n} cols"
    
    def __str__(self) -> str:
        return f"({self.m},{self.n})"