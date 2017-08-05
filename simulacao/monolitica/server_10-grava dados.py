# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
import socket
import thread
from Crypto.PublicKey import RSA
import hashlib
import psycopg2
from Crypto.Cipher import PKCS1_OAEP
import base64
import time


HOST = 'localhost'              # Endereco IP do Servidor
PORT = 10010            # Porta que o Servidor esta
nmeter = 200

fprcl = open("keys/cloud-private.pem")#CAMINHO DA CHAVE PRIVADA DA NUVEM
keyprcl = RSA.importKey(fprcl.read())#importa a chave privada
print "LEU CHAVE PRIVADA DA CLOUD 4096\n"

fprcl = open("keys/meter-public")
pubkey = RSA.importKey(fprcl.read())
print "LEU CHAVE PRUBLICA 1024 do MEDIDOR \n"



def saveTime(n_meter, dtime):
    con = psycopg2.connect(host='localhost', port='5432', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_mono')
    bd=con.cursor()
    sql="INSERT INTO tempo_recebe (n_meter,tempo) VALUES('%s','%s')"%(n_meter,dtime)
    #sql = "INSERT INTO tempo (n_meter,tempo)VALUES('%s','%s')"%(n_meter,dtime))
    #sql="INSERT INTO tempo (n_meter,tempo)VALUES('%s','%s')"%(n_meter,dtime))
    bd.execute(sql)
    con.commit()
    con.close()

    
	

def cryptText(plain_text):
    
    """
        marcosaraujo.mvma@gmail.com
        Encrypts the text and returns the text encrypted in UTF-8 base64
    """
    
    key = RSA.importKey(open('keys/inmetro-public').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(plain_text.encode('UTF-8'))
    #print type(ciphertext)
    #print (base64.b64encode(ciphertext))
    b64cipher = base64.b64encode(ciphertext)
    return b64cipher


def splitFrame(frame):
    """
    Função para separar os dados do Frame Recebido
    """
    split = frame.split(";")
    #print split
    id_medidor =  split[0]#
    leitura =  split[1]
    ts_medidor = split[2]
    assinatura_str_tupla = split[3]
    assinatura_str = assinatura_str_tupla[1:len(assinatura_str_tupla)-2]
    assinatura_long = long(assinatura_str)
    assinatura_long_tupla = (assinatura_long,) 

    return (id_medidor,leitura,ts_medidor,assinatura_long_tupla)

def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())


def gravaBancoDadosInmetro(id_meter,metering,ts,signature):
    """
        marcosaraujo.mvma@gmail.com
        Responsible function in writing the data in the database
        
    """
    metering_b64cipher = cryptText(metering)
    con = psycopg2.connect(host='localhost', port='5432', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_mono')
    bd = con.cursor()
    """
    key = RSA.importKey(open('chaves/keypu.pem').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(leitura.encode('UTF-8'))
    print type(ciphertext)
    #print (base64.b64encode(ciphertext))
    b64cipher = base64.b64encode(ciphertext)
    """
    #metering_b64cipher = cryptText(metering) #Encrypts the text and returns the text encrypted in UTF-8 base64
    
    sql = "INSERT INTO logmedidores (id_medidor,leitura,ts_medidor,assinatura)VALUES ('%s','%s','%s','%s')"%(id_meter,metering_b64cipher,ts,str(signature))

    #print sql
    bd.execute(sql)

    con.commit()

    con.close()
    
    #print "Dados Gravados No Banco do Inmetro"


def conectado(con, cliente):
    #print 'Conectado por', cliente

    while True:
        msg = con.recv(4096)
        con.close()
        if not msg: break
        #print cliente,
        start = time.time()
        tupla = (msg,)
        msg_decodificada=keyprcl.decrypt(tupla)#decodifica a mensagem com a chave privada da nuvem
        #print(msg_decodificada)
        id_medidor,leitura,ts_medidor,assinatura = splitFrame(msg_decodificada)#SEPARA O FRAME
        
        #print id_medidor
		
		#print id_medidor
        
        #print leitura
        
        #print ts_medidor
        
        #print assinatura
        
        pkg = "%s;%s;%s"%(id_medidor,leitura,ts_medidor)
        
        hash_msg = criarHash(pkg)          
    
        z = pubkey.verify(hash_msg,assinatura)
        
        if True:
			gravaBancoDadosInmetro(id_medidor,leitura,ts_medidor,assinatura)
			end = time.time()
			saveTime(str(nmeter),end-start) #grava o tempo de processamento 
			
			thread.exit()
		#print 'Finalizando conexao do cliente', cliente
		#con.close()
		#print "Final fthres"
		#thread.exit()
    

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(-1)
print "SERVIDOR OK! ATIVO"
while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
