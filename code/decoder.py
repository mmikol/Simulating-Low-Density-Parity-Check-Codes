from tanner_graph import TannerGraph

# Decodes a corrupted codeword using belief propagation techniques
class Decoder:
    def __init__(self, parity_matrix, decoding_method, max_iterations):
        self.TG = TannerGraph(parity_matrix)
        self.MAX_ITERATIONS = max_iterations
        self.decoding_method = decoding_method

    # Method for a Binary Erasure Channel
    def bec_decode(self, Y):
        # Initialization
        I = 0
        M = Y.copy()
        E = [{} for c in self.TG.check_nodes]

        while True: 
            # Check Messages
            for check in self.TG.check_nodes:
                for i in range(len(check.neighbors)):
                    bit = check.neighbors.pop(i)
                    
                    if check.all_msgs_known(M):
                        E[check.index][bit] = check.sum_bits(M)
                    else:
                        E[check.index][bit] = -1

                    check.neighbors.insert(i, bit)

            # Bit Messages                        
            for bit in self.TG.bit_nodes:
                if M[bit.index] == -1:
                    for check in bit.neighbors:
                        if E[check][bit.index] != -1:
                            M[bit.index] = E[check][bit.index]

            # Test
            if (not -1 in M) or (I == self.MAX_ITERATIONS):
                return (M, I, f'QUIT: {I == self.MAX_ITERATIONS}')
            else: 
                I += 1
    
    # Method for a Binary Symmetric Channel
    def bsc_decode(self, Y):
        # Initialization
        I = 0
        M = Y.copy()
        E = [{} for c in self.TG.check_nodes]

        while True:
            # Check Messages
            for check in self.TG.check_nodes:
                for i in range(len(check.neighbors)):
                    bit = check.neighbors.pop(i)
                    E[check.index][bit] = check.sum_bits(M)
                    check.neighbors.insert(i, bit)
            
            # Bit Messages
            for bit in self.TG.bit_nodes:
                if bit.majority_checks_disagree(E, Y):
                    M[bit.index] = (M[bit.index] + 1) % 2

            equations_satisfied = all(check.sum_bits(M) == 0 for check in self.TG.check_nodes)
            
            if equations_satisfied or (I == self.MAX_ITERATIONS):
                return (M, I, f'QUIT: {I == self.MAX_ITERATIONS}')
            else: 
                I += 1     

    def run(self, arg):
        return {
            'erasure': self.bec_decode,
            'flipping': self.bsc_decode,
        }[self.decoding_method](arg)