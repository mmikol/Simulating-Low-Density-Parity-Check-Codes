from numpy import zeros
from random import shuffle
from math import factorial

class MackayNealLDPC:
    def __init__(self, code_len, rate, col_dist, row_dist, cycles_allowed):
        num_rows = int(round((code_len * (1 - rate))))
       
        # Initialize
        a = []
        for i in range(1, len(col_dist) + 1):
            for j in range(int(round(col_dist[i - 1] * code_len))):
                a.append(i)
        
        b = []
        for i in range(1, len(row_dist) + 1):
            for j in range(int(round(row_dist[i - 1] * num_rows))):
                b.append(i)

        self.H = zeros((int(round((code_len * (1 - rate)))), code_len))
        
        # Construct
        while True:
            B = b.copy()

            for i in range(code_len):
                c = [1 if count < a[i] else 0 for count in range(len(b))]
                
                shuffle(c)

                (I, subset_found) = (0, True)
                max_I = factorial(num_rows) // (factorial(a[i]) * factorial(num_rows - a[i]))
                while not all(c[j] <= B[j] for j in range(len(b))):
                    shuffle(c)
                    I += 1

                    if I >= max_I:
                        subset_found = False
                        break

                if subset_found:
                    self.H[:, i] = c
                    B = [B[j] - c[j] for j in range(len(b))]

            if all(x == 0 for x in B):
                break