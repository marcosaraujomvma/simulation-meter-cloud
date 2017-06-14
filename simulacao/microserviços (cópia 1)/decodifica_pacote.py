import socket
import thread
from Crypto.PublicKey import RSA

HOST = 'localhost'              # Endereco IP do Servidor
PORT = 8086            # Porta que o Servidor esta

fprcl = open("chaves/cloudPrivate.pem")
keyprcl = RSA.importKey(fprcl.read())
print "LEU CHAVE PRIVADA 4096\n"

def enviaDados(msg):
    
    HOST = 'localhost'     # Endereco IP do Servidor
    PORT = 8087           # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    #print 'Para sair use CTRL+X\n'
    
    #while msg <> '\x18':
    tcp.send (msg)
        
    tcp.close()


def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente

        tupla = (msg,)
        #print tupla
        dec = keyprcl.decrypt(tupla)

        print "Mensagen Decodificada"
        print dec
        enviaDados(dec)

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