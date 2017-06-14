# -*- coding: utf-8 -*-
#python 2.7
import socket
import thread
import psycopg2

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8089            # Porta que o Servidor esta


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


def gravaBancoDadosInmetro(id_medidor,leitura,ts,assinatura):

    con = psycopg2.connect(host='192.168.122.232', user='postgres', password='postgres',dbname='inmetrobd')

    bd = con.cursor()

    sql = "INSERT INTO logmedidores (id_medidor,leitura,ts_medidor,assinatura)VALUES ('%s','%s','%s','%s')"%(id_medidor,leitura,ts,str(assinatura))


    bd.execute(sql)

    con.commit()

    con.close()
    
    print "Dados Gravados No Banco do Inmetro"

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente
        print msg


        id_medidor,leitura,ts_medidor,assinatura = splitFrame(msg)
        

        gravaBancoDadosInmetro(id_medidor,leitura,ts_medidor,assinatura)
        
        

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