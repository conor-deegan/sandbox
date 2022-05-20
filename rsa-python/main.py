from prime import get_random_n_bit_prime
from extended_euclidean import modular_inverse


def generate_key_pair():
    # generate 2 random 1024 bit primes
    p = get_random_n_bit_prime(1024)
    q = get_random_n_bit_prime(1024)

    # Compute n such that n = pq
    n = p * q

    # Compute lambda_n using Euler's totient function
    lambda_n = (p - 1) * (q - 1)

    # Common to let public exponent e = 65,537
    e = 65537

    # Compute d using the extended Euclidean Algorithm
    # Compute d duch that e.d = 1 (mod lambda_n)
    d = modular_inverse(e, lambda_n)

    return {'private_key': (d, n), 'public_key': (e, n)}

### TEST RSA ###

# Generate keypair
print('Generating keypair...')
keypair = generate_key_pair()
public_key = keypair['public_key']
private_key = keypair['private_key']

# Test encryption and decryption
print('Testing encryption and decryption...')

# Set plaintext
plaintext = 42
print('> PLAINTEXT:', plaintext)

# Encrypt with public key
ciphertext = (plaintext ** public_key[0] ) % public_key[1]
print('> CIPHERTEXT:', ciphertext)

# Decrypt with private key
recovered_plaintext = pow(ciphertext, private_key[0], private_key[1])
print('> RECOVERED PLAINTEXT:', recovered_plaintext)

if(plaintext == recovered_plaintext): print('Encryption and decryption successful')

# Test signing and verification
print('Testing signing and verification...')

# Set message to sign
message = 161803398875
print('> MESSAGE:', message)

# Sign message with private key
signature = pow(message, private_key[0], private_key[1])
print('> SIGNATURE:', signature)

# Get signed message with public key
message_prime = pow(signature, public_key[0], public_key[1])
print('> MESSAGE PRIME:', message_prime)

if(message == message_prime): print('Signing and verification successful')