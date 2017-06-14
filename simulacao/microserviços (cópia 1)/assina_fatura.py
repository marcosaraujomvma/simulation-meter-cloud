# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
#assina fatura

import socket
import thread, hashlib
from Crypto.PublicKey import RSA

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8093            # Porta que o Servidor esta

fpr = open("chaves/inmetroPrivate.pem")
key = RSA.importKey(fpr.read())
print "LEU CHAVE PRIVADA 1024 INMETRO \n"

def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())


def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente
        print msg
        
        

    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))
tcp.close()