import time

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


start_time = time.time()


p = number.getPrime(1024)
g = 2 
x =number.getRandomRange(2, p-2)
y = pow(g,x,p)
k = number.getRandomRange(2, p-2)


# multiplication
def get_generator(p: int):
    while True:
        # Find generator which doesn't share factor with p
        generator = random.randrange(3, p)
        if pow(generator, 2, p) == 1:
            continue
        if pow(generator, p, p) == 1:
            continue
        return generator

def homomorphicMultiply(input1,input2):
    bits=512
    v1=input1
    v2=input2
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
    k1=random.randrange(3, p)  
    a1=pow(g,k1,p)
    b1=(pow(Y,k1,p)*v1) % p
    k2=random.randrange(3, p)  
    a2=pow(g,k2,p)
    b2=(pow(Y,k2,p)*v2) % p
    a=(a1*a2) %p
    b=(b1*b2) %p
    v_r=(b*libnum.invmod(pow(a,x,p),p)) % p
    return v_r

def get_generator_div(p: int):
    while True:
        # Find generator which doesn't share factor with p
        generator = random.randrange(3, p)
        if pow(generator, 2, p) == 1:
            continue
        if pow(generator, p, p) == 1:
            continue
        return generator

def homomorphicDiv(input1,input2):
    bits=512
    v1=input1
    v2=input2
    if (len(sys.argv)>1):
        v1=int(sys.argv[1])
    if (len(sys.argv)>2):
        v2=int(sys.argv[2])
    if (len(sys.argv)>3):
        bits=int(sys.argv[3])
    p = Crypto.Util.number.getPrime(bits, randfunc=Crypto.Random.get_random_bytes)
    g = get_generator_div(p)  
    x = random.randrange(3, p)  
    Y = pow(g,x,p)
    k1=random.randrange(3, p)  
    a1=pow(g,k1,p)
    b1=(pow(Y,k1,p)*v1) % p
    k2=random.randrange(3, p)  
    a2=pow(g,k2,p)
    b2=(pow(Y,k2,p)*v2) % p
    a=(a1*libnum.invmod(a2,p)) %p
    b=(b1*libnum.invmod(b2,p)) %p
    v_r=(b*libnum.invmod(pow(a,x,p),p)) % p
    finalData = [a,v_r]
    return finalData



def string_to_ascii(s):
    ascii_vals = []
    for c in s:
        ascii_val = ord(c)
        ascii_vals.append(ascii_val)
    return ascii_vals

def ascii_to_word(ascii_list):
    word = ""
    for ascii_value in ascii_list:
        char = chr(ascii_value)
        word += char
    return word


def encryptNormalText(m):
    c1 = pow(g, k,p)
    c2 =(m*pow(y,k,p))%p
    return c2

def decryptedNormalText(m):
    c1 = pow(g, k,p)
    c2 =(m*pow(y,k,p))%p
    m_dec = (c2 * pow(c1, p-1-x, p)) % p
    return m_dec

def main():
    f = open('transcript1.json')
    data = json.load(f)
    finalEncryptedData = []
    finalDecryptedData = []
    sumOfGradMult = 0
    sumOfCredit = 0
    multiplicationTemp =1
    finalGrade = 0
    for i in data:
        tempAsciiValue = string_to_ascii(i['course_code'])
        tempAsciiValueOfGrade = string_to_ascii(i['course_grade'])
    
        tempArray =[]
        tempArrayGrade =[]
        tempArray1 =[]
        tempArrayGrade1 =[]
        # print(tempAsciiValue)
        for j in tempAsciiValue:
            tempArray.append(encryptNormalText(j))

        for j in tempAsciiValueOfGrade:
            tempArrayGrade.append(encryptNormalText(j))

        for j in tempAsciiValue:
            tempArray1.append(decryptedNormalText(j))

        for j in tempAsciiValueOfGrade:
            tempArrayGrade1.append(decryptedNormalText(j))

        finalEncryptedData.append({
            "semester_name" :i['semester_name'],
            "course_code" : tempArray,
            "course_grade" : tempArrayGrade,
            "course_credit": i['course_credit']
        })

        finalDecryptedData.append({
            "semester_name" :i['semester_name'],
            "course_code" :ascii_to_word(tempArray1),
            "course_grade" : ascii_to_word(tempArrayGrade1),
            "course_credit": i['course_credit']
        })

        gradeSum = 0
        gradePoint = 1
        if(i['course_grade']=='D'):
            gradePoint = 1*1000
        elif(i['course_grade']=='C'):
            gradePoint = 2*1000
        elif(i['course_grade']=='B'):
            gradePoint = 3*1000
        elif(i['course_grade']=='B+'):
            gradePoint = math.floor(3.7*1000)
        elif(i['course_grade']=='D+'):
            gradePoint = math.floor(1.7*1000)
        tempMulti = homomorphicMultiply(i['course_credit'], gradePoint)
        sumOfCredit=sumOfCredit+i['course_credit']
        multiplicationTemp = max(multiplicationTemp, tempMulti)
        sumOfGradMult = (sumOfGradMult)+multiplicationTemp

        # finalGrade=homomorphicDiv(sumOfGradMult,sumOfCredit)

    encryptGradeMultAscii = string_to_ascii(str(sumOfGradMult))
    tempAsciiMult=[]
    tempAsciiMult1=[]
    for j in encryptGradeMultAscii:
            tempAsciiMult.append(encryptNormalText(j))
    # print("encryptGradeMult",tempAsciiMult)

    for j in encryptGradeMultAscii:
        tempAsciiMult1.append(decryptedNormalText(j))

    depcryptedGradeMult = ascii_to_word(tempAsciiMult1)


    encryptsumOfCreditAscii = string_to_ascii(str(sumOfCredit))
    tempAsciisumOfCredit=[]
    tempAsciisumOfCredit1=[]
    for j in encryptsumOfCreditAscii:
            tempAsciisumOfCredit.append(encryptNormalText(j))
    # print("encryptGradeMult",tempAsciiMult)

    for j in encryptsumOfCreditAscii:
        tempAsciisumOfCredit1.append(decryptedNormalText(j))

    depcryptedsumOfCredit = ascii_to_word(tempAsciisumOfCredit1)

    finalGrade=(int(depcryptedGradeMult)/int(depcryptedsumOfCredit))/1000

    finalEncryptedData.append({
        "CGPA" : [encryptGradeMultAscii,encryptsumOfCreditAscii]
    })
    print(tempAsciisumOfCredit1)
    with open("encrypted.json", "w") as outfile:
        json.dump(finalEncryptedData, outfile)

    finalDecryptedData.append({
        "CGPA" : finalGrade
    })
    with open("decrypted.json", "w") as outfile:
        json.dump(finalDecryptedData, outfile)



main()

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.6f} seconds")
