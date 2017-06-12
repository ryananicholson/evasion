# -*- coding: utf-8 -*-
import socket
import sys

if (len(sys.argv) < 3):
	print >>sys.stderr, 'Need IP and port!'
	quit()
else:
	ip = sys.argv[1]
	port = int(sys.argv[2])

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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ip, port)
print >>sys.stderr, 'Connecting to %s, port %s' % server_address
sock.connect(server_address)

try:
	while True:
		cmd = raw_input('# ')
		cmd = cmd.strip()
		message = ''
		for i in cmd:
			tempint = shiftLeft(ord(i))
			message += chr(tempint)
		sock.sendall(message)
		data = sock.recv(2048)
		message = ''
		for i in data:
			tempint = shiftRight(ord(i))
			message += str(unichr(tempint))
		print message

finally:
	print >>sys.stderr, 'Closing socket'
	sock.close()
