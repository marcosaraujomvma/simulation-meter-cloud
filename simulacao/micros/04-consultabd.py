# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
import socket

import hashlib 
import psycopg2
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import time,random
from psycopg2 import extras

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8090            # Porta que o Servidor esta

#nmeter= sys.argv[1] #quantidade de medidores

fprcl = open("keys/inmetro-private.pem")#CAMINHO DA CHAVE PRIVADA DA NUVEM
keypr = RSA.importKey(fprcl.read())#importa a chave privada
print "LEU CHAVE PRIVADA DO INMETRO\n"

def saveTime(n_meter, dtime):
    con = psycopg2.connect(host='192.168.122.232', port='5432', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_micro')
    bd=con.cursor()
    sql="INSERT INTO tempo_agrega (n_meter,tempo) VALUES('%s','%s')"%(n_meter,dtime)
    #sql = "INSERT INTO tempo (n_meter,tempo)VALUES('%s','%s')"%(n_meter,dtime))
    #sql="INSERT INTO tempo (n_meter,tempo)VALUES('%s','%s')"%(n_meter,dtime))
    bd.execute(sql)
    con.commit()
    con.close()

def saveDb(id_medidor,fatura,signature,conferir):
    con = psycopg2.connect(host='localhost', port='5432', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_micro')
    bd=con.cursor()
    sql="INSERT INTO faturas (id_medidor, fatura,signature,conferencia) VALUES('%s','%s','%s','%s')"%(id_medidor,fatura,signature,conferir)
    #sql = "INSERT INTO tempo (n_meter,tempo)VALUES('%s','%s')"%(n_meter,dtime))
    #sql="INSERT INTO tempo (n_meter,naturetempo)VALUES('%s','%s')"%(n_meter,dtime))
    bd.execute(sql)
    con.commit()
    con.close()


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
        bd = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
        #bd = con.cursor()
        #print bd
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

def enviaDados(msg):
    try:
        
        HOST = 'localhost'     # Endereco IP do Servidor
        PORT = 8090          # Porta que o Servidor esta
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (HOST, PORT)
        tcp.connect(dest)
        
        tcp.send (msg)
            
        tcp.close()
    
    except:
        
        print "ERRO AO ENVIAR"
        
        
    
def fazerConsulta():
    #w = []
    id_medidor = random.randint(1,10) #raw_input("Digite o id do medidor:\n")
    ts_inicial = (time.time()) - 50 #raw_input("Digite o periodo Inicial: \n")
    ts_final = time.time() #raw_input("Digite o periodo Final: \n")
    
    inmetro_id,inmetro_leitura,inmetro_ts = pegaBancoInmetro(criarHash(str(id_medidor)),ts_inicial,ts_final)
    
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
    
    return id_medidor, soma, hashconf, ts_inicial,ts_final 
   

while True:
	time.sleep(6)
	time_start = time.time()
	id_medidor, op, hash_chain, ts_start, ts_final = fazerConsulta()
	#msg = ("%s;%s;%s"%(op,ts_start,ts_final)) #prepara a ms
	#hash_msg = criarHash(msg)#hash da mensagem
	#signature = keypr.sign(hash_msg,"") #assina a mensagem
	pkg = "%s;%s;%s;%s;%s;%s"%(id_medidor,op,hash_chain, ts_start, ts_final,time_start)
	#print pkg
	enviaDados(pkg)
"""
	
	saveDb(id_medidor,op,str(signature),"ok")
	time_end = time.time()
	saveTime(str(nmeter),time_end - time_start)
	time.sleep(5)
        #pkg = "%s;%s;%s;%s;%s"%(id_medidor,op,hash_chain, ts_start, ts_final)

"""