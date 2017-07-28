from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Util.randpool import RandomPool
"""
rng = Random.new().read
RSAkey = RSA.generate(1024, rng)

"""
pool = RandomPool(1024)
pool.stir()
randfunc = pool.get_bytes
RSAkey= RSA.generate(1024, randfunc)

f = open("meter-private.pem","w+")
f.write(RSAkey.exportKey("PEM"))
f.close()
print "Gerou chave Privada"
f = open("meter-public","w+")
f.write(RSAkey.publickey().exportKey("PEM"))
f.close()
print "Gerou chave Publica"
