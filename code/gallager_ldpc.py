from numpy import zeros, ones, random, dot

# Constructs a Gallager LDPC Parity Matrix given dimensions
class GallagerLDPC:
    def __init__(self, num_cols, col_weight, row_weight, cycles_allowed):
        # Initialize
        num_rows = (num_cols * col_weight) // row_weight
        num_sets = num_rows // col_weight

        self.H = zeros((num_rows, num_cols))

        # Generate First Set
        k = 0
        code_bits_arr = ones((1, row_weight))
        for row in range(col_weight):
            self.H[row, k:k + wr] = code_bits_arr
            k += row_weight
        
        # Generate Remaining Sets
        perm_arr = self.H[:col_weight,:num_cols].copy().T
        row = col_weight
        for sets in range(num_sets - 1):
            random.shuffle(perm_arr)
            self.H[row:row + wr - 1,:] = perm_arr.T
            row += (row_weight - 1)
         
        if not cycles_allowed:
            cycles_exist = True
            while cycles_exist:
                cycles_exist = False

                for i in range(num_cols - 1):
                    for j in range(i + 1, num_cols):
                        if dot(self.H[:,i], self.H[:,j]) >= 2:
                            cycles_exist = True
                            random.shuffle(self.H[:,j])

        self.H = self.H.astype(int)