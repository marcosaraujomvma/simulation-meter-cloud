from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto import Random
import base64

msg = 'msg';


aeskey = Random.new().read(32)
iv = Random.new().read(AES.block_size)
aescipher = AES.new(aeskey, AES.MODE_CFB, iv)
aesciphertext = iv + aescipher.encrypt(msg.encode('utf-8'))


rsakey = RSA.importKey(open('public.pem').read())
rsacipher = PKCS1_OAEP.new(rsakey)
rsaciphertext = rsacipher.encrypt(aeskey)

#print (base64.b64encode(aesciphertext))
#print (base64.b64encode(rsaciphertext))


rsakey = RSA.importKey(open('private.pem').read())	
rsacipher = PKCS1_OAEP.new(rsakey)

aeskey = rsacipher.decrypt(rsaciphertext)
aescipher = AES.new(aeskey, AES.MODE_CFB, aesciphertext[0:AES.block_size])
msg = aescipher.decrypt(aesciphertext[AES.block_size:])


print(msg.decode('utf-8'))
