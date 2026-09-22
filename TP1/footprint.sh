#!/bin/bash

# Check if target domain is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <target-domain>"
    exit 1
fi

DOMAIN=$1

echo "[*] Creating directory for target: $DOMAIN"
mkdir -p "$DOMAIN"

echo "[*] Running DNS Analysis with dnsenum..."
dnsenum --nocolor "$DOMAIN" > "$DOMAIN/dnsenum_result.txt" 2>&1

echo "[*] Searching for subdomains with Sublist3r..."
sublist3r -d "$DOMAIN" -o "$DOMAIN/sublist3r_result.txt"

echo "[*] Running quick Nmap scan..."
nmap -T4 -F "$DOMAIN" > "$DOMAIN/nmap_result.txt"

echo "[*] Running Nikto web server scan..."
nikto -h "$DOMAIN" > "$DOMAIN/nikto_result.txt" 2>&1

echo "[*] Running Whois lookup (Additional tool)..."
whois "$DOMAIN" > "$DOMAIN/whois_result.txt"

echo "[+] Footprinting completed successfully! All results saved in directory: ./$DOMAIN/"
