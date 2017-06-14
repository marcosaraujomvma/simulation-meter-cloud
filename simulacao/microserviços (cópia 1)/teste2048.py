# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA
import hashlib

def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())



hash = criarHash("CARRO")

fpr = open("chaves/medidor01_Privatekey.pem")
key = RSA.importKey(fpr.read())
print "LEU CHAVE PRIVADA 1024\n"

signature = key.sign(hash,"")
print "ASSINOU COM CHAVE PRIVADA 1024\n"
print (signature)


fpucl = open("chaves/cloudPublic.pem")
keypucl = RSA.importKey(fpucl.read())
print "LEU CHAVE PUBLICA 4096\n"

strmsg=str(signature)

enc = keypucl.encrypt(strmsg,4096)
print "MENSAGEM CRIPTOGRAFADA"
print (enc)


fprcl = open("chaves/cloudPrivate.pem")
keyprcl = RSA.importKey(fprcl.read())
print "LEU CHAVE PRIVADA 4096\n"


dec = keyprcl.decrypt(enc)

print "DECRYPT"
print dec

hash2 = criarHash("CARRO")

fpu = open("chaves/medidor1_Publickey.pem")
pukey = RSA.importKey(fpu.read())
print "LEU CHAVE PUBLICA 1024\n"

ass = long(dec[1:len(dec)-2])

print ass
print type(ass)

ass_tupla=(ass,)

print ass_tupla

z = pukey.verify(hash2,ass_tupla)


print ("Assinatura Correta:",z)