#!/usr/bin/env python
import os
import telnetlib
from threading import Thread
from . import app
def obtener_ips_ruteo():

    """ En esta funcion se busca en la tabla de ruteo,
     todas las subredes enrutadas por la interfaz tap0 """

    #Obteniendo y limpiando las ip de las subredes 
    request = os.popen('route -n |grep "tap0" ').read()
    request = request.split("\n")
    #De cada linea de la salida obtengo la ip de la red 
    ips = [line.split(" ")[0] for line in request ]
    ips.pop()

    return ips

def obtener_ips_de_routers(ips):
    """Se modifican las ip de las sub redes, para obtener las de gateway,
    las cuales son colocadas en las interfaces del router """
    return [ip.replace("0","1") for ip in ips ]

def obtener_ip_host():
    """ Obtenemos la ip del host en la interfaz tap0, conectada a GNS3 """

    request = os.popen("ip a | grep 'inet' | grep 'tap0' ").read()
    ip_host = request.strip().split(" ")[1].replace("/24","")
    
    return ip_host

def obtener_backup(ip):
    """Funcion con la que se obtiene cada uno de los backups

    ip => es la ip de gateway de la subred.

    password => Es la contraseña para acceder a los routers por telnet,
                esta fue configurada por el administrador de la red.

    passwd_1 => Es la contraseña para acceder a la configuracion en el router

    add_host => Es la direccion del host donde se guardara la configuracion
     
    """

        
    password = "ray"
    passwd_2 = "pulido"
    addr_host = obtener_ip_host()
    
    #Creamos la coneccion Telnet
    tn = telnetlib.Telnet(ip)

    #LLevamos a cabo la comunicacion como si fuera en la tty o terminal 
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"enable\n")
    tn.read_until(b"Password: ")
    tn.write(passwd_2.encode('ascii') + b"\n")
    #Con este comando creamos una copy de la configuracion y la enviamos via tftp
    tn.write(b"copy running-config tftp: \n")
    #Despues no pide a que host y le mandamos la direccion
    tn.write(addr_host.encode('ascii') + b"\n")
    #le confirmamos el nombre por defecto con  un enter o \n
    tn.write(b"\n")
    #terminamos la coneccion
    tn.write(b"exit\n")
    #leemos todo para que se efectue las oberaciones y mostremos la salida
    print(tn.read_all().decode('ascii'))



def mover_backups():

    """ Esta funcion esta diseñada para mover los archivos de configuracion
    a la carpeta destino de backups 
     
    path_tftp => contiene el path o direccion donde se alojan los datos traidos por tftp

    path_backs => Es el path donde se guardara los backups
    """

    path_tftp = "/tftp/"
    path_backs = "/var/www/raypulido/app/Backups/"

    os.popen("mkdir "+path_backs).read()
    NameBackups = os.popen("cd " + path_tftp + " ; ls").read()
    NameBackups = NameBackups.strip().split("\n")

    #Este ciclo movera cada archivo de configuracion a su respectiva carpeta a la vez que crea estas
    for back in NameBackups:
        os.popen("mkdir " + path_backs + back)
        os.popen("sudo -S mv " + path_tftp + back + " " + path_backs + back)
    return NameBackups

def tftp():
    with app.app_context():
        ips = obtener_ips_ruteo()
        #print(ips)
        ips = obtener_ips_de_routers(ips)
        for ip in ips:
            obtener_backup(ip)
        backs = mover_backups()
def do_back():
    thread = Thread(target=tftp)
    thread.start()
    return thread


if __name__ == "__main__":
    tftp()


