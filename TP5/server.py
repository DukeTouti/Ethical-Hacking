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
