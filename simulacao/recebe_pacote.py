# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
import socket, ssl, thread
import sys


def enviaDados(msg):
     
    HOST = '127.0.0.1'     # Endereco IP do Servidor
    PORT = 8086            # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    #print 'Para sair use CTRL+X\n'
    msg = raw_input()
    while msg <> '\x18':
        tcp.send (msg)
    tcp.close()

def splitFrame(frame):
    """
    Função para separar os dados do Frame Recebido
    """
    split = frame.split(";")
    id_medidor =  split[0]#
    leitura =  split[1]
    ts_medidor = split[2]
    assinatura_str_tupla = split[3]
    assinatura_str = assinatura_str_tupla[1:len(assinatura_str_tupla)-2]
    assinatura_long = long(assinatura_str)
    assinatura_long_tupla = (assinatura_long,) 

    return (id_medidor,leitura,ts_medidor,assinatura_long_tupla)



def teste(newsock,fromaddr):

    """
        Função para receber os pacotes
        
    """
    
    conn = ssl.wrap_socket(newsock, server_side=True, certfile='chaves/certificado-chave.pem', keyfile='chaves/certificado-chave.pem')#certificado
    conn.setblocking(0)
    while True:
        try:
            buf = conn.read(512)#recebe os dados ja decodificado
            if buf == '':
                #print("nenhuma mensagem para receber!")
                
                break
            else:
                print (sys.getsizeof(buf))               
                id_medidor,leitura,ts_medidor,assinatura = splitFrame(buf)
                msg = ("%s;%s;%s",id_medidor,leitura,ts_medidor,assinatura)
                print (msg)
                enviaDados(msg)
                
               
        except:
            #print "err0"
            pass
            
    conn.close()
    thread.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8085))
sock.listen(1)
print("Servidor Funcionando!")

while True:
    newsock, fromaddr = sock.accept()
    #con, cliente = tcp.accept()
    
    thread.start_new_thread(teste,tuple([newsock,fromaddr]))
    print("Abriu nova Thread!")
