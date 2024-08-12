from tkinter.filedialog import askdirectory, askopenfilename
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from getpass import getpass
from datetime import datetime

date = datetime.now()

#Set variables
#Choose .pfx File and save directory location
fileChoice = askopenfilename()
with open(fileChoice, 'rb') as filepfx:
    pfx = filepfx.read()
    
directory = askdirectory() + "/"
#Create outfile name | year + 1 and current month
outfile = input("What is the prefix for the file? ") + str(int(date.year + 1)) + "_" + str(date.month)
keyFile = directory + outfile + ".key"
crtFile = directory + outfile + ".crt"
chainFile = directory + "ChainofTrust.crt"

#File Pass
passphrase = getpass("Enter Password ")
passByte=bytes(passphrase, 'utf-8')

#Get files
privKey, cert, chain=pkcs12.load_key_and_certificates(pfx, passByte)

if privKey:
    with open(keyFile, "wb") as keyFile:
        keyFile.write(privKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(passByte)
            ))
if cert:
    with open(crtFile, "wb") as crtFile:
        crtFile.write(cert.public_bytes(
            encoding=serialization.Encoding.PEM
            ))
if chain:
    with open(chainFile, "wb") as chainFile:
        for ca in reversed(chain): #having none-reversed will only add the CA to the cert instead of IA and CA
            chainFile.write(ca.public_bytes(
                encoding=serialization.Encoding.PEM
            ))
keyFile.close()
crtFile.close()
chainFile.close()