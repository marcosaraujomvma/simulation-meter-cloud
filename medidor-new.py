import requests, hashlib, time, random, sys, OpenSSL
from OpenSSL import crypto
import base64
key_file = open("private.pem", "r")
key = key_file.read()
key_file.close()

pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)

chave = sys.argv[1]
auth = hashlib.sha256(chave.encode('utf-8')).hexdigest()

print ('auth medidor: ' + auth)

url = 'https://sc-gir.rhcloud.com/modulo_entrada'

	
while True:
	valor = random.uniform(2,4)
	valor_sign = OpenSSL.crypto.sign(pkey, valor, "sha256") 
	timestamp = time.time()
	timestamp_sign = OpenSSL.crypto.sign(pkey, timestamp, "sha256") 
	
	
	data =  {
		'valor': valor,
		'valor_sign': base64.b64encode(valor_sign),
		'timestamp': timestamp,
		'timestamp_sign': base64.b64encode(timestamp_sign),
		'auth': auth
	}
		
	r = requests.post(url, data)
	time.sleep(1)
	
	print (r.text)
