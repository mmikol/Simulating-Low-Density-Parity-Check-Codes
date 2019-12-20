import linear_code as lc
import numpy as np
import random
import datetime
from commpy import bec, bsc
from mackay_neal_ldpc import MackayNealLDPC
from gallager_ldpc import GallagerLDPC
from decoder import Decoder

# Simulator will run BEC simulations over 9 incrementing corruption probabilities beginning with 0.1
class Simulator:
    def __init__(self, H, num_tests, decoding_method, max_iterations=1000):
        self.num_tests = num_tests if num_tests % 10 == 0 else num_tests * 10
        self.num_test_per_prob = num_tests // 10 # Number of probability tests
        self.max_iterations = max_iterations
        self.H = H
        self.G = lc.to_rref(H)
        self.decoding_method = decoding_method

    def run(self):
        print(f'\nSTART TIME: {datetime.datetime.now()}\n')

        code_set = lc.create_code_set(self.G, self.H)

        print(f'Code Set: \n {code_set}\n')

        noise = {
            'erasure': bec,
            'flipping': bsc
        }[self.decoding_method] 
        
        decoder = Decoder(self.H, self.decoding_method, self.max_iterations)

        corruption_prob = 0.05

        decoding_success_count = []
        decoding_error_probabilities = []
        decoding_result_tuples = {round(i / 100, 2): [] for i in range(5, 60, 5)}

        success_count = 0
        iteration_count = 0
        quit_count = 0

        for t in range(1, self.num_tests + 1):
            random_msg = random.choice(code_set)
            original_codeword = lc.generate_code_word(random_msg, self.G)            

            corrupted_codeword = noise(original_codeword, corruption_prob)

            decoder_result_tuple = decoder.run(corrupted_codeword)
            
            decoded_codeword = decoder_result_tuple[0]
            iteration_count = decoder_result_tuple[1]
            quit = decoder_result_tuple[2]

            if (original_codeword == decoded_codeword).all():
                success_count += 1
            
            correct_decoding_count = 0
            for i in range(len(original_codeword)):
                correct_decoding_count += 1 if (original_codeword[i] == decoded_codeword[i]) else 0
            
            decoding_result_tuple = (correct_decoding_count, iteration_count, quit)
            decoding_result_tuples[corruption_prob].append(decoding_result_tuple)

            if t % self.num_test_per_prob == 0:
                # Store results
                decoding_success_count.append(success_count)
                decoding_error_probabilities.append(round(1 - (success_count / self.num_test_per_prob), 2))

                # Reset counters
                success_count = 0
                iteration_count = 0

                # Increment to next probability test
                corruption_prob = round(corruption_prob + 0.05, 2)
        
        print(f'END TIME: {datetime.datetime.now()}\n')
        print('********* RESULTS *********\n')
        print(f'SIMULATIONS RUN: [TOTAL: {self.num_tests}, PER NOISE PROBABILITY: {self.num_test_per_prob}]')
        print(f'\n<SUCCESSFUL DECODINGS>: -> {decoding_success_count}')
        print(f'\n<DECODING ERROR PROBABILITY>: -> {decoding_error_probabilities}')
            
        return decoding_error_probabilities                
