from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256

# bytes que vamos cifrar
texto = b'conteudo a cifrar'

# definicao da password a partir da qual vamos criar uma chave
password = 'uma password qualquer'

# geracao da chave de 16bytes a partir da password
h = SHA256.new()
h.update(password)
key = h.digest()[0:16]

# geracao do vector de inicializacao de 16bytes
iv = Random.new().read(16) 

# criacao do criptograma (texto cifrado)
cipher = AES.new(key, AES.MODE_CFB, iv)
criptograma = iv + cipher.encrypt(texto)

# recuperacao do texto limpo, a partir do criptograma
cipher = AES.new(key, AES.MODE_CFB, criptograma[0:16])
texto_recuperado = cipher.decrypt(criptograma[16:])

print(texto_recuperado)
print(texto)