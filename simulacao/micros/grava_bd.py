# -*- coding: utf-8 -*-
#python 2.7
import socket
import thread
import psycopg2

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8087            # Porta que o Servidor esta


def gravaBancoDadosInmetro(pkg):

    con = psycopg2.connect(host='192.168.122.232', user='postgres', password='postgres',dbname='bd')

    bd = con.cursor()

    sql = "INSERT INTO dadospkg (pkg)VALUES('%s')"%(pkg)
    print "\n",sql,"\n"
    print type(pkg),"\n"
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

        gravaBancoDadosInmetro(msg)
        #id_medidor,leitura,ts_medidor,assinatura = splitFrame(msg)
        

        #gravaBancoDadosInmetro(id_medidor,leitura,ts_medidor,assinatura)
        
        

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