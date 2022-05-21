from diffie_hellman import DiffieHellman

### ALICE ###

# Create Alice instance
alice = DiffieHellman('alice')

# Alice generates p, a 2,048-bit prime
# For efficency actually generating a 32-bit prime
p = alice.get_p(32)

# Alice compute g, such that g is a primitive root of p
g = alice.get_g(p)

print('\nINITIAL PARAMETERS', alice.get_initial_parameters())

# Alice chooses a private key (a) such that 1 ≤ a ≤ p − 2
# Alice keeps this private
a = alice.generate_private_key(p)

# Alice generates a public key (A) such that A = (g ^ a) mod p
A = alice.generate_public_key(a, p, g)

print('ALICE:', alice)

### BOB ###

bob = DiffieHellman('bob')

# Bob chooses a private key (b) such that 1 ≤ b ≤ p − 2
# Bob keeps this private
b = bob.generate_private_key(p)

# Bob generates a public key (B) such that B = (g ^ b) mod p
B = bob.generate_public_key(b, p, g)

print('BOB:', bob)

### ALICE & BOB PUBLICLY SHARE A & B RESPECTIVELY ###

# Alice computes key_alice = (B ^ a) (mod p)
key_alice = pow(B, a, p)

# Save the key
alice.set_shared_key(key_alice)

# Bob computes key_bob = (A ^ b) (mod p)
key_bob = pow(A, b, p)

# Save the key
bob.set_shared_key(key_bob)

print('COMPUTED KEYS:')
print('KEY_ALICE:', key_alice)
print('KEY_BOB:  ', key_bob)

if(key_alice == key_bob): print('\nBoth Alice and Bob have generated the same secret without ever revealing their respective private keys. This shared secret can now be used for symmetric encryption.\n')

print('Testing encrption and decryption with the new shared secret...\n')

# Alice creates ciphertext with her shared key
alice_plaintext = 'Hey, Bob! I am Alice.'
alice_ciphertext = alice.encrypt(alice_plaintext)
print('ALICE\'S CIPHERTEXT:', alice_ciphertext)

# Alice sends ciphertext to Bob who decrypts it with his shared key
bob_recovered_plaintext = bob.decrypt(alice_ciphertext)
print('BOB\'S RECOVERED PLAINTEXT:', bob_recovered_plaintext)

if(alice_plaintext == bob_recovered_plaintext): print('\nAlice and Bob have successfully communicated using their shared secret key generated with Diffie Hellman.\n')

