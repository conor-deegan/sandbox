# Requires Python 3

# Imports
import hashlib
import math

# Constants
BLOCK_SIZE = 64
ROUNDS = 8

# Encrypt function takes a plaintext ASCII string and a secret
def encrypt(plaintext, secret):
    # Convert plaintext string to bits (with padding)
    plaintext_bits = string_to_bits(plaintext)
    # Split bits into blocks of size BLOCK_SIZE
    plaintext_blocks = split_to_blocks(plaintext_bits, BLOCK_SIZE)
    # Generate 256 bit key from secret
    key = generate_key(secret)
    # Generate sub keys - 8x32 bit blocks from the 256 bit key
    sub_keys = split_to_blocks(key, int(BLOCK_SIZE/2))
    ciphertext_blocks = []
    # Loop over each plaintext block
    for plaintext_block in plaintext_blocks:
        # For each block, perform ROUNDS rounds
        for i in range(ROUNDS):
            plaintext_block = round(plaintext_block, sub_keys[i])
        # Once rounds completed, add ciphertext to chipertext blocks - reverse left and right halves
        ciphertext_blocks.append(str(plaintext_block[32:]) + str(plaintext_block[:32]))
    # Join the ciphertext blocks and convert binary string to hex string    
    return bits_to_hex(''.join(ciphertext_blocks))

# Decrypt function takes a chipertext hex string and a secret
def decrypt(ciphertext, secret):
    # Convert chipertext string to bits
    ciphertext_bits = hex_to_bits(ciphertext)
    # Split bits into blocks of size BLOCK_SIZE
    ciphertext_blocks = split_to_blocks(ciphertext_bits, BLOCK_SIZE)
    # Generate 256 bit key from secret
    key = generate_key(secret)
    # Generate sub keys - 8x32 bit blocks from the 256 bit key
    sub_keys = split_to_blocks(key, int(BLOCK_SIZE/2))
    plaintext_blocks = []
    # Loop over each ciphertext block
    for ciphertext_block in ciphertext_blocks:
        # For each block, perform ROUNDS rounds
        for i in range(ROUNDS, 0, -1):
            # Use the sub_keys in reverse order compared to encryption
            ciphertext_block = round(ciphertext_block, sub_keys[i - 1])
        # Once rounds completed, add plaintext to plaintext blocks - reverse left and right halves
        plaintext_blocks.append(str(ciphertext_block[32:]) + str(ciphertext_block[:32]))
    # Join the 64-bit plaintext blocks into a single bit string
    # Split the plaintext bit string into blocks of 8 bits (1 byte)
    # For each byte, convert byte to ASCII character
    return bits_to_string(split_to_blocks(''.join(plaintext_blocks), 8))

# This funciton defines the logic performed during each round of the Feistel Network
def round(bits, sub_key):
    # Split the bit string into left and right halves (32 bits each)
    left_bits = bits[:32]
    right_bits = bits[32:]
    # Compute f_out: in this case by XORing the sub key with the right bits
    f_out = xor(sub_key, right_bits)
    # XOR f_out and the left bits
    left_xor_f_out = xor(left_bits, f_out)
    # Swap the halves and return
    return right_bits + left_xor_f_out

# Function for XORing two binary strings
def xor(first, second):
    return ''.join([str(ord(a) ^ ord(b)) for a,b in zip(first, second)]) 

# Get the binary representation of the hashed secret using sha256
def generate_key(secret):
    hash = hashlib.sha256(str.encode(secret)).hexdigest()
    integer = int(hash, 16)
    bin_hash = format(integer, '0>42b').zfill(256)
    return bin_hash

# Function to convert ASCII characters to their binary represenation
def string_to_bits(string):
    str = ''.join('{:08b}'.format(ord(c)) for c in string)
    return str.ljust(BLOCK_SIZE * math.ceil(len(str)/BLOCK_SIZE), '0')

# Convert bit string to hex string
def bits_to_hex(bits):
    return hex(int(bits, 2))

# Convert hex string to bit string
def hex_to_bits(hex):
    return bin(int(hex, 16))[2:]

# Convert byte to corresponding ASCII character
def bits_to_string(bytes):
    return ''.join([chr(int(x, 2)) for x in bytes])

# Splits bit string into blocks of size block_size
def split_to_blocks(bits, block_size):
    return [bits[i:i+block_size] for i in range(0, len(bits), block_size)]

######## TEST NETWORK ########

plaintext = 'Hello Feistel Network!'
secret = 'My Secret Key'

print('PLAINTEXT:          ', plaintext)
print('SECRET KEY:         ', secret)

ciphertext = encrypt(plaintext, secret)
print('CIPHERTEXT:         ', ciphertext)

recovered_plaintext = decrypt(ciphertext, secret)
print('RECOVERED PLAINTEXT:', recovered_plaintext)