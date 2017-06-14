# -*- coding: utf-8 -*-
import socket
import thread
import hashlib
from Crypto.PublicKey import RSA

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8088            # Porta que o Servidor esta

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

def splitFrame(frame):
    """
    Função para separar os dados do Frame Recebido
    """
    split = frame.split(";")
    id_medidor =  split[0]#
    leitura =  split[1]
    ts_medidor = split[2]
    return (id_medidor,leitura,ts_medidor)

def enviaDados(msg):
    
    HOST = 'localhost'     # Endereco IP do Servidor
    PORT = 8089           # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send (msg)
        
    tcp.close()

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente
        print msg
        
        id_medidor,leitura,ts_medidor = splitFrame(msg)
        
        print id_medidor
        
        print leitura
        
        print ts_medidor

        pkg = "%s;%s;%s"%(id_medidor,leitura,ts_medidor)

        hash,
        hash_pkg = criarHash(pkg)
        
        signature = key.sign(hash_pkg,"")
        print "ASSINOU COM CHAVE PRIVADA do INMETRO 1024\n"
        #print (signature)

        pkg_send = ("%s;%s"%(pkg,signature))
        
        print pkg_send
        
        enviaDados(pkg_send)

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