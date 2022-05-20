import random

# Function to generate random n-bit prime
def get_random_n_bit_prime(n):
    while True:
        prime_candidate = low_level_primality_test(n)
        if not miller_rabin_test(prime_candidate):
            continue
        else:
            return prime_candidate


# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]


# Get a random n-bit number
def get_random_n_bit_number(n):
    return random.randrange(2**(n-1)+1, 2**n-1)


# Low-Level Primality Test
def low_level_primality_test(n):
    while True:
        # Obtain a random number
        prime_candidate = get_random_n_bit_number(n)

        # Test divisibility by pre-generated primes
        for divisor in first_primes_list:
            if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                break
        else:
            return prime_candidate


# Miller rabin primality test
def miller_rabin_test(prime_candidate):
    max_divisions_by_two = 0
    even_component = prime_candidate - 1
    while even_component % 2 == 0:
        even_component >>= 1
        max_divisions_by_two += 1
    assert(2 ** max_divisions_by_two * even_component == prime_candidate - 1)

    def trial_composite(round_tester):
        if pow(round_tester, even_component, prime_candidate) == 1:
            return False
        for i in range(max_divisions_by_two):
            if pow(round_tester, 2**i * even_component, prime_candidate) == prime_candidate - 1:
                return False
        return True

    # Set number of trials here
    number_of_rabin_trials = 20
    for i in range(number_of_rabin_trials):
        round_tester = random.randrange(2, prime_candidate)
        if trial_composite(round_tester):
            return False
    return True