# -*- coding: utf-8 -*-
#python 2.7
import socket
import thread
import psycopg2
import base64
from Crypto.PublicKey import RSA
import time
import sys
from Crypto.Cipher import PKCS1_OAEP

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8087            # Porta que o Servidor esta

nmeter = sys.argv[1]

def saveTime(n_meter, dtime):
    con = psycopg2.connect(host='192.168.122.232', port='5432', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_micro')
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
    tempo = split[4] 

    return (id_medidor,leitura,ts_medidor,assinatura_long_tupla,tempo)


def gravaBancoDadosInmetro(id_meter,metering,ts,signature):
    """
        marcosaraujo.mvma@gmail.com
        Responsible function in writing the data in the database
        
    """
    
    con = psycopg2.connect(host='192.168.122.232',port='5432', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_micro')
    bd = con.cursor()
    """
    key = RSA.importKey(open('chaves/keypu.pem').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(leitura.encode('UTF-8'))
    print type(ciphertext)
    #print (base64.b64encode(ciphertext))
    b64cipher = base64.b64encode(ciphertext)
    """
    metering_b64cipher = cryptText(metering) #Encrypts the text and returns the text encrypted in UTF-8 base64
    
    sql = "INSERT INTO logmedidores (id_medidor,leitura,ts_medidor,assinatura)VALUES ('%s','%s','%s','%s')"%(id_meter,metering_b64cipher,ts,str(signature))

    #print sql
    bd.execute(sql)

    con.commit()

    con.close()
    
    #print "Dados Gravados No Banco do Inmetro"

def conectado(con, cliente):
  

    while True:
        msg = con.recv(1024)
        if not msg: break
        con.close()
        id_medidor,leitura,ts_medidor,assinatura,tempo = splitFrame(msg)
        gravaBancoDadosInmetro(id_medidor,leitura,ts_medidor,assinatura)
	end = time.time()
	deltatime= end-float(tempo)
	saveTime(str(nmeter),str(deltatime))
        #print tempo
        
        thread.exit()
        
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(-1)
print "GRAVA BANCO OK OK"

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
