# Requires Python 3

import random
import math
import matplotlib.pyplot as plt

# where n = 2^i
I = [i for i in range(1, 17)]
# hash length
d = 16

# Using a pseudorandom generator over a hash function
def hash(d):
    return random.getrandbits(d)

# generates n d-bit hashes
def get_hashes(n, d):
    hashes = []
    for i in range(n):
        hashes.append(hash(d))
    return hashes

def main(I, d):
    # stores i
    x_list = []
    # stores experimental results
    y_actual_list = []
    # stores calculated results
    y_predicted_list = []
    for i in I:
        counter = 0
        dup = 0
        # Runs each experiment 1000 times
        for _ in range(1000):     
            hashes = get_hashes(2 ** i, d)
            collsion = check_collison(hashes)
            if(collsion):
                dup += 1
            counter += 1
        x_list.append(i)
        y_actual_list.append((dup / counter))
        y_predicted_list.append(gamma(2 ** i, d))
    # create and show results
    plt.plot(x_list, y_actual_list)
    plt.plot(x_list, y_predicted_list)
    plt.xlabel('i (Number of hashes produced = 2^i)')
    plt.ylabel('Probability of at least one collision')
    plt.legend(["Empirical Results", "Analytical formula"], loc ="lower right")
    plt.show()

# checks for collision using sets
def check_collison(l):
    if len(l) == len(set(l)):
        return False
    else:
        return True

# gamma prime - derived in article
def gamma_prime(n, d):
    return math.exp(-((n ** 2)/(2 * (2 ** d))))

# gamma - derived in article
def gamma(n, d):
    return 1 - gamma_prime(n, d)

main(I, d)