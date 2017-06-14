# -*- coding: utf-8 -*-
#Cliente socket
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Util.randpool import RandomPool

import socket,time,random

#from Crypto import Random
from Crypto.Cipher import AES
import base64

BLOCK_SIZE=32


pool = RandomPool(1024)
pool.stir()
randfunc = pool.get_bytes
key= RSA.generate(1024, randfunc)#gera a chave aqui



def encrypt(message, passphrase):
    h = SHA256.new()
    h.update(passphrase)
    key = h.digest()[0:16]
    # passphrase MUST be 16, 24 or 32 bytes long, how can I do that ?
    IV = Random.new().read(16)
    aes = AES.new(key, AES.MODE_CFB, IV)
    return base64.b64encode(aes.encrypt(message))



print("Pode Codificar? ",key.can_encrypt())

print("Pode Assinar? ",key.can_sign())

print("E privada? ",key.has_private())

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 6000           # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)


print 'Para sair use CTRL+X\n'


id_medidor = raw_input("Digite o Id do Medidor: ")
"""
while msg <> '\x18':
    tcp.send (msg)
    msg = raw_input()
"""
for i in range(2880):
    ts = time.time()
    time.sleep(0.3)
    
    hash = SHA256.new(str(ts)).digest()
    
    signature = key.sign(hash,"")
    
    leitura = random.uniform(1,8)#gera a leitura aletorio
    n, e, d = key.n, key.e, key.d 
    msg = "%s;%s;%s;%s;%s;%s"%(n,e,signature,ts,id_medidor,leitura)
    msgcod = encrypt(msg,"medidor")
    tcp.send(msg)
    
    print "Pacote %i Enviado!"%i
    print "Leitura: %i Kwh"%leitura
tcp.close()