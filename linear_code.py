from numpy import array, dot, random
from sympy import Matrix

# Returns a code word containing original message bits and parity bits
def generate_code_word(msg_vector, gen_matrix):
    return (array(msg_vector).T @ array(gen_matrix)) % 2

# Returns the syndrome of a potentially corrupted codeword
def compute_syndrome(msg, par_matrix):
    return (array(msg) @ array(par_matrix).T) % 2

# Returns a generator matrix using Gauss-Jordan elimination
def to_rref(par_matrix):
    M = Matrix(par_matrix)
    rref = array(M.rref()[0]) % 2
    rref = array([ row for row in rref if not np.all(row == 0) ])
    return rref.astype(int)

def create_code_set(G, H):
    code_set = []
    for i in range(2**len(G)):
        # Create a message
        msg = []
        msg_str = str(bin(i))[2:]
        for j in range(len(msg_str)):
            msg.append((int(msg_str[j])))

        while len(msg) < len(G):
            msg.insert(0, 0)
        
        # Create a code word
        code_word = generate_code_word(msg, G)
        syndrome = compute_syndrome(code_word, H)

        # Add if codeword is valid
        if (all(bit== 0 for bit in syndrome)):
            code_set.append(array(msg))

    return array(code_set).astype(int)

def cycles_exist(H, n):
    for i in range(n - 1):
        for j in range(i + 1, n):
            if (H[i] @ H[j] >= 2):
                return True
    return False

def remove_cycles(H):
    cycles_exist = True
    while cycles_exist:
        cycles_exist = False
        for i in range(len(H) - 1):
            for j in range(i + 1, len(H)):
                if (H[i] @ H[j] >= 2):
                    cycles_exist = True         
                    random.shuffle(H[j])
        print(H)
    return H
