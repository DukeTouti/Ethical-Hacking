#!/bin/bash

# ==============================
# Script avancé de reconnaissance
# Auteur : PR Anass Sebbar
# ==============================

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

DOMAIN="$1"
RESULT_DIR="${DOMAIN}_results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULT_DIR"
cd "$RESULT_DIR" || exit 1

# Vérification des outils requis
for tool in dnsenum sublist3r nmap nikto whois dig traceroute curl; do
    if ! command -v $tool &>/dev/null; then
        echo "[!] Outil manquant : $tool. Installez-le svp."
        exit 1
    fi
done

echo "[+] Début de l'audit sur $DOMAIN"
echo "[!] Résultats dans le dossier : $RESULT_DIR"

#### 1. WHOIS Lookup (propriétaire du domaine)
echo "[+] WHOIS Lookup"
whois "$DOMAIN" > whois.txt

#### 2. Résolution IP et géolocalisation
echo "[+] IP Geolocation"
IP=$(dig +short "$DOMAIN" | tail -n1)
echo "IP trouvée: $IP" > ip_found.txt
curl -s "https://ipinfo.io/$IP" > ip_geolocation.txt

#### 3. Énumération DNS
#echo "[+] DNSENUM"
#dnsenum "$DOMAIN" > dnsenum_result.txt

#### 4. Extraction DNS avancée
echo "[+] Extraction types DNS"
dig "$DOMAIN" ANY > dns_any.txt
dig "$DOMAIN" MX > dns_mx.txt
dig "$DOMAIN" TXT > dns_txt.txt
dig "$DOMAIN" SOA > dns_soa.txt

#### 5. Recherche de sous-domaines
echo "[+] Subdomain enumeration"
sublist3r -d "$DOMAIN" -o sublist3r_result.txt

#### 6. Scan rapide des ports (TCP)
echo "[+] TCP port scan"
nmap -Pn -F "$DOMAIN" -oN nmap_tcp.txt

#### 7. Scan UDP des ports principaux
echo "[+] UDP port scan"
nmap -sU "$DOMAIN" -oN nmap_udp.txt

#### 8. Scan du serveur web pour failles classiques
echo "[+] Nikto web server scan"
nikto -h "$DOMAIN" -output nikto.txt

#### 9. Traceroute réseau
echo "[+] Traceroute"
traceroute "$DOMAIN" > traceroute.txt

#### 10. Recherche de répertoires/fichiers cachés (gobuster si présent)
if command -v gobuster &>/dev/null; then
    echo "[+] Directory scan (gobuster)"
    gobuster dir -u "http://$DOMAIN" -w /usr/share/wordlists/dirb/common.txt -o gobuster.txt
fi

#### 11. Détection CMS (si whatweb présent)
if command -v whatweb &>/dev/null; then
    echo "[+] CMS detection (whatweb)"
    whatweb "$DOMAIN" > cms.txt
fi

#### 12. Dorks Google pour la recherche d'informations publiques
echo "[+] Google Dorks (requête à utiliser manuellement)"
echo "site:$DOMAIN filetype:pdf" > google_dork.txt

echo "[+] Audit terminé ! Consultez tous les résultats dans $RESULT_DIR"
