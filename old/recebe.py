#auditor

import hashlib, pprint
import psycopg2
from psycopg2 import extras

lista_id_medidor = []
lista_leitura = []
lista_ts_medidor = []

def criarHASH(texto):

    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())

def pegaBancoInmetro(id_valor,ts_inicial,ts_final):
    con = psycopg2.connect(host='192.168.122.13', user='postgres', password='postgres',dbname='inmtroLog')
    bd = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    sql = "select (id_medidor,leitura,ts_medidor) from logmedidor where id_medidor = '%s' and ts_medidor between '%s' and '%s'"%(id_valor,ts_inicial,ts_final)
    bd.execute(sql)
    dados = bd.fetchall()
    con.commit()
    for i in range(len(dados)):
        aux = (dados[i][0].strip("(").strip(")"))
        sp = aux.split(",")
        lista_id_medidor.append(sp[0])
        lista_leitura.append(sp[1])
        lista_ts_medidor.append(sp[2])
        
    return (lista_id_medidor,lista_leitura,lista_ts_medidor)

def pegaBancoRastro(id_valor,ts_inicial,ts_final):
    con = psycopg2.connect(host='192.168.122.13', user='postgres', password='postgres',dbname='rastro')
    bd = con.cursor(cursor_factory = psycopg2.extras.DictCursor)
    sql = "select (id_medidor,leitura,ts_medidor) from rastros where id_medidor = '%s' and ts_medidor between '%s' and '%s'"%(id_valor,ts_inicial,ts_final)
    bd.execute(sql)
    dados01= bd.fetchall()
    #pprint.pprint(dados)
    con.commit()
    for i in range(len(dados01)):
        aux = (dados01[i][0].strip("(").strip(")"))
        sp = aux.split(",")
        lista_id_medidor.append(sp[0])
        lista_leitura.append(sp[1])
        lista_ts_medidor.append(sp[2])
        
    return (lista_id_medidor,lista_leitura,lista_ts_medidor)



