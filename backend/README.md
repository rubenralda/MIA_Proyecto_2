# Comandos y paquetes utilizados

# Maquina virtual EC2
Se puede conectar a una instancia desde el navegador u otra forma
## En vm instalar python y herramientas necesarias
con root para que pueda crear los reportes:
sudo apt update
sudo apt install python3 python3-pip
sudo pip3 install flask
sudo pip3 install ply
sudo pip3 install graphviz
sudo apt install graphviz
sudo pip3 install flask-cors
### En vm instalar git
sudo apt install git

# descargar proyecto de git
git clone https://github.com/rubenralda/MIA_Proyecto_2.git

# ahora instalar nginx
sudo apt install nginx

# activar el servicio
sudo systemctl enable nginx
sudo systemctl start nginx

#ingresar archivo para exponer puerto
sudo vim /etc/nginx/sites-enabled/fasapi_nginx

server {
    listen 80;
    server_name 18.225.248.23;
    location / {
        proxy_pass http://127.0.0.1:4000;
    }
}

esc + :wq

# para verificar si se guardó el archivo
cat /etc/nginx/sites-enabled/fasapi_nginx

# ahora resetear el servidor de nginx
sudo service nginx restart

# Correr el proyecto:

sudo python3 main.py


Comandos no actualizados para uso de la API REST:

1. comando_cat
2. comando_edit
3. comando_execute
4. comando_remove
5. comando_rename
6. comando_unmount

y el comando_pause se paso al lado del fronted