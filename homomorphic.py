
import numpy as np
from Pyfhel import Pyfhel

HE = Pyfhel()           # Creating empty Pyfhel object
HE.contextGen(scheme='bfv', n=2**14, t_bits=20)  # Generate context for 'bfv'/'ckks' scheme
                       
HE.keyGen()           

integer1 = np.array([104, 101, 108, 108, 111], dtype=np.int64)
ctxt1 = HE.encryptInt(integer1) # Encryption makes use of the public key

resSum = HE.decryptInt(ctxt1) # Decryption must use the corresponding function

print(resSum)



# sphinx_gallery_thumbnail_path = 'static/thumbnails/helloworld.png'