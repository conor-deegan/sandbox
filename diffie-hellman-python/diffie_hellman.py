# Main Diffe Hellman class

from toy_symmetric_cipher import ToySymmetricCipher

from prime import get_random_n_bit_prime, get_random_prime_within_bounds
from primitive_root import find_primitive

# This class is a child of ToySymmetricCipher. This has nothing to do with Diffie Hellman but is used to demonstrate encryption, decryption, and attacks when a shared key is generated
class DiffieHellman(ToySymmetricCipher):

    # Constructor
    def __init__(self, name):
        self.name = name

    # Generate p
    def get_p(self, n):
        p = get_random_n_bit_prime(n)
        self.p = p
        return p
    
    # Generate g
    def get_g(self, p):
        g = find_primitive(p)
        self.g = g
        return g

    # Generate a private key
    def generate_private_key(self, p):
        private_key = get_random_prime_within_bounds(1, p - 2)
        self.private_key = private_key
        return private_key
    
    # Generate a public key
    def generate_public_key(self, private_key, p, g):
        # return (g ** private_key) % p
        public_key = pow(g, private_key, p)
        self.public_key = public_key
        return public_key

    # Creating nice representation for printing
    def __repr__(self):
        return '\nPrivate key: {}\nPublic key: {}\n'.format(self.private_key, self.public_key)

    # Getter for initital parameters
    def get_initial_parameters(self):
        return '\nP: {}\nG: {}\n'.format(self.p, self.g)