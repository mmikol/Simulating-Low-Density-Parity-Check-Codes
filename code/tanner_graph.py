class TannerGraph:
    def __init__(self, parity_matrix):
        # Generate Check Nodes
        self.check_nodes = []
        for check_index in range(len(parity_matrix)):
            bit_indeces = [i for (i, e) in enumerate(parity_matrix[check_index]) if e == 1]
            self.check_nodes.append(_CheckNode(check_index, bit_indeces))
        
        # Generate Bit Nodes
        self.bit_nodes = []
        for bit_index in range(len(parity_matrix[0])):
            check_indeces = [c.index for c in self.check_nodes if bit_index in c.neighbors]
            self.bit_nodes.append(_BitNode(bit_index, check_indeces))        
    
    # For debugging purposes
    def toString(self):
        checks = f'Check Nodes: {[node.neighbors for node in self.check_nodes]}'
        bits = f'Bit Nodes: {[node.neighbors for node in self.bit_nodes]}'
        return f'{checks}\n{bits}'

class Node():
    def __init__(self, index, neighbors):
        self.index = index
        self.neighbors = neighbors

class _CheckNode(Node):
    def __init__(self, index, bit_nodes):
        super().__init__(index, bit_nodes)
    
    def sum_bits(self, M):
        sum = 0
        for bit in self.neighbors:
            sum += M[bit]
        return sum % 2

    def all_msgs_known(self, M):
        return all([bit != -1 for bit in self.neighbors])

class _BitNode(Node):
    def __init__(self, index, check_nodes):
        super().__init__(index, check_nodes)
            
    def majority_checks_disagree(self, E, Y):
        majority = (len(self.neighbors) // 2) + 1
        disagreements = 0
        
        for check in self.neighbors:
            if E[check][self.index] != Y[self.index]:
                disagreements += 1

            if disagreements >= majority:
                return True
    
        return False