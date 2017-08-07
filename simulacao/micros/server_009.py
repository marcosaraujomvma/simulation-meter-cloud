# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
import socket, ssl, thread,time,hashlib
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import inmetro
import psycopg2
from psycopg2 import extras
import sys

ts = 0
lista = []
hash_chain = ""
cont01 = 0
ts_inicial01 = ""
ts_final01 = ""
fat01 = ""


def criarHash(texto):
    """
    Função responsavel em criar Hash com algoritmo SHA 256
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
    assinatura_str_tupla = split[3]
    assinatura_str = assinatura_str_tupla[1:len(assinatura_str_tupla)-2]
    assinatura_long = long(assinatura_str)
    assinatura_long_tupla = (assinatura_long,) 

    return (id_medidor,leitura,ts_medidor,assinatura_long_tupla)


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
        dados = bd.fetchall()
        #print dados
        
        con.commit()
        for i in range(len(dados)):
            aux = (dados[i][0].strip("(").strip(")"))
            sp = aux.split(",")
            lista_id_medidor.append(sp[0])
            lista_leitura.append(sp[1])
            lista_ts_medidor.append(sp[2])
        print ("retournou aqui")

        
        #print (lista_id_medidor,lista_leitura,lista_ts_medidor)
        return (lista_id_medidor,lista_leitura,lista_ts_medidor)
        
    except:
        print ("erro!!!")

def conferirInmetro(id_medidor,ts_inicial,ts_final,hash_rastro):
    hashconf = ""

    lista_hash_inmetro_id = []
    rastro_id = []

    lista_hash_inmetro_leitura = []
    rastro_leitura = []
    inmetro_leitura = []

    rastro_ts = []
    inmetro_ts = [] 
    
    inmetro_id,inmetro_leitura,inmetro_ts = pegaBancoInmetro(id_medidor,ts_inicial,ts_final)#recupera do banco do inmetro
    print ("aquiiiiiiii!!!!!!!!")
    hs_id_medidor = criarHash(id_medidor)#cria o hash do id do medidor
    #print inmetro_id,inmetro_leitura,inmetro_ts
    #rastro_id,rastro_leitura,rastro_ts = audit.pegaBancoRastro(str(hs_id_medidor),ts_inicial,ts_final)#recupera do banco do rastro
    tam = len(inmetro_leitura)
    print (tam,"ssssssssssssssssssss")
    for i in range(tam):
        print ("aquiiiiiiii!!!!!!!!")
        hashconf = hashconf + criarHash(inmetro_leitura[i]+inmetro_ts[i])
        print (hashconf)
        #hash_inmetro_id = criarHash()
        #hash_inmetro_leitura = criarHASH(inmetro_leitura[i])

        #lista_hash_inmetro_id.append(hash_inmetro_id)
        #lista_hash_inmetro_leitura.append(hash_inmetro_leitura)
    #print hash_rastro,'\n'
    print (hashconf)
    z = hashconf == hash_rastro
    print (hashconf,"\n")
    print (hash_rastro)
    hash_rastro = ""
    hashconf = ""

    if z == True:
        print ("CORRETTOOOOOOOOOOOO!!!!!")
        hash_rastro = ""
        hashconf = ""
        return True
    else:
        print ("INCORRETO")
        return False



def teste(newsock,fromaddr):
    
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.bind(('', 8081))
    #sock.listen(1)
    #newsock, fromaddr = sock.accept()
    conn = ssl.wrap_socket(newsock, server_side=True, certfile='chaves/certificado-chave.pem', keyfile='chaves/certificado-chave.pem')#certificado
    conn.setblocking(0)
    #fpu = open("chaves/medidor01_Publickey.pem")
    #public_key = RSA.importKey(fpu.read())
    while True:
        try:
            buf = conn.read(512)#recebe os dados ja decodificado
            if buf == '':
                #print("nenhuma mensagem para receber!")
                
                break
            else:
                print (sys.getsizeof(buf))               
                id_medidor,leitura,ts_medidor,assinatura = splitFrame(buf)
                #print ts_medidor
                print (type(ts_medidor))
                msg = ("%s;%s"%(str(leitura),str(ts_medidor)))

                conferir_assinatura = inmetro.conferirAssinatura(id_medidor,msg,assinatura)
    
                #print conferir_assinatura
                #print id_medidor
                if conferir_assinatura == True:
                    inmetro.gravaBancoDadosInmetro(id_medidor,leitura,ts_medidor)
                    if int(id_medidor) == 1:
                        global cont01
                        cont01 += 1
                        #print ts_medidor
                        global hash_chain
                        #global ts_inicial01
                        #global ts_final01
                        hash_chain += criarHash(leitura+ts_medidor)
                        #print hash_chain
                        #print ts_inicial_01
                        #print ts_final01
                        print (cont01)
                        print (type(cont01))
                        if cont01 == 1:
                            ts_inicial01 = ts_medidor
                            print (ts_inicial01)
                        if cont01 == 5:
                            ts_final01 = ts_medidor
                            print (ts_final01)
                            print ("Conferir dados")
                            print (id_medidor)
                            print (ts_inicial01)
                            print (ts_final01)
                            print (hash_chain)
                            w = inmetro.conferirInmetro(id_medidor,ts_inicial01,ts_final01,hash_chain)
                            hash_chain = ""
                            cont01 = 0
                            if w == True:
                                print ("@@@@@@@@@@@@@@ok")
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




