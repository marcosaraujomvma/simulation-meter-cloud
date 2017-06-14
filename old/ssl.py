#!/usr/bin/env python
# -*- coding: utf-8 -*-
from OpenSSL import crypto

# Lendo o arquivo pfx no formato pkcs12 como binario
pkcs12 = crypto.load_pkcs12(open('certi.pfx', 'rb').read(), 'passphrase')

# Retorna a string decodificado do certificado 
cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, pkcs12.get_certificate())

# Retorna a string decodificado da chave privada
key_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkcs12.get_privatekey())

# Gravando a string no dicso 
open('cert.pem', 'wb').write(cert_str)

# Gravando a string no dicso 
open('key.ptm', 'wb').write(key_str)
