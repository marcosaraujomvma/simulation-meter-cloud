from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Util.randpool import RandomPool
"""
rng = Random.new().read
RSAkey = RSA.generate(1024, rng)

"""
pool = RandomPool(2048)
pool.stir()
randfunc = pool.get_bytes
RSAkey= RSA.generate(2048, randfunc)

f = open("cloudPrivate.pem","w+")
f.write(RSAkey.exportKey("PEM"))
f.close()
print "Gerou chave Privada"
f = open("cloudPublic.pem","w+")
f.write(RSAkey.publickey().exportKey("PEM"))
f.close()
print "Gerou chave Publica"
