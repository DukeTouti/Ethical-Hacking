#!/bin/bash

# Vérification de la présence du fichier proxy local
if [ ! -f "proxy.txt" ]; then
    echo "Erreur : Le fichier proxy.txt est introuvable !"
    exit 1
fi

read -p "Entrez l'IP cible (ex: 192.168.1.50) : " TARGET
echo "Choisissez le mode de scan :"
echo "1) Proxy Statique (sélection aléatoire depuis proxy.txt)"
echo "2) Proxy Dynamique (Tor - simulation locale)"
echo "3) Proxy Chain (Chaîne de plusieurs proxies aléatoires)"
read -p "Votre choix (1-3) : " CHOICE

# Sauvegarde de la config originale de proxychains
sudo cp /etc/proxychains4.conf /etc/proxychains4.conf.bak

# Nettoyage de la section [ProxyList] existante
sudo sed -i '/^\[ProxyList\]/,$!b;/^[^#]/d' /etc/proxychains4.conf

case $CHOICE in
    1)
        # Sélection aléatoire d'un proxy unique depuis le fichier
        PROXY=$(shuf -n 1 proxy.txt)
        echo "Proxy statique sélectionné aléatoirement : $PROXY"
        IFS=':' read -r p_ip p_port <<< "$PROXY"
        sudo bash -c "echo 'socks5 $p_ip $p_port' >> /etc/proxychains4.conf"
        ;;
    2)
        echo "Simulation du Proxy Dynamique (Tor / 127.0.0.1:9050)"
        sudo bash -c "echo 'socks5 127.0.0.1 9050' >> /etc/proxychains4.conf"
        ;;
    3)
        echo "Configuration d'une chaîne de proxies aléatoires..."
        PROXIES=$(shuf -n 3 proxy.txt)
        while IFS= read -r proxy; do
            IFS=':' read -r p_ip p_port <<< "$proxy"
            if [ -n "$p_ip" ] && [ -n "$p_port" ]; then
                echo "Ajout dans la chaîne : $p_ip:$p_port"
                sudo bash -c "echo 'socks5 $p_ip $p_port' >> /etc/proxychains4.conf"
            fi
        done <<< "$PROXIES"
        ;;
    *)
        echo "Choix invalide."
        sudo mv /etc/proxychains4.conf.bak /etc/proxychains4.conf
        exit 1
        ;;
esac

echo "Lancement du scan Nmap en TCP Connect (-sT) sur la cible $TARGET..."
# Exécution obligatoire en -sT car le proxying ne supporte pas les SYN scans
proxychains nmap -sT -Pn "$TARGET"

# Restauration automatique de la configuration d'origine
sudo mv /etc/proxychains4.conf.bak /etc/proxychains4.conf
echo "Configuration proxychains restaurée avec succès."
