#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  teste_01.py
#  
#  Copyright 2016 Marcos Vinicius Monteiro Araújo <marcos@badbook>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import socket

def main(args):
	print "hello world"
	
	HOST = '127.0.0.1'     # Endereco IP do Servidor
	PORT = 5000            # Porta que o Servidor receber
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #conexão tcp
	dest = (HOST, PORT) 
	tcp.connect(dest)
	print 'Para sair use CTRL+X\n'
	msg = raw_input()
	while msg <> '\x18':
		tcp.send (msg)
		msg = raw_input()
	tcp.close()

	
	
    #return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
