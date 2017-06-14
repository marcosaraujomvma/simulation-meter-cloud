# -*- coding: utf-8 -*-
import socket
import thread,time
import sys
from Crypto.PublicKey import RSA
import hashlib 
import psycopg2
from psycopg2 import extras

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8091            # Porta que o Servidor esta
PORT2 = 8095

def splitFrame(frame):
    """
    Função para separar os dados do Frame Recebido
    """
    split = frame.split(";")
    id_medidor =  split[0]#
    leitura =  split[1]
    hash_chain = split[2]
    ts_inicial = split[3]
    ts_final = split[4]
    return (id_medidor,leitura,hash_chain,ts_inicial,ts_final)

def pegaBancoInmetro(id_valor,ts_inicial,ts_final):

    lista_id_medidor = []
    lista_leitura = []
    lista_ts_medidor = []
    try: 
    
        con = psycopg2.connect(host='192.168.122.232', user='postgres', password='postgres',dbname='inmetrobd')
        #print con
        bd = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #bd = con.cursor()
        #print bd
        sql = "select (id_medidor,leitura,ts_medidor) from logmedidores where id_medidor = '%s' and ts_medidor between '%s' and '%s'"%(id_valor,ts_inicial,ts_final)
        bd.execute(sql)
        print sql
        dados = bd.fetchall()
        #print dados
        
        con.commit()
        for i in range(len(dados)):
            aux = (dados[i][0].strip("(").strip(")"))
            sp = aux.split(",")
            lista_id_medidor.append(sp[0])
            lista_leitura.append(sp[1])
            lista_ts_medidor.append(sp[2])
        print "retournou aqui"

        
        #print (lista_id_medidor,lista_leitura,lista_ts_medidor)
        return (lista_id_medidor,lista_leitura,lista_ts_medidor)
        
    except:
        print "erro!!!"        


def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())

def enviaDados(msg):
    
    HOST = 'localhost'     # Endereco IP do Servidor
    PORT = 8093           # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    tcp.send (msg)        
    tcp.close()


def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(4096)
        if not msg: break
        print cliente
        #print msg
        z = sys.getsizeof(msg)
        print z
        
        id_medidor,fatura,hash_chain,ts_inicial,ts_final = splitFrame(msg)
        print "\nId do Medidor: ",id_medidor
        print "\nFATURA MES: ",fatura
        print "\nHASH CHAIN: ",hash_chain
        print "\nTS INICIAL: ",ts_inicial
        print "\nTS FINAL: ",ts_final
        print "====================================================================================="
        time.sleep(0.05)
        inmetro_id,inmetro_leitura,inmetro_ts = pegaBancoInmetro(id_medidor,ts_inicial,ts_final)
        
        print inmetro_id
        print inmetro_leitura
        print inmetro_ts
        


        tam = len(inmetro_leitura)
        print tam,"ssssssssssssssssssss"
        hashconf = ""
        for i in range(tam):
            print "aquiiiiiiii!!!!!!!!"
            hashconf = hashconf + criarHash(inmetro_id[i]+inmetro_leitura[i]+inmetro_ts[i])
                
    print "\nHASH CONF: ",hashconf
    z = hashconf == hash_chain

    
   
   

    if z == True:
        print "CORRETTOOOOOOOOOOOO!!!!!"
        
        pkg = "%s;%s;%s"%(id_medidor, fatura,"ok")
        enviaDados(pkg)
        hashconf = ""
        return True
    else:
        print"INCORRETO"
        
        pkg = "%s;%s;%s"%(id_medidor, fatura,"erro billing")
        enviaDados(pkg)
        
        hashconf = ""
        return False
        
        #pkg = "%s;%s;%s;%s;%s"%(id_medidor,leitura,hash_chain,ts_inicial,ts_final)
        
        
    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tcp2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)
#orig2 = (HOST, PORT2)

tcp.bind(orig)
tcp.listen(1000000)

#tcp2.bind(orig2)
#tcp2.listen(1)

while True:
    con, cliente = tcp.accept()
    #con2, cliente2 = tcp2.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))
    #thread.start_new_thread(conectado, tuple([con2, cliente2]))

tcp.close()
#tcp2.close()