# -*- coding: utf-8 -*-
#Inmetro deve rodar no sgx
#python 2.7
import socket, ssl, thread,time, hashlib
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import psycopg2


def criarHash(texto):
    """
    Função responsavel em criar Hash com algoritmo SHA 256
    """
    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())

def gravaBancoDadosInmetro(id_medidor,leitura,ts):

    has = criarHash(leitura + ts)

    fpr = open("chaves/inmetroPrivate.pem")
    
    key = RSA.importKey(fpr.read())
    
    assinatura = key.sign(has,"")
    
    con = psycopg2.connect(host='192.168.122.232', user='postgres', password='postgres',dbname='inmetrobd')

    bd = con.cursor()

    sql = "INSERT INTO logmedidores (id_medidor,leitura,ts_medidor,assinatura)VALUES ('%s','%s','%s','%s')"%(id_medidor,leitura,ts,assinatura)


    bd.execute(sql)

    con.commit()

    con.close()
    
    print "Dados Gravados No Banco do Inmetro"

def conferirAssinatura(id_medidor,msg,assinatura):
    """
    Função Responsavel em pegar as chaves publicas do medidor   
    """
    path = "chaves/medidor%s_Publickey.pem"%id_medidor
    fpu = open(path)
    public_key = RSA.importKey(fpu.read())
    has = criarHash(msg)

    if True == public_key.verify(has,assinatura):
        print "Assinatura Conferida Correta"
        return True
        
    else:
        print "Assinatura Incorreta"
        return False


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
        print "retournou aqui"

        
        #print (lista_id_medidor,lista_leitura,lista_ts_medidor)
        return (lista_id_medidor,lista_leitura,lista_ts_medidor)
        
    except:
        print "erro!!!"

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
    print "aquiiiiiiii!!!!!!!!"
    hs_id_medidor = criarHash(id_medidor)#cria o hash do id do medidor
    #print inmetro_id,inmetro_leitura,inmetro_ts
    #rastro_id,rastro_leitura,rastro_ts = audit.pegaBancoRastro(str(hs_id_medidor),ts_inicial,ts_final)#recupera do banco do rastro
    tam = len(inmetro_leitura)
    print tam,"ssssssssssssssssssss"
    for i in range(tam):
        print "aquiiiiiiii!!!!!!!!"
        hashconf = hashconf + criarHash(inmetro_leitura[i]+inmetro_ts[i])
        print hashconf
        #hash_inmetro_id = criarHash()
        #hash_inmetro_leitura = criarHASH(inmetro_leitura[i])

        #lista_hash_inmetro_id.append(hash_inmetro_id)
        #lista_hash_inmetro_leitura.append(hash_inmetro_leitura)
    #print hash_rastro,'\n'
    print hashconf
    z = hashconf == hash_rastro
    print hashconf,"\n"
    print hash_rastro
    hash_rastro = ""
    hashconf = ""

    if z == True:
        print "CORRETTOOOOOOOOOOOO!!!!!"
        hash_rastro = ""
        hashconf = ""
        return True
    else:
        print"INCORRETO"
        return False
