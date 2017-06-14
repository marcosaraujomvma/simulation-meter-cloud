#Modulo de Conferencia do INMETRO
# -*- coding: utf-8 -*-
import audit
import hashlib

lista_hash_inmetro_id = []
rastro_id = []

lista_hash_inmetro_leitura = []
rastro_leitura = []

rastro_ts = []
inmetro_ts = []

hashconf = ""


def criarHASH(texto):

    hash = hashlib.sha256()
    hash.update(texto)
    return (hash.hexdigest())

def conferirInmetro(id_medidor,ts_inicial,ts_final,hash_rastro):
    hashconf = ""

    lista_hash_inmetro_id = []
    rastro_id = []

    lista_hash_inmetro_leitura = []
    rastro_leitura = []
    inmetro_leitura = []

    rastro_ts = []
    inmetro_ts = [] 

    inmetro_id,inmetro_leitura,inmetro_ts = audit.pegaBancoInmetro(id_medidor,ts_inicial,ts_final)#recupera do banco do inmetro

    hs_id_medidor = criarHASH(id_medidor)#cria o hash do id do medidor

    #rastro_id,rastro_leitura,rastro_ts = audit.pegaBancoRastro(str(hs_id_medidor),ts_inicial,ts_final)#recupera do banco do rastro

    for i in range(len(inmetro_id)):
        hashconf = hashconf + criarHASH(inmetro_leitura[i]+inmetro_ts[i])
        #print hashconf
        #hash_inmetro_id = criarHASH(inmetro_id[i])
        #hash_inmetro_leitura = criarHASH(inmetro_leitura[i])

        #lista_hash_inmetro_id.append(hash_inmetro_id)
        #lista_hash_inmetro_leitura.append(hash_inmetro_leitura)
    #print hash_rastro,'\n'
    #print hashconf
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

    

    """
    x = lista_hash_inmetro_id == rastro_id
    y = lista_hash_inmetro_leitura == rastro_leitura
    z = rastro_ts == inmetro_ts

    if x == True:
        print "RASTROS DO ID CORRETOS"
    else:
        print "FRAUDE NOS DADOS DO ID!!!"

    if y == True:
        print "RASTROS DAS LEITURAS CORRETOS"
    else:
        print "FRAUDE NOS DADOS DA LEITURA!!!"

    if z == True:
        print "RASTROS DO TS CORRETOS"
    else:
        print "FRAUDE NOS DADOS DO TS!!!"

    if x == y == z:
        return True
    else:
        return False

    """

    
    
"""

    if lista_hash_inmetro_id == rastro_id:
        print ("RASTRO DO %s CONFERIDOS"%(id_medidor)
        #lista_hash_inmetro_id = []
        #rastro_id = []

    #if (lista_hash_inmetro_leitura == rastro_leitura):
        #print ("RASTRO DA LEITURA CONFERIDOS")
        #lista_hash_inmetro_leitura = []
        #rastro_leitura = []
    if rastro_ts == inmetro_ts:
        print("RASTRO DOS TIME CONFERIDOS")
        #rastro_ts = []
        #inmetro_ts = []
"""
