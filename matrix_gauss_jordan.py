class GaussJordanMatrix():
    __eq_system: list[str] = []
    __solved_matrix: np.ndarray = np.array([])
    __augmented_matrix: np.ndarray = np.array([])
    __size: MatrixSize = MatrixSize()
    __variables: list[str] = []

    # Receive equations system
    def __init__(self, eq_system: list[str]) -> None:
        if self.validate_equations(eq_system):
            self.__eq_system = eq_system
        else:
            raise ValueError("Format is not accepted")
        
        self.__size.m = len(self.__eq_system)

        self.gauss_jordan_elimination(self.eq_system_to_matrix())

    # Overloaded methods
    def __str__(self) -> str:
        if self.__augmented_matrix.size == 0:
            return "Empty matrix"

        A = self.__augmented_matrix
        num_rows, num_cols = A.shape

        # Convert all elements to strings with sign alignment
        str_matrix = []
        for row in A:
            new_row = []
            for x in row:
                s = f"{x:.3g}"
                if not s.startswith("-"):  # add leading space for positive numbers
                    s = " " + s
                new_row.append(s)
            str_matrix.append(new_row)

        # Compute max width of each column
        col_widths = [max(len(str_matrix[i][j]) for i in range(num_rows)) for j in range(num_cols)]

        # Build formatted string
        lines = []
        for row in str_matrix:
            row_str = "  ".join(f"{val:{col_widths[i]}}" for i, val in enumerate(row[:-1]))
            # Add vertical bar before last column
            lines.append(f"{row_str} | {row[-1]}")

        return "\n".join(lines)

    # Getters and setters
    @property
    def size(self):
        return self.__size
    
    @property
    def variables(self):
        return self.__variables
    
    @property
    def result(self):
        # Change to the proposed {variable:value, ...} format
        return self.__solved_matrix   

    @property
    def solved(self):
        return self.__solved_matrix

    # Matrix operations
    def swap_rows(self, idx_1: int, idx_2: int = 0):
        try:
            self.__solved_matrix[[idx_1, idx_2]]= self.__solved_matrix[[idx_2, idx_1]]
        except Exception as e:
            raise e
    
    def multiply_row(self, factor: int, idx: int):
        try:
            self.__solved_matrix[idx] *= factor
        except Exception as e:
            raise e
    
    # NOT CURRENTLY USED: Useful when you follow classic Gauss-Jordan logic, instead of scaled elimination
    def sum_factor_other_row(self, factor: int, idx_target: int, idx_by_factor: int):
        try:
            row_by_factor = self.__solved_matrix[idx_by_factor] * factor
            self.__solved_matrix[idx_target] += row_by_factor
        except Exception as e:
            raise e

    def sum_two_factor_rows(self, elim_factor: int | float, idx_target: int, pivot_factor: int|float, idx_pivot: int):
        elim_factor = -elim_factor

        target_row_by_factor = self.__solved_matrix[idx_target] * pivot_factor
        pivot_row_by_factor = self.__solved_matrix[idx_pivot] * elim_factor

        try:
            self.__solved_matrix[idx_target] = target_row_by_factor + pivot_row_by_factor
        except Exception as e:
            raise e
        
    # Equations' logic
    def validate_equations(self, eq_system: list[str]):
        # Pattern to match an equation of the shape -ax+by-cz=-d (ie. -x+2y-12z=35 is valid as well as -x=2)
        pattern = r"^[-]?\d*[a-z]([+-]\d*[a-z])*(=[-+]?\d+)$"

        # Reject the whole system if any equation is invalid
        for num, eq in enumerate(eq_system):
            if not isinstance(re.match(pattern, eq), re.Match):
                print(f"Equation {num+1} is invalid")
                return False
        
        # If all equations are valid, returns the system normalized
        return True
    
    def eq_system_to_matrix(self):
        raw_data = []

        for eq in self.__eq_system:
            # Extract pairs coefficient,variable and result
            pairs = re.findall(r"([+-]?\d*)([a-z])", eq)
            constant = re.findall(r"(=)([+-]?\d+)", eq)

            # Wrap the information on a raw format
            raw_data.append([list(pair) for pair in pairs] + [constant[0][1]]   )

        # Store number of variables in the system
        self.__size.n = len(raw_data[0])

        for row in raw_data:
            variables: list[str] = []
            for pair in row[:-1]:
                # Normalize special cases (1, -1)
                if pair[0] == '' or pair[0] == '+':
                    pair[0] = '1'
                elif pair[0] == '-':
                    pair[0] = '-1'

                variables.append(pair[1])
            
            # Store the list of variables
            self.__variables = variables if len(self.__variables) < len(variables) else self.__variables



        # Transform raw data into an int matrix
        # augmented_matrix = np.array([[int(pair[0]) for pair in row[:-1]] + [int(row[-1])] for row in raw_data])

        augmented_matrix = np.array([[float(pair[0]) for pair in row[:-1]] + [float(row[-1])] for row in raw_data])

        self.__augmented_matrix = np.array(augmented_matrix)

        return augmented_matrix
    
    def gauss_jordan_elimination(self, mat: np.ndarray):
        # Copy matrix and assign an alias for object attribute
        self.__solved_matrix = np.array(mat, dtype=float)
        A = self.__solved_matrix

        # Instead of normalizing, use factors of the rows to preserve precision
        for m in range(self.__size.m):
            # Use largest absolute value as pivot (partial pivoting)
            max_row_idx = np.argmax(A[m:, m]) + m
            self.swap_rows(m, int(max_row_idx))

            # Eliminate column values except the current row
            for i in range(self.__size.m):
                if i == m:
                    continue

                self.sum_two_factor_rows(A[i,m], i, A[m,m], m)

        # Normalize pivots after solving
        for i in range(self.__size.m):
            pivot = 1 / A[i,i]
            self.multiply_row(pivot, i)