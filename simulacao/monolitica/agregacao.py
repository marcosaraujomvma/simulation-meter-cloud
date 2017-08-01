# -*- coding: utf-8 -*-
#python 2.7
import socket
import thread
import hashlib


HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8090            # Porta que o Servidor esta


ts = 0
lista = []
hash_chain = ""
cont01 = 0
ts_inicial01 = ""
ts_final01 = ""
fat01 = 0

def enviaDados(msg):
    
    HOST = 'localhost'     # Endereco IP do Servidor
    PORT = 8091           # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send (msg)
        
    tcp.close()

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


def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        #print cliente
        print ("AGREAGACAO!!!")
        #print msg
        id_medidor,leitura,ts_medidor = splitFrame(msg)
        ########################################################
        if int(id_medidor) == 1:
                        global cont01
                        global fat01
                        cont01 += 1
                        #print ts_medidor
                        global hash_chain
                        #global ts_inicial01
                        #global ts_final01
                        hash_chain += criarHash(id_medidor+leitura+ts_medidor)
                        print hash_chain
                        #print ts_inicial_01
                        #print ts_final01
                        print (cont01)
                        #print (type(cont01))
                        fat01 += int(leitura)
                        global ts_inicial01 
                        if cont01 == 1:
                            ts_inicial01 = ts_medidor
                            print (ts_inicial01)
                        if cont01 == 5:
                            ts_final01 = ts_medidor
                            
                            print (ts_inicial01)
                            print (ts_final01)
                            print ("Conferir dados")
                            print (id_medidor)
                            #print (ts_inicial01)
                            #print (ts_final01)
                            print (hash_chain)
                            print (type(hash_chain))

                            print("FATURA FECHADA MENSAL: ", fat01)
                            pkg = "%s;%s;%s;%s;%s"%(id_medidor,fat01,hash_chain,ts_inicial01,ts_final01)
                            enviaDados(pkg)

                            hash_chain = ""
                            cont01 = 0
                            fat01=0
                            
        ########################################################
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