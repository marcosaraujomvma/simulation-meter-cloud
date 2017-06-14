# -*- coding: utf-8 -*-
#Cliente socket enviando mensagem de um numero aleatorio
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, ssl, hashlib, time

CERT="48a0276e012bbb6754eb4fdaea1de5f4"
sock = socket.socket()
sock.settimeout(2)
sock.connect(('localhost', 8081))
conn = ssl.wrap_socket(sock)

id = input("qual é id do medidor?")

if hashlib.md5(conn.getpeercert(True)).hexdigest() != CERT:
    conn.close()
    print 'CERT diferente do esperado, tentando me hackearrrrrrr'
else:
    print 'Conectado!'
    for i in range(300):
        time.sleep(.3)
        ts = time.time()
        msg = ("%s;%s;%s"%(id,str(i),str(ts)))
        print("Pacote:",msg," Enviado!")
        conn.write(msg)
    print 'enviado'
    conn.close()