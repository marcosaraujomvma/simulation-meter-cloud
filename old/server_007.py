#Servidor
# -*- coding: utf-8 -*-
import audit
import socket
import thread,time
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import base64
from Crypto.Util.randpool import RandomPool
import psycopg2
import hashlib
import auditinmetro

BLOCK_SIZE=32


HOST = ''              # Endereco IP do Servidor
PORT = 6000           # Porta que o Servidor esta
"""
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
"""
"""
def operacao(id_medidor,leitura):
    global id_c +=leitura
""" 
medidor01 = 0
medidor02 = 0
medidor03 = 0
lista =[]
lista_hash_inmetro_id = []
lista_hash_inmetro_leitura = []
cont01 = 0
cont02 = 0
cont03 = 0
contmes = 0
ts_inicial01 = ""
ts_inicial02 = ""
ts_inicial03 = ""
ts_final01 =""
ts_final02 =""
ts_final03 ="" 
fat01 = ""
fat02 = ""
fat03 = ""
"""
lista_id_medidor = []
lista_leitura = []
lista_ts_medidor = []
"""
#ts_final = ""
def encrypt(message, passphrase):
    """
    codifica a mensagem com AES
    message = recebe a mensagem em string
    passphase = recebe a palavra para chavem
    retorna a mensagem codificada
    
    """
    h = SHA256.new()
    h.update(passphrase)
    key = h.digest()[0:16]
    # passphrase MUST be 16, 24 or 32 bytes long, how can I do that ?
    IV = Random.new().read(16)
    aes = AES.new(key, AES.MODE_CFB, IV)
    criptograma = IV + aes.encrypt(message)
    #return base64.b64encode(aes.encrypt(message))
    return criptograma


def decrypt(encrypted, passphrase):

    """
    descodifica a mensagem com AES
    message = recebe a mensagem em string
    passphase = recebe a palavra para chavem
    retorna a mensagem codificada
    
    """
    
    h = SHA256.new()
    h.update(passphrase)
    key = h.digest()[0:16]
    #IV = Random.new().read(16)
    #aes = AES.new(key, AES.MODE_CFB, IV)
    #deco = aes.decrypt(base64.b64decode(encrypted))
    #return aes.decrypt(base64.b64decode(encrypted))
    cipher = AES.new(key,AES.MODE_CFB,encrypted[0:16])
    recup = cipher.decrypt(encrypted[16:])
    return recup

def geraChave():
    pool = RandomPool(1024)
    pool.stir()
    randfunc = pool.get_bytes
    key= RSA.generate(1024, randfunc)
    return key
 
def gravaArquivo(id_gravar,msg,pasta):
    
    nome_arquivo = "%s/%s.txt"%(pasta,id_gravar)
    arq = open(nome_arquivo,'r')
    arquivo = arq.readlines()
    arquivo.append(msg)
    #lista.append(msg)
    arq = open(nome_arquivo,'w') 
    arq.writelines(arquivo)
    arq.close

def gravaBancoDadosInmetro(id_medidor,leitura,ts,assinatura,n,e):
    con = psycopg2.connect(host='192.168.122.232', user='postgres', password='postgres',dbname='inmetrobd')

    bd = con.cursor()

    sql = "INSERT INTO logmedidores (id_medidor,leitura,ts_medidor,assinatura,n,e)VALUES ('%s','%s','%s','%s','%s','%s')"%(id_medidor,leitura,ts,assinatura,n,e)


    bd.execute(sql)

    con.commit()

    con.close()


def criarHASH(texto):

    hash = hashlib.sha256()
    hash.update(texto)  
    return (hash.hexdigest())

def gravaBancoRastro(id_medidor,leitura,ts_medidor):
    ####hash das entradas###
    
    id_medidor_hash = criarHASH(id_medidor)
    leitura_hash = criarHASH(leitura)
    #ts_medidor_hash = criarHASH(ts_medidor)
    con2 = psycopg2.connect(host='192.168.122.232', user='postgres', password='postgres', dbname = 'rastro')

    bd2 = con2.cursor()

    sql2 = "INSERT INTO rastros (id_medidor,leitura,ts_medidor)VALUES ('%s','%s','%s')"%(id_medidor_hash,leitura_hash,ts_medidor)
    print ("Rastro Gerado!")

    bd2.execute(sql2)

    con2.commit()

    con2.close()
                    

def gravaInmetroLog(id_medidor,leitura,ts):
       
    hash = SHA256.new(str(leitura)).digest()
    key = geraChave()
    signature = key.sign(hash,"")
    n, e, d = key.n, key.e, key.d #paranmetro para gerar a chave publica depois
    
    #msg_grava = "%s;%s;%s;%s\n"%(log,signature,n,e)
    gravaBancoDadosInmetro(id_medidor,leitura,ts,signature,n,e)
    
    #gravaBanco("INMETRO",msg_grava,"loginmetro")
    print "Log INMETRO Gravado!!!!\n++++++++++++++++++++++++++++++++"

#def receberBanco
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
   
