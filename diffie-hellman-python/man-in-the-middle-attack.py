from diffie_hellman import DiffieHellman

# Create Alice instance, this is the same as main.py so will not include comments
alice = DiffieHellman('alice')
p = alice.get_p(32)
g = alice.get_g(p)

print('\nINITIAL PARAMETERS', alice.get_initial_parameters())

a = alice.generate_private_key(p)
A = alice.generate_public_key(a, p, g)

print('ALICE:', alice)

# Create Bob instance

bob = DiffieHellman('bob')
b = bob.generate_private_key(p)
B = bob.generate_public_key(b, p, g)

print('BOB:', bob)

# Create Mallet instance

mallet = DiffieHellman('mallet')
m = mallet.generate_private_key(p)
M = mallet.generate_public_key(m, p, g)

print('MALLET:', mallet)

# Mallet sits in between Alice and Bob's communication without either being aware

# Alice shares her public key with whom she thinks is Bob
# Mallet intercepts Alice's public key and uses it to create a shared secret with Alice and returns his public key to Alice
# Alice then creates her shared secret with Mallets public key although she thinks it is Bob's

# Alice computes key_alice = (M ^ a) (mod p) using Mallets public key
key_alice = pow(M, a, p)

# Save the key
alice.set_shared_key(key_alice)

# Mallet creates key_mallet_alice = (A ^ m) mod p
key_mallet_alice = pow(A, m, p)

# Bob shares his public key with whom he thinks is Alice
# Mallet intercepts Bob's public key and uses it to create a shared secret with Bob and returns his public key to Bob
# Bob then creates his shared secret with Mallets public key although he thinks it is Alice's

# Bob computes key_bob = (M ^ b) (mod p), using Mallets public key
key_bob = pow(M, b, p)

# Save the key
bob.set_shared_key(key_bob)

# Mallet creates key_mallet_bob = (B ^ m) mod p
key_mallet_bob = pow(B, m, p)

print('COMPUTED KEYS:')
print('KEY_ALICE:       ', key_alice)
print('KEY_MALLET_ALICE:', key_mallet_alice)
print('KEY_BOB:         ', key_bob)
print('KEY_MALLET_BOB:  ', key_mallet_bob)
print('\nNote from above that Alice now has a shared secret with Mallet and Bob has a different shared secret with Mallet\n')

print('Mallet can now become a passive listener in Alice and Bob\'s communication:\n')

# Alice encrypts and sends a message to Mallet, although she thinks it is Bob
alice_plaintext = 'Hey Bob, I hope nobody is listening to us...'
alice_ciphertext = alice.encrypt(alice_plaintext, alice.shared_key)
print('ALICE\'S CIPHERTEXT:', alice_ciphertext)

# Mallet can decrypt this ciphertext with his shared secret with Alice and read it in the clear
mallet_recovered_plaintext = mallet.decrypt(alice_ciphertext, bin(key_mallet_alice)[2:] )
print('MALLET READS ALICE\'S MESSAGE:', mallet_recovered_plaintext)

# Mallet then encrypts Alice's plaintext message with his shared secret with Bob and forwards it to Bob
mallet_ciphertext = mallet.encrypt(mallet_recovered_plaintext, bin(key_mallet_bob)[2:])
print('MALLETS\'S CIPHERTEXT:', mallet_ciphertext)

# Bob decrypts the message from Mallet but thinks it is from Alice
bob_recovered_plaintext = bob.decrypt(mallet_ciphertext, bob.shared_key)
print('BOB\'S RECOVERED PLAINTEXT:', bob_recovered_plaintext)

print('\nMallet has successfully become a passive listener in Alice and Bob\'s communication\n')

print('Mallet can also perform an active attack on Alice and Bob\'s communication:\n')

# Alice encrypts and sends a message to Mallet, although she thinks it is Bob
alice_plaintext = 'Hey Bob, my account number is 65,537. Can you send the money today?'
alice_ciphertext = alice.encrypt(alice_plaintext, alice.shared_key)
print('ALICE\'S CIPHERTEXT:', alice_ciphertext)

# Mallet can decrypt this ciphertext and read it in the clear
mallet_recovered_plaintext = mallet.decrypt(alice_ciphertext, bin(key_mallet_alice)[2:] )
print('MALLET READS ALICE\'S MESSAGE:', mallet_recovered_plaintext)

# Mallet then creates a malicious message, encrypts it and sends it to Bob
mallet_malicious_plaintext = 'Hey Bob, my account number is 31,415. Can you send the money today?'
mallet_ciphertext = mallet.encrypt(mallet_malicious_plaintext, bin(key_mallet_bob)[2:])
print('MALLETS\'S CIPHERTEXT:', mallet_ciphertext)

# Bob decrypts the message from Mallet but thinks it is from Alice
bob_recovered_plaintext = bob.decrypt(mallet_ciphertext, bob.shared_key)
print('BOB\'S RECOVERED PLAINTEXT:', bob_recovered_plaintext)

print('\nMallet has successfully performed an active attack on Alice and Bob\'s communication by changing the account number.\n')