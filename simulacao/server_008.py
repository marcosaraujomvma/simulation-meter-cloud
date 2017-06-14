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
import hashlib, ssl
import auditinmetro


BLOCK_SIZE=32


HOST = ''              # Endereco IP do Servidor
PORT = 6001           # Porta que o Servidor esta

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
hash01 = ""
hash02 = ""
hash03 = ""


def num2msg(n):
 s = []
 while n > 0:
     s.insert(0, chr(n & 255))
     n >= 8
 return ''.join(s)


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
    IV = Random.new().read(16)
    aes = AES.new(key, AES.MODE_CFB, IV)
    criptograma = IV + aes.encrypt(message)
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
                

def gravaInmetroLog(id_medidor,leitura,ts):
       
    hash = SHA256.new(str(leitura)).digest()
    key = geraChave()
    signature = key.sign(hash,"")
    n, e, d = key.n, key.e, key.d #paranmetro para gerar a chave publica depois
        
    gravaBancoDadosInmetro(id_medidor,leitura,ts,signature,n,e)
    
    print "Log INMETRO Gravado!!!!\n++++++++++++++++++++++++++++++++"

def conectado(con, cliente):
    fpr = open("chaves/keypr.pem")
    sgx_key = RSA.importKey(fpr.read())

    fpu = open("chaves/medidor01_Publickey.pem")
    public_key = RSA.importKey(fpu.read())


    conn = ssl.wrap_socket(con, server_side=True, certfile='chaves/certificado-chave.pem', keyfile= 'chaves/certificado-chave.pem')#certificado
    conn.setblocking(0)    
    print 'Conectado por', cliente
    
    while True:
        buf = conn.read(1024)
	#con.close()
        if not msg: break

        #print msg
        tupla= (msg,)
        msg_decodificada = sgx_key.decrypt(tupla)
        print msg_decodificada
        #w = msg[2:len(msg)-3]
        #print w
        #print type(w)
        #z = bytes(w)
        #rint z
        #
        #print type(z)
        #tupla = (z,)
        #print tupla
        #long_msg = long(w)
        #print long_msg
        #print type(long_msg)
        #tupla = (long_msg,"senha")
        #print tupla
        #msg_decodificada = sgx_key.decrypt(tupla)
        #bina = msg

        #print msg
	#print type(msg)
	#y = (msg[1:len(msg)-3])
	#print y
	#w = long(y)
	#print w
	#zz = (w,)
	#print zz

	
        #y = (base64.b64decode(msg),)
        #print base64.b64decode(msg)
        #msg_decodificada = sgx_key.decrypt(zz)
        #print tupla
        #print msg_decodificada
        #kk = num2msg(msg_decodificada)
        
        #print kk
        
        """     
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
        """

        """
        if z == True:#compara
                        
            print("\n========Assinatura do Pacote OK!\n============================\n")
            print("Medidor %s, com Leitura %i e Time %s\n\n=======================\n"%(id_medidor,int(leitura),ts))
                        
            gravaInmetroLog(id_medidor,int(leitura),ts)
          
            ###SGX###
            if int(id_medidor)==01:
                global medidor01
                global ts_inicial01
                medidor01 += int(leitura)
                global cont01
                cont01 += 1
                global hash01
                hash01 = hash01 + criarHASH(leitura + ts)#gera chain hash
                if cont01 == 1:
                    ts_inicial01 = ts#ts inicial do mes
                if cont01 == 5:#GERA O MES
                    cont01 = 0#ZERO O CONTADOR DO NUMERO DE PACOTES PARA FECHAR UM MES
                    ts_final01 = ts#ts final do mes
                    print cont01
                    conf = auditinmetro.conferirInmetro(str(id_medidor),str(ts_inicial01),str(ts_final01),hash01)#Conferir
                    hash01 = ""
                    if conf == True:
                        print "FATURA FECHADA E CONFERIDA"
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
                
                global hash02
                hash02 = hash02 + criarHASH(leitura + ts)#gera chain hash
                global cont02
                cont02 += 1
                if cont02 == 1:
                    ts_inicial02 = ts#ts inicial do mes
                if cont02 == 5:#GERA O MES
                    cont02 = 0#ZERO O CONTADOR DO NUMERO DE PACOTES PARA FECHAR UM MES
                    ts_final02 = ts#ts final do mes
                    #print cont02
                    conf = auditinmetro.conferirInmetro(str(id_medidor),str(ts_inicial02),str(ts_final02),hash02)#Conferir
                    hash01 = ""
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
                #gravaBancoRastro(id_medidor,leitura,ts)#gera rastro
                global hash03
                hash03 = hash03 + criarHASH(leitura + ts)#gera chain hash
                global cont03
                cont03 += 1
                #print "CONTE AQUI",cont03
                if cont03 == 1:
                    ts_inicial03 = ts#ts inicial do mes
                if cont03 == 5:#GERA O MES
                    cont03 = 0#ZERO O CONTADOR DO NUMERO DE PACOTES PARA FECHAR UM MES
                    ts_final03 = ts#ts final do mes
                    #print cont03
                    conf = auditinmetro.conferirInmetro(str(id_medidor),str(ts_inicial03),str(ts_final03),hash03)#Conferir
                    hash03 = ""
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

    """
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
