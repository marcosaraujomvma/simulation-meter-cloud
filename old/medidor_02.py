# -*- coding: utf-8 -*-
#Cliente socket enviando mensagem de um numero aleatorio
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 2.7

import socket
import random
import time
import md5

def enviar(*msg):
    HOST = '127.0.0.1'     # Endereco IP do Servidor
    PORT = 5001            # Porta que o Servidor recebe
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #conexão tcp
    dest = (HOST, PORT) 
    tcp.connect(dest)
    msg = str(msg)
    tcp.send(msg)
"""
def leitura():
    ler = random.uniform(1,8)
    print ler
    return ler
"""

for i in range(30000):
	ts = time.time()
	leitura = random.uniform(1,8)
	print leitura
	enviar(leitura,ts)
	#msg = str(i)
	#tcp.send(msg)
	
	time.sleep(0.3)

#tcp.close

print "terminou de enviar"
