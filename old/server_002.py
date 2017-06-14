# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes
#Servidor pode ser usado para linux e windows
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 2.7
import socket, ssl, thread,time

ts = 0
lista = []

def teste(newsock,fromaddr):
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.bind(('', 8081))
    #sock.listen(1)
    #newsock, fromaddr = sock.accept()
    conn = ssl.wrap_socket(newsock, server_side=True, certfile='cert.pem', keyfile='cert.pem')#certificado
    conn.setblocking(0)
    while True:
        try:
            buf = conn.read(512)
            if buf == '':
                #print("nenhuma mensagem para receber!")
                
                break
            else:
                arq = open('lista.txt','w')
                ts = time.time()
                print ("ID;NºPCT;TSM;TSS\n%s;%s"%(buf,ts))
                lista.append("%s;%s\n"%(buf,ts))
                #print(lista)
                arq.writelines(lista)
                arq.close()
                
                
        except:
            pass
            
    conn.close()
    thread.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8081))
sock.listen(1)
print("Servidor Funcionando!")

while True:
    newsock, fromaddr = sock.accept()
    #con, cliente = tcp.accept()
    
    thread.start_new_thread(teste,tuple([newsock,fromaddr]))
    print("Abriu nova Thread!")




