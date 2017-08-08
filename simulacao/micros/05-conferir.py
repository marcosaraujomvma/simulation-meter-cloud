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
        
        con = psycopg2.connect(host='192.168.122.232', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_micro')
        #print con
        #print "+++++AAAAAAAAAAAAAAAAAAA"
        bd = con.cursor()
        #bd = con.cursor()
        #print bd
        #print "AAAAAAAAAAAAAAAAAAA"
        sql = "select (id_medidor,leitura,ts_medidor) from logmedidores where id_medidor = '%s' and ts_medidor between '%s' and '%s'"%(id_meter,ts_start,ts_end)
        
        #print sql
        
        bd.execute(sql)
        
        dados = bd.fetchall()
        #print dados
        
        con.commit()
        con.close()
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
    tempo = split[5]
    #assinatura_str_tupla = split[3]
    #assinatura_str = assinatura_str_tupla[1:len(assinatura_str_tupla)-2]
    #assinatura_long = long(assinatura_str)
    #assinatura_long_tupla = (assinatura_long,) 

    return (id_medidor,op,hash_chain,ts_start,ts_end, tempo)

def fazerConsulta(id_medidor, ts_start, ts_end):
    #w = []
    #id_medidor = random.randint(1,10) #raw_input("Digite o id do medidor:\n")
    ##ts_final = time.time() #raw_input("Digite o periodo Final: \n")
    
    inmetro_id,inmetro_leitura,inmetro_ts = pegaBancoInmetro(criarHash(str(id_medidor)),ts_start,ts_end)
    
    hashconf=""
    soma = 0
    
    key = RSA.importKey(open('keys/inmetro-private.pem').read())
    cipher = PKCS1_OAEP.new(key)

    tam = len(inmetro_leitura)
    #print tam
    for i in range(tam):
            
        
        z = inmetro_leitura[i]
        #print z
        x = base64.b64decode(z)
        #x = z.decode('UTF-8')
        #print x
        message = cipher.decrypt(x)
        
        soma += int(message)
        
        hashconf = hashconf + criarHash(inmetro_id[i]+message+inmetro_ts[i])
    
    
       
    
    #print soma
    
    return hashconf


def conectado(con, cliente):
    #print 'Conectado por', cliente

    while True:
        msg = con.recv(819200)
        if not msg: break
        con.close()
        #print cliente
        
        id_medidor,op,hash_chain, ts_start, ts_end,tempo = splitFrame(msg)
        if hash_chain =='':
            print "VAZIO HASH CHAIN"
       
        hash_bd = fazerConsulta(str(id_medidor), str(ts_start), str(ts_end))
        
        if hash_chain == hash_bd:
            print "CONFERIDO CORRETO!\n\n\n"
            thread.exit()
        else:
            print "Erro nos pacotes para o Calculo!!!!"

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()