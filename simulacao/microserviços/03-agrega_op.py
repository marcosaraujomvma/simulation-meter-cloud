# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
import socket

import hashlib 
import psycopg2
from psycopg2 import extras
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8090            # Porta que o Servidor esta


def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())


def pegaBancoInmetro(id_meter,ts_start,ts_end):

    lista_id_medidor = []
    lista_leitura = []
    lista_ts_medidor = []
    try: 
    
        con = psycopg2.connect(host='192.168.122.232', user='postgres', password='postgres',dbname='inmetrobd')
        #print con
        bd = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #bd = con.cursor()
        #print bd
        sql = "select (id_medidor,leitura,ts_medidor) from logmedidores where id_medidor = '%s' and ts_medidor between '%s' and '%s'"%(id_meter,ts_start,ts_end)
        
        print sql
        
        bd.execute(sql)
        
        dados = bd.fetchall()
        #print dados
        
        con.commit()
        for i in range(len(dados)):
            aux = (dados[i][0].strip("(").strip(")"))
            sp = aux.split(",")
            lista_id_medidor.append(sp[0])
            lista_leitura.append(sp[1])
            lista_ts_medidor.append(sp[2])
        #print "retournou aqui"

        
        #print (lista_id_medidor,lista_leitura,lista_ts_medidor)
        return (lista_id_medidor,lista_leitura,lista_ts_medidor)
        
    except:
        print "erro!!!"        

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
    
    
def fazerConsulta():
    #w = []
    id_medidor = raw_input("Digite o id do medidor:\n")
    ts_inicial = raw_input("Digite o periodo Inicial: \n")
    ts_final = raw_input("Digite o periodo Final: \n")
    
    inmetro_id,inmetro_leitura,inmetro_ts = pegaBancoInmetro(criarHash(id_medidor),ts_inicial,ts_final)
    
    hashconf=""
    soma = 0
    
    key = RSA.importKey(open('chaves/keypr.pem').read())
    cipher = PKCS1_OAEP.new(key)

    tam = len(inmetro_leitura)
    print tam
    for i in range(tam):
        #print "aquiiiiiiii!!!!!!!!"
        
        
        z = inmetro_leitura[i]
        #print z
        x = base64.b64decode(z)
        #x = z.decode('UTF-8')
        #print x
        message = cipher.decrypt(x)
        
        soma += int(message)
        
        hashconf = hashconf + criarHash(inmetro_id[i]+message+inmetro_ts[i])
    
    
        print message,"\n"
        
        
    print hashconf,"\n"
        #print(message.decode('utf-8'))
    
    
    print soma
    
    return id_medidor, soma, hashconf, ts_inicial,ts_final 
    #print inmetro_id
    #print inmetro_leitura
    #print inmetro_ts

id_medidor, op, hash_chain, ts_start, ts_final = fazerConsulta()
pkg = "%s;%s;%s;%s;%s"%(id_medidor,op,hash_chain, ts_start, ts_final)
enviaDados(pkg)
"""
def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(4096)
        if not msg: break
        print cliente, msg

        

        #enviaDados(msg)

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
"""