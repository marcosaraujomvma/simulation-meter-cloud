# -*- coding: utf-8 -*-
#Cliente socket enviando mensagem de um numero aleatorio
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import hashlib
import time
import random
from Crypto.PublicKey import RSA


def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())


fpr = open("chaves/medidor01_Privatekey.pem")
keypr = RSA.importKey(fpr.read())
print "LEU CHAVE PRIVADA 1024 DO MEDIDOR\n"

fpucl = open("chaves/cloudPublic.pem")
keypucl = RSA.importKey(fpucl.read())
print "LEU CHAVE PUBLICA 4096 DA NUVEM \n"

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 8085            # Porta que o Servidor esta
#tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#dest = (HOST, PORT)
#tcp.connect(dest)



i =0

while i <5000000:
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)   
    tcp.connect(dest)
 
    time.sleep(0.3)#espera 1 segundo
    
    
    meter = random.randint(1,10)#gera a medição

    ts = time.time()#gera o timestamp
    
    msg = ("01;%s;%s"%(str(meter),str(ts))) #prepara a msg

    hash_msg = criarHash(msg) #hash da mensagem
    
    signature = keypr.sign(hash_msg,"") #assina a mensagem
    
    strmsg=("%s;%s"%(msg,str(signature))) #tranforma em string a mensagem para enviar
    
    enc = keypucl.encrypt(strmsg,4096) #criptografa a mensagem para enviar com a chave publica da nuvem
    print "MENSAGEM CRIPTOGRAFADA"
     
    print strmsg
    print (type(enc))
    print "MENSAGEM CRIPTOGRAFADA"
    #print (enc)
    i += 1
    a, = enc
    #print a
    print type(a)
    
    
    tcp.send (a)
    
    tcp.close()

