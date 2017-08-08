# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
import socket, thread,time


HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8085            # Porta que o Servidor esta


def enviaDados(msg):
    
    HOST = 'localhost'     # Endereco IP do Servidor
    PORT = 8086           # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send (msg)       
    tcp.close()

def conectado(con, cliente):
    #print 'Conectado por', cliente
    #print "RECEBER PACOTE OK""""
    while True:
        msg = con.recv(8192)
        if not msg: break
        con.close()
        
        tempo_start = time.time()
        pkg = ("%s;/%s"%(msg,tempo_start)) #prepara a msg
        enviaDados(pkg)
    	thread.exit()




tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(-1)

print "RECEBER PACOTE OK"

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))
tcp.close()
