# This script implements a toy symmetric cipher class to help motivate Diffie Hellman - This cipher is not secure

import math

class ToySymmetricCipher():

    # Storing the shared key in binary
    def set_shared_key(self, key):
        self.shared_key = bin(key)[2:]

    # Ecnrypt
    def encrypt(self, plaintext, key):
        plaintext_bits = self.string_to_bits(plaintext)
        key_stream = self.create_key_steam(key, len(plaintext_bits))
        ciphertext_bits = self.xor(plaintext_bits, key_stream)
        ciphertext = self.bits_to_hex(ciphertext_bits)
        return ciphertext

    # Decrypt
    def decrypt(self, ciphertext, key):
        ciphertext_bits = self.hex_to_bits(ciphertext)
        key_stream = self.create_key_steam(key, len(ciphertext_bits))
        plaintext_bits = self.xor(ciphertext_bits, key_stream)
        plaintext = self.bits_to_string(plaintext_bits)
        return plaintext

    # Convert ASCII characters to their binary
    def string_to_bits(self, string):
        str = ''.join('{:08b}'.format(ord(c)) for c in string)
        return str

    # Create key stream the same length as the plaintext
    def create_key_steam(self, key, length):
        upper_bound = math.ceil(length/len(key))
        key_stream = ''
        for i in range(upper_bound):
            key_stream += key
        key_stream = key_stream[:length]
        return key_stream

    # XOR two binary strings
    def xor(self, first, second):
        return ''.join([str(ord(a) ^ ord(b)) for a,b in zip(first, second)]) 

    # Convert bit string to hex string
    def bits_to_hex(self, bits):
        return hex(int(bits, 2))

    # Convert hex string to bit string
    def hex_to_bits(self, hex):
        return bin(int(hex, 16))[2:]

    # Convert bits to corresponding ASCII character
    def bits_to_string(self, bits):
        n = 8
        bytes_array = [bits[i:i+n] for i in range(0, len(bits), n)]
        return ''.join([chr(int(x, 2)) for x in bytes_array])

