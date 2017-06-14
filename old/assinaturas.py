# -*- coding: utf-8 -*-
#Cliente socket enviando mensagem de um numero aleatorio
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
random_generator = Random.new().read
print random_generator
private_key = RSA.generate(1024, random_generator)
text = 'abcdefgh'
hash = SHA256.new(text).digest()
print hash
signature = private_key.sign(hash, 'medidor001')


print("Pode Codificar? ",private_key.can_encrypt())

print("Pode Assinar? ",private_key.can_sign())

print("E privada? ",private_key.has_private())

#gerar chave publica
public_key = private_key.publickey()

enc_data = public_key.encrypt(text,32) #dados codificado com a chave publica


z = public_key.verify(hash, signature)#testar  integridade do dado

text2 = private_key.decrypt(enc_data)


####servidor
#texto + hash + signature)
