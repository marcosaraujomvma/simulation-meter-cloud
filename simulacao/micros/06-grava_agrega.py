# -*- coding: utf-8 -*-
#Servidor Socket com thread concorrentes-
#python 2.7
import socket, thread,time
import psycopg2
import sys

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8091            # Porta que o Servidor esta
nmeter = sys.argv[1]

def splitFrame(frame):
    """
    Função para separar os dados do Frame Recebido
    """
    split = frame.split(";")
    #print split
    id_medidor =  split[0]#
    leitura =  split[1]
    #ts_medidor = split[2]
    assinatura_str_tupla = split[2]
    assinatura_str = assinatura_str_tupla[1:len(assinatura_str_tupla)-2]
    assinatura_long = long(assinatura_str)
    assinatura_long_tupla = (assinatura_long,)
    tempo = split[3] 
    #print tempo
    return (id_medidor,leitura,assinatura_long_tupla,tempo)


def saveDb(id_medidor,fatura,signature,conferir):
    con = psycopg2.connect(host='192.168.122.232', port='5432', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_micro')
    bd=con.cursor()
    sql="INSERT INTO faturas (id_medidor, fatura,signature,conferencia) VALUES('%s','%s','%s','%s')"%(id_medidor,fatura,signature,conferir)
    #sql = "INSERT INTO tempo (n_meter,tempo)VALUES('%s','%s')"%(n_meter,dtime))
    #sql="INSERT INTO tempo (n_meter,naturetempo)VALUES('%s','%s')"%(n_meter,dtime))
    bd.execute(sql)
    con.commit()
    con.close()

def saveTime(n_meter, dtime):
    con = psycopg2.connect(host='192.168.122.232', port='5432', user='inmetro', password='lsdinmetrolsdlsd',dbname='bd_micro')
    bd=con.cursor()
    sql="INSERT INTO tempo_agrega (n_meter,tempo) VALUES('%s','%s')"%(n_meter,dtime)
    #sql = "INSERT INTO tempo (n_meter,tempo)VALUES('%s','%s')"%(n_meter,dtime))
    #sql="INSERT INTO tempo (n_meter,tempo)VALUES('%s','%s')"%(n_meter,dtime))
    bd.execute(sql)
    con.commit()
    con.close()
    


def conectado(con, cliente):
    #print 'Conectado por', cliente
    #print "RECEBER PACOTE OK""""
    while True:
        msg = con.recv(819200)
        if not msg: break
        con.close()
        #print msg
        id_medidor,op,assinatura,tempo = splitFrame(msg)
        tempo_execucao = (time.time() - float(tempo))
        saveDb(id_medidor,op,assinatura,"ok")
        saveTime(str(nmeter),tempo_execucao)        
        thread.exit()
        



tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(-1)

print "RECEBER PACOTE OK"

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))
tcp.close()
