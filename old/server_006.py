# -*- coding: utf-8 -*-
#Servidor socket e
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import thread,time

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
#from Crypto import Random

from Crypto import Random
from Crypto.Cipher import AES
import base64

BLOCK_SIZE=32


HOST = ''              # Endereco IP do Servidor
PORT = 6000           # Porta que o Servidor esta
"""
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
"""
"""
def operacao(id_medidor,leitura):
    global id_c +=leitura
""" 
medidor01 = 0
medidor02 = 0
medidor03 = 0 

def decrypt(encrypted, passphrase):
    h = SHA256.new()
    h.update(passphrase)
    key = h.digest()[0:16]
    IV = Random.new().read(16)
    aes = AES.new(key, AES.MODE_CFB, IV)
    #deco = aes.decrypt(base64.b64decode(encrypted))
    
    return aes.decrypt(base64.b64decode(encrypted))
    
   
def conectado(con, cliente):
    
    
    print 'Conectado por', cliente
    """
    def operacao(medidor,leitura):
        medidor += leitura
        return medidor
    """

    while True:
        msg = con.recv(102400)
        if not msg: break
        
        
        
        #deco = decrypt(msg,"medidor")
    
        sp = msg.split(";")
        print sp
        n = sp[0]
        e = sp[1]
        signature = sp[2]
        ts = sp[3]
        id_medidor = sp[4]
        leitura = sp[5]
       
        sign = signature[1:(len(signature)-2)]
        long_sign = long(sign)
        tuple_long_sign = (long_sign,)
        
        
        com = (long(n),long(e))
        pub_key = RSA.construct(com)
        
        hash = SHA256.new(str(ts)).digest()
        #sign = long(signature)
              
        z = pub_key.verify(hash,tuple_long_sign)
        if z == True:
            print("Assinatura do Pacote OK!")
            print("Medidor %s, com Leitura %.2f e Time %s"%(id_medidor,float(leitura),ts))
            if float(id_medidor)==01:
                global medidor01
                medidor01 += float(leitura)
                print "O valor total : ",medidor01
                
            elif float(id_medidor)==02:
                global medidor02
                medidor02 += float(leitura)
                print "O valor total : ",medidor02
            elif float(id_medidor)==03:
                global medidor03
                medidor03 += float(leitura)
                print "O valor total : ",medidor03
            else:
                print("Medidor não cadastrado")
                con.close
            
        else:
            print("Pacate Corronpido!")
            con.close()
            thread.exit()
            
               

    print 'Finalizando conexao do cliente', cliente
    print "O valor total do Medidor 01 : ",medidor01
    print "O valor total do Medidor 02: ",medidor02
    print "O valor total do Medidor 03: ",medidor03
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)
print "Servidor OK! "

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()