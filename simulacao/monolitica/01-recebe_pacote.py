# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
import socket, thread

from Crypto.PublicKey import RSA

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8085            # Porta que o Servidor esta


def enviaDados(msg):
    
    HOST = 'localhost'     # Endereco IP do Servidor
    PORT = 8086           # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    #print 'Para sair use CTRL+X\n'
    
    #while msg <> '\x18':
    tcp.send (msg)
        
    tcp.close()

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(4096)
        if not msg: break
        print cliente, msg

        

        enviaDados(msg)

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