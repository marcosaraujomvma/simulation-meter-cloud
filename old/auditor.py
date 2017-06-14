#!/usr/bin/env python
# -*- coding: utf-8 -*-

def abrirLog():
    log = open("loginmetro/INMETRO.txt","r")
    arq_log = log.readlines()
    return arq_log

def abrirRastro(rastro):
    
    arquivo = "rastros/0%s.txt"%(str(rastro))
    arq_rastro = open(arquivo,"r")
    arq_lista = arq_rastro.readlines() 
    return arq_lista            

log_inmetro = abrirLog()
rastro_medidor = abrirRastro(str(01))

mes = 1
lista = rastro_medidor[0:20]


    

