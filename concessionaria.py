import hashlib
h = hashlib.sha1()

h.update(b"m10")
h.update(b"t1")
#print (h.hexdigest())

h.update(h.digest())
h.update(b"m15")
h.update(b"t2")
#print (h.hexdigest())

h.update(h.digest())
h.update(b"m15")
h.update(b"t3")
#print (h.hexdigest())

h.update(h.digest())
h.update(b"m10")
h.update(b"t4")

print ("Hash de todos pacotes:")
print (h.hexdigest())

