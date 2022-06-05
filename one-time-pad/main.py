import random

class one_time_pad():
    # XOR two binary strings
    def xor(self, first, second):
        return ''.join([str(ord(a) ^ ord(b)) for a,b in zip(first, second)]) 

    # Convert ASCII characters to their binary
    def string_to_bits(self, string):
        str = ''.join('{:08b}'.format(ord(c)) for c in string)
        return str

    # Convert bits to corresponding ASCII character
    def bits_to_string(self, bits):
        n = 8
        bytes_array = [bits[i:i+n] for i in range(0, len(bits), n)]
        return ''.join([chr(int(x, 2)) for x in bytes_array])

    # Convert bit string to hex string
    def bits_to_hex(self, bits):
        return hex(int(bits, 2))

    # Convert hex string to bit string
    def hex_to_bits(self, hex):
        return  bin(int(hex, 16))[2:]
    
    # Generate a key stream of length n
    def generate_key_stream(self, n):
        key = "1"
        for _ in range(n-1):
            bit = str(random.randint(0, 1))
            key += bit
        return key

    # Encryption function
    def encrypt(self, plaintext):
        plaintext_binary = self.string_to_bits(plaintext)
        key = self.generate_key_stream(len(plaintext_binary))
        ciphertext = self.xor(plaintext_binary, key)
        return self.bits_to_hex(ciphertext), self.bits_to_hex(key)

    # Decryption function
    def decrypt(self, ciphertext, key):
        key = self.hex_to_bits(key)
        ciphertext = self.hex_to_bits(ciphertext)
        plaintext = self.xor(key, ciphertext)
        return self.bits_to_string(plaintext)
   
otp = one_time_pad()
ciphertext, key = otp.encrypt('My account number is 12345')
plaintext = otp.decrypt(ciphertext, key)

print('\nPlaintext:')
print(plaintext)

# set the ciphertext as fixed
ciphertext = '0xbd168da42ceadd8313fb72b5f47b85ef595970fe91ca938cb975'

# A different key will create a different plaintext
key = '0xf06fadc54f89b2f67d8f52db8116e78a2b79198db1fca4b48045'
plaintext = otp.decrypt(ciphertext, key)
print('\nTampered plaintext:')
print(plaintext)

# Every possible plaintext message can be found with different keys
key = '0xbd42e5cd5fcabeec66971695961ea58e37200496f8a4f4ad9854'
plaintext = otp.decrypt(ciphertext, key)
print('\nDemo that any plaintext message can be found:')
print(plaintext)