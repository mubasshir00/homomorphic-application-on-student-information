import numpy as np
from Pyfhel import Pyfhel
import json
from Crypto.Util import number

    
from Crypto.Util.number import *
from Crypto import Random
import Crypto
import random
import libnum
import sys
import hashlib

def main():
    f = open('transcript.json')
    data = json.load(f)
    print(data)
main()