# -*- coding: utf-8 -*-
#python 2.7
#marcosaraujo.mvma@gmail.com

import socket
import thread
from Crypto.PublicKey import RSA
import hashlib

HOST = 'localhost'              # ip Server
PORT = 8086            # Port Server

fprcl = open("keys/cloud-private.pem") ##chave para decodificar
keyprcl = RSA.importKey(fprcl.read())
print "LEU CHAVE PRIVADA 4096\n"

fprcl = open("keys/meter-public")
pubkey = RSA.importKey(fprcl.read())
print "LEU CHAVE PRUBLICA 1024 do MEDIDOR \n"




def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())

def enviaDados(msg):
    
    HOST = 'localhost'     # Endereco IP do Servidor
    PORT = 8087           # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    #print 'Para sair use CTRL+X\n'
    
    #while msg <> '\x18':
    tcp.send (msg)
        
    tcp.close()

def splitFrame(frame):
    """
    Função para separar os dados do Frame Recebido
    """
    split = frame.split(";")
    #print split
    id_medidor =  split[0]#
    leitura =  split[1]
    ts_medidor = split[2]
    assinatura_str_tupla = split[3]
    assinatura_str = assinatura_str_tupla[1:len(assinatura_str_tupla)-2]
    assinatura_long = long(assinatura_str)
    assinatura_long_tupla = (assinatura_long,) 

    return (id_medidor,leitura,ts_medidor,assinatura_long_tupla)


def conectado(con, cliente):
    #print 'Conectado por', cliente
   
    while True:
        msg = con.recv(8192000)
        if not msg: break
        con.close()
        
        split = msg.split(";/")
        cod = split[0]
        tempo = split[1]
        
        
        tupla = (cod,)
        
        
        
        dec = keyprcl.decrypt(tupla)
               
    
        #dec = keyprcl.decrypt(tupla)
    
        
        id_medidor,leitura,ts_medidor,assinatura = splitFrame(dec)
        
        
        pkg = "%s;%s;%s"%(id_medidor,leitura,ts_medidor)
        
        hash_msg = criarHash(pkg)
                  
        z = pubkey.verify(hash_msg,assinatura)
        
        if z == True:
		#print "ASSINATURA OK"
		send = "%s;%s;%s;%s;%s"%(id_medidor,leitura,ts_medidor,assinatura,tempo)
										
		enviaDados(send)
		thread.exit()
	else:
		print "ERRO NA ASSINATURA"
		thread.exit()
			
        
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(-1)
print "Decodifica pacote OK"

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
