from Crypto.Util import number

# Generate public and private keys
p = number.getPrime(1024)
g = 2
x = number.getRandomRange(2, p-2)
y = pow(g, x, p)

# Encrypt a message
m = 5
k = number.getRandomRange(2, p-2)
c1 = pow(g, k, p)
c2 = (m * pow(y, k, p)) % p

# Decrypt the ciphertext
m_dec = (c2 * pow(c1, p-1-x, p)) % p

# Print the original message and the decrypted message
print(f"Original message: {m}")
print(f"Decrypted message: {m_dec}")
