# -*- coding: utf-8 -*-
#Cliente socket enviando mensagem de um numero aleatorio
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import hashlib
import time
import random, sys
from Crypto.PublicKey import RSA


def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())


fpr = open("keys/meter-private.pem")
keypr = RSA.importKey(fpr.read())
print "LEU CHAVE PRIVADA 1024 DO MEDIDOR\n"

fpucl = open("keys/cloud-public")
keypucl = RSA.importKey(fpucl.read())
print "LEU CHAVE PUBLICA 4096 DA NUVEM \n"

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 10010            # Porta que o Servidor esta
#tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#dest = (HOST, PORT)
#tcp.connect(dest)

id_medidor = sys.argv[1]

#id_medidor = raw_input("Digite o id do medidor: \n")


i =0
#86400
while i <2880:
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)   
    tcp.connect(dest)
 
    time.sleep(1)#espera 1 segundo
    
    
    meter = random.randint(1,100)#gera a medição

    ts = time.time()#gera o timestamp
    
    msg = ("%s;%s;%s"%(criarHash(id_medidor),str(meter),str(ts))) #prepara a msg

    hash_msg = criarHash(msg) #hash da mensagem
    
    signature = keypr.sign(hash_msg,"") #assina a mensagem
    
    strmsg=("%s;%s"%(msg,str(signature))) #tranforma em string a mensagem para enviar
    
    enc = keypucl.encrypt(strmsg,4096) #criptografa a mensagem para enviar com a chave publica da nuvem
    #print "MENSAGEM CRIPTOGRAFADA"
     
    #print strmsg
    #print (type(enc))
    #print "MENSAGEM CRIPTOGRAFADA"
    #print (enc)
    i += 1
    a, = enc
    #print a
    #print type(a)
    
    print "Numero de Pacotes Enviados (%i) \n\n"%(i)
    tcp.send (a)
    
    tcp.close()
sys.exit(0)
