# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes
#Servidor pode ser usado para linux e windows
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 2.7

import socket, ssl
import thread

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta
lista = []
arq = open('lista','w')
def conectado(con, cliente): #função para abrir conexão
    print 'Conectado por Medidor: ', cliente

    while True:
        con = ssl.wrap_socket(con, server_side=True, certfile='cert.pem', keyfile='cert.pem')
        con.setblocking(0)
   	msg= con.recv(1024)
   	if not msg: break
   	print msg
   	gra = str(msg) + str(cliente) + "\n"
   	lista.append(gra)
   	arq.writelines(lista)
   	#lista.append()
			
    print 'Finalizando conexao do Medidor', cliente
		
		#print lista
		#arq.writelines(lista)
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
    
   