def conectado(con, cliente):
        
    print 'Conectado por', cliente
    
    while True:
        msg = con.recv(102400)
	#con.close()
        if not msg: break
             
        deco = decrypt(msg,"medidor")#decodifica a mensagem 
    
        sp = deco.split(";")
        #print sp
        n = sp[0]
        e = sp[1]
        signature = sp[2]
        ts = sp[3]
        id_medidor = sp[4]
        leitura = sp[5]
       
        sign = signature[1:(len(signature)-2)]
        long_sign = long(sign)
        tuple_long_sign = (long_sign,)#tupla com um long dentro
        
        
        com = (long(n),long(e))#tupla com os parametros da chave publica
        pub_key = RSA.construct(com)#gera a chave publica 
        
        hash = SHA256.new(str(ts)).digest()#gera hash para comparar assinatura
        #sign = long(signature)
              
        z = pub_key.verify(hash,tuple_long_sign)# conferi a assinature e retorna Bolean
        
        if z == True:#compara
                        
            print("\n========Assinatura do Pacote OK!\n============================\n")
            print("Medidor %s, com Leitura %i e Time %s\n\n=======================\n"%(id_medidor,int(leitura),ts))
            
            #log = "%s;%s;%s"%(id_medidor,leitura,ts)
            gravaInmetroLog(id_medidor,int(leitura),ts)
           # gravaBancoDados()
            ###SGX###
            if int(id_medidor)==01:
                global medidor01
                global ts_inicial01
                medidor01 += int(leitura)
                gravaBancoRastro(id_medidor,leitura,ts)#gera rastro
                global cont01
                cont01 += 1
                print "CONTE AQUI",cont01
                if cont01 == 1:
                    ts_inicial01 = ts#ts inicial do mes
                if cont01 == 5:#GERA O MES
                    cont01 = 0#ZERO O CONTADOR DO NUMERO DE PACOTES PARA FECHAR UM MES
                    ts_final01 = ts#ts final do mes
                    print cont01
                    conf = auditinmetro.conferirInmetro(str(id_medidor),str(ts_inicial01),str(ts_final01))#Conferir
                    if conf == True:
                        fat01 = ("%s;%s;CORRETO PELO INMETRO\n"%(id_medidor,medidor01))
                        gravaArquivo("01",fat01,"faturas")
                    else:
                        fat01 = ("%s;%s;INCORRETO PELO INMETRO, FRAUDE\n"%(id_medidor,medidor01))
                        gravaArquivo("01",fat01,"faturas")
                    medidor01 = 0#zero a fatura do mes
                                
            elif float(id_medidor)==02:

                global medidor02
                global ts_inicial02
                medidor02 += int(leitura)
                gravaBancoRastro(id_medidor,leitura,ts)#gera rastro
                global cont02
                cont02 += 1
                print "CONTE AQUI",cont02
                if cont02 == 1:
                    ts_inicial02 = ts#ts inicial do mes
                if cont02 == 5:#GERA O MES
                    cont02 = 0#ZERO O CONTADOR DO NUMERO DE PACOTES PARA FECHAR UM MES
                    ts_final02 = ts#ts final do mes
                    print cont02
                    conf = auditinmetro.conferirInmetro(str(id_medidor),str(ts_inicial02),str(ts_final02))#Conferir
                    if conf == True:
                        fat02 = ("%s;%s;CORRETO PELO INMETRO\n"%(id_medidor,medidor02))
                        gravaArquivo("02",fat02,"faturas")
                    else:
                        fat02 = ("%s;%s;INCORRETO PELO INMETRO, FRAUDE\n"%(id_medidor,medidor02))
                        gravaArquivo("02",fat02,"faturas")
                    medidor02 = 0#zero a fatura do mes
                    
            elif float(id_medidor)==03:
                global medidor03
                global ts_inicial03
                medidor03 += int(leitura)
                gravaBancoRastro(id_medidor,leitura,ts)#gera rastro
                global cont03
                cont03 += 1
                print "CONTE AQUI",cont03
                if cont03 == 1:
                    ts_inicial03 = ts#ts inicial do mes
                if cont03 == 5:#GERA O MES
                    cont03 = 0#ZERO O CONTADOR DO NUMERO DE PACOTES PARA FECHAR UM MES
                    ts_final03 = ts#ts final do mes
                    print cont03
                    conf = auditinmetro.conferirInmetro(str(id_medidor),str(ts_inicial03),str(ts_final03))#Conferir
                    if conf == True:
                        fat03 = ("%s;%s;CORRETO PELO INMETRO\n"%(id_medidor,medidor03))
                        gravaArquivo("03",fat03,"faturas")
                    else:
                        fat03 = ("%s;%s;INCORRETO PELO INMETRO, FRAUDE\n"%(id_medidor,medidor03))
                        gravaArquivo("03",fat03,"faturas")
                    medidor03 = 0#zero a fatura do mes

            
            else:
                print("Medidor não cadastrado")
                con.close
            
        else:
            print("Pacote Corronpido!")
            con.close()
            thread.exit()
            
    ###FIM SGX###           

    print 'Finalizando conexao do cliente', cliente
    print "O valor total do Medidor 01 : ",medidor01
    print "O valor total do Medidor 02: ",medidor02
    print "O valor total do Medidor 03: ",medidor03
    con.close()
    thread.exit()


    #fim conectado
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)
print "Servidor OK! "

while True:
    con, cliente = tcp.accept()
    thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()
