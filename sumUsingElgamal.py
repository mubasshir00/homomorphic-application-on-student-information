from Crypto.Util.number import *
from Crypto import Random
import Crypto
import random
import libnum
import sys
import hashlib
    
def get_generator(p: int):
    while True:
        # Find generator which doesn't share factor with p
        generator = random.randrange(3, p)
        if pow(generator, 2, p) == 1:
            continue
        if pow(generator, p, p) == 1:
            continue
        return generator
    
bits=512
v1=19
v2=5

if (len(sys.argv)>1):
    v1=int(sys.argv[1])
if (len(sys.argv)>2):
    v2=int(sys.argv[2])
if (len(sys.argv)>3):
    bits=int(sys.argv[3])

p = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
    
        
g = get_generator(p)  
x = random.randrange(3, p)  
Y = pow(g,x,p)

print (f"v1={v1}\nv2={v2}\n")
print (f"Public key:\ng={g}\nY={Y}\np={p}\n\nPrivate key\nx={x}")

k1=random.randrange(3, p)  
a1=pow(g,k1,p)
b1=(pow(Y,k1,p)*pow(g,v1,p)) % p

k2=random.randrange(3, p)  
a2=pow(g,k2,p)
b2=(pow(Y,k2,p)*pow(g,v2,p)) % p

a=(a1*a2)%p
b=(b1*b2)%p

print (f"\nEncrypted (v1)\na={a1}\nb={b1}")
print (f"\nEncrypted (v2)\na={a2}\nb={b2}")
print (f"\nAfter homomorphic encryption\na={a}\nb={b}")

v_r=(b*libnum.invmod(pow(a,x,p),p)) % p

print ("\nResult: ",v_r )

# Now search for g^i
for i in range(1,2**64):
    if (pow(g,i,p)==v_r):
        print("Found: ",i)
        break