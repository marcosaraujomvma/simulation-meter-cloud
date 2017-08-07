# -*- coding: utf-8 -*-

#python 2.7

from Crypto.PublicKey import RSA
import socket
import thread
import psycopg2
import hashlib
from Crypto.Cipher import PKCS1_OAEP
import base64

HOST = ''              # Endereco IP do Servidor
PORT = 8087            # Porta que o Servidor esta

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
        #bd = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        
        bd = con.cursor()
        print "retournou aqui!!!!!!!!!!!!!!!"
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
        print "retournou aqui"

        
        #print (lista_id_medidor,lista_leitura,lista_ts_medidor)
        return (lista_id_medidor,lista_leitura,lista_ts_medidor)
        
    except:
        print "erro!!!"        



def splitFrame(frame):
    """
    Função para separar os dados do Frame Recebido
    """
    split = frame.split(";")
    #print split
    id_medidor =  split[0]#
    op =  split[1]
    hash_chain = split[2]
    ts_start = split[3]
    ts_end = split[4]
    #assinatura_str_tupla = split[3]
    #assinatura_str = assinatura_str_tupla[1:len(assinatura_str_tupla)-2]
    #assinatura_long = long(assinatura_str)
    #assinatura_long_tupla = (assinatura_long,) 

    return (id_medidor,op,hash_chain,ts_start,ts_end)

def fazerConsulta(id_medidor, ts_inicial, ts_final):
    #w = []
    #id_medidor = raw_input("Digite o id do medidor:\n")
    #ts_inicial = raw_input("Digite o periodo Inicial: \n")
    #ts_final = raw_input("Digite o periodo Final: \n")
    
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
    
    
    print hashconf
    return hashconf


def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente
        
        id_medidor,op,hash_chain, ts_start, ts_end = splitFrame(msg)
 
        print id_medidor
        #print op
        print hash_chain,"\n\n"
        
        print ts_start,"\n"
        
        print ts_end,"\n"
        """    
        inmetro_id,inmetro_leitura,inmetro_ts = pegaBancoInmetro(criarHash(id_medidor),ts_start,ts_end)

        for i in range(len(inmetro_leitura)):
        """
        hash_bd = fazerConsulta(id_medidor, ts_start, ts_end)
        
        if hash_chain == hash_bd:
            print "ok!!!!!!!!!!!!!!\n\n\n"
        else:
            print "Erro nos pacotes para o Calculo!!!!"

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