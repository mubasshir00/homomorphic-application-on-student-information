from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

import json
import base64
import time

start_time = time.time()

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Serialize and save private key
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open("private_key.pem", "wb") as f:
    f.write(private_pem)

# Get the corresponding public key
public_key = private_key.public_key()

# Serialize and save public key
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("public_key.pem", "wb") as f:
    f.write(public_pem)


def encryptDataRSA(data):
    data_to_encrypt = data.encode("utf-8")

    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    
    # Encrypt data
    ciphertext = public_key.encrypt(
        data_to_encrypt,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )   
    # print("Ciphertext:", ciphertext)
    return ciphertext


def decryptDataRSA(ciphertext):
    # Load private key
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Decrypt data
    decrypted_data = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    #print("Decrypted data:", decrypted_data.decode("utf-8"))
    return decrypted_data.decode("utf-8")

def cgpaCount(data):
    gradeSum = 0
    gradePoint = 1
    totalCredit =0
    for i in data:
        gradePoint = gradingPolicy(i['course_grade'])*float(i['course_credit'])
        gradeSum += gradePoint
        totalCredit += float(i['course_credit'])
    return gradeSum/totalCredit


def gradingPolicy(grade):
    if(grade == "D"):
        return 1
    elif(grade == "C"):
        return 2
    elif(grade == "B"):
        return 3
    elif(grade == "B+"):
        return 3.7
    elif(grade == "D+"):
        return 1.7

    return gradPoint

def cgpaCountFromEncryptedData(data):
    for i in data:
        if("cgpa" in i):
            i['cgpa'] = base64.b64decode(i['cgpa'])
        else:
            i['semester_name'] = base64.b64decode(i['semester_name'])
            i['course_code'] = base64.b64decode(i['course_code'])
            i['course_grade'] = base64.b64decode(i['course_grade'])
            i['course_credit'] = base64.b64decode(i['course_credit'])

    for i in data:
        if("cgpa" in i):
            i['cgpa'] = decryptDataRSA(i['cgpa'])
        else:
            i['semester_name'] = decryptDataRSA(i['semester_name'])
            i['course_code'] = decryptDataRSA(i['course_code'])
            i['course_grade'] = decryptDataRSA(i['course_grade'])
            i['course_credit'] = decryptDataRSA(i['course_credit'])

    totalCGPANow = encryptDataRSA(str(cgpaCount(data)))
    encodedCGPA = base64.b64encode(totalCGPANow).decode("utf-8")
    return encodedCGPA
    # print(totalCGPANow)

def main():
    #read data
    f = open('transcript.json')
    data = json.load(f)
    newTranscript = data

    # totalCGPANow = encryptDataRSA(str(cgpaCount(data)))
    # encodedCGPA = base64.b64encode(totalCGPANow).decode("utf-8")

    for i in newTranscript:
        i['semester_name'] = encryptDataRSA(i['semester_name'])
        i['course_code'] = encryptDataRSA(i['course_code'])
        i['course_grade'] = encryptDataRSA(i['course_grade'])
        i['course_credit'] = encryptDataRSA(str(i['course_credit']))

    for i in newTranscript:
        i['semester_name'] = base64.b64encode(i['semester_name']).decode("utf-8")
        i['course_code'] = base64.b64encode(i['course_code']).decode("utf-8")
        i['course_grade'] = base64.b64encode(i['course_grade']).decode("utf-8")
        i['course_credit'] = base64.b64encode(i['course_credit']).decode("utf-8")

    # newTranscript.append({'cgpa': encodedCGPA})

    with open("rsa_encrypted.json", "w") as outfile:
        json.dump(newTranscript, outfile)

    loadData = open('rsa_encrypted.json')
    encryptedData = json.load(loadData)

    totalCGPA = cgpaCountFromEncryptedData(encryptedData)

    newTranscript.append({'cgpa': totalCGPA})

    for i in newTranscript:
        if("cgpa" in i):
            i['cgpa'] = base64.b64decode(i['cgpa'])
        else:
            i['semester_name'] = base64.b64decode(i['semester_name'])
            i['course_code'] = base64.b64decode(i['course_code'])
            i['course_grade'] = base64.b64decode(i['course_grade'])
            i['course_credit'] = base64.b64decode(i['course_credit'])

    for i in newTranscript:
        if("cgpa" in i):
            i['cgpa'] = decryptDataRSA(i['cgpa'])
        else:
            i['semester_name'] = decryptDataRSA(i['semester_name'])
            i['course_code'] = decryptDataRSA(i['course_code'])
            i['course_grade'] = decryptDataRSA(i['course_grade'])
            i['course_credit'] = decryptDataRSA(i['course_credit'])

    with open("rsa_decrypted.json", "w") as outfile:
        json.dump(newTranscript, outfile)
    

main()

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.6f} seconds")