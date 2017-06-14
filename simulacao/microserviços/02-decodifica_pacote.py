# -*- coding: utf-8 -*-
#python 2.7
#marcosaraujo.mvma@gmail.com

import socket
import thread
from Crypto.PublicKey import RSA
import hashlib
import psycopg2
from Crypto.Cipher import PKCS1_OAEP
import base64

HOST = 'localhost'              # ip Server
PORT = 8086            # Port Server

fprcl = open("chaves/cloudPrivate.pem")
keyprcl = RSA.importKey(fprcl.read())
print "LEU CHAVE PRIVADA 4096\n"

fprcl = open("chaves/medidor1_Publickey.pem")
pubkey = RSA.importKey(fprcl.read())
print "LEU CHAVE PRUBLICA 1024 do MEDIDOR \n"


def cryptText(plain_text):
    
    """
        marcosaraujo.mvma@gmail.com
        Encrypts the text and returns the text encrypted in UTF-8 base64
    """
    
    key = RSA.importKey(open('chaves/keypu.pem').read())
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(plain_text.encode('UTF-8'))
    print type(ciphertext)
    #print (base64.b64encode(ciphertext))
    b64cipher = base64.b64encode(ciphertext)
    return b64cipher

def gravaBancoDadosInmetro(id_meter,metering,ts,signature):
    """
        marcosaraujo.mvma@gmail.com
        Responsible function in writing the data in the database
        
    """
    
    con = psycopg2.connect(host='192.168.122.232', user='postgres', password='postgres',dbname='inmetrobd')
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

    print sql
    bd.execute(sql)

    con.commit()

    con.close()
    
    print "Dados Gravados No Banco do Inmetro"

def criarHash(texto):
    """
    Funçãor responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())


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

def splitFrame(frame):
    """
    Função para separar os dados do Frame Recebido
    """
    split = frame.split(";")
    print split
    id_medidor =  split[0]#
    leitura =  split[1]
    ts_medidor = split[2]
    assinatura_str_tupla = split[3]
    assinatura_str = assinatura_str_tupla[1:len(assinatura_str_tupla)-2]
    assinatura_long = long(assinatura_str)
    assinatura_long_tupla = (assinatura_long,) 

    return (id_medidor,leitura,ts_medidor,assinatura_long_tupla)


def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente
        tupla = (msg,)
        #print tupla
        dec = keyprcl.decrypt(tupla)
        print "Mensagen Decodificada"
        print dec

        id_medidor,leitura,ts_medidor,assinatura = splitFrame(dec)
        
        print id_medidor
        
        print leitura
        
        print ts_medidor
        
        print assinatura
        
        #print type(assinatura)
        
        pkg = "%s;%s;%s"%(id_medidor,leitura,ts_medidor)
        
        hash_msg = criarHash(pkg)          
    
        z = pubkey.verify(hash_msg,assinatura)


        print "\n Assinatura Correta:",z
        
        gravaBancoDadosInmetro(id_medidor,leitura,ts_medidor,assinatura)
        #enviaDados(msg)
        #print "\n Mensagem enviada!!!\n--------------------------"

    print '\nFinalizando conexao do cliente', cliente
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
