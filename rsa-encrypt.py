from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64


message = '4'
key = RSA.importKey(open('keypu.pem').read())
cipher = PKCS1_OAEP.new(key)
ciphertext = cipher.encrypt(message.encode('utf-8'))

print (base64.b64encode(ciphertext))

key = RSA.importKey(open('keypr.pem').read())
cipher = PKCS1_OAEP.new(key)
message = cipher.decrypt(ciphertext)

print(message.decode('utf-8'))
