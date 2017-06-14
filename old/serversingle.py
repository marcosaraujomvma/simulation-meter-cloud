import socket

from Crypto.PublicKey import RSA
HOST = ''              # Endereco IP do Servidor
PORT = 5020            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
while True:
    con, cliente = tcp.accept()
    print 'Concetado por', cliente
    while True:
        msg = con.recv(1024)
        if not msg: break
        sp = msg.split(";")
        #print cliente, msg
        n = sp[0]
        e= sp[1]
        d = sp[2]
        print ("%s\n=========\n%s\n=========\n%s\n========"%(n,e,d))
        e2 = long(e)
        n2 = long(n)
        pub_key = RSA.construct((n2, e2))
        print pub_key
    print 'Finalizando conexao do cliente', cliente
    con.close()