from argparse import ArgumentParser
import sys
import socket
import time
import os

parser = ArgumentParser(description='Servidor Broadcast')
parser.add_argument('Puerto', help='El puerto de salida', type=int)
args = parser.parse_args()
puerto = args.Puerto

#Variables globales
Imagenes = {}
#Configuracion del socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.settimeout(0.2)

def obtener_imagenes():
    Nombre_de_imagenes = os.popen("cd Imagenes_a_enviar;ls").read()
    Nombre_de_imagenes = Nombre_de_imagenes.split("\n")
    Nombre_de_imagenes.pop()
    #Agregandolos al dicc
    for Nombre  in Nombre_de_imagenes:
        sizefile = os.stat("./Imagenes_a_enviar/"+Nombre).st_size
        Imagenes[Nombre]=(Nombre,sizefile)
    #print(Imagenes)

def enviar_imagen(Datos_imagen,num):
    num_paquete = 0
    print("Listo para enviar Imagen "+str(num))
    archivo = open("./Imagenes_a_enviar/"+Datos_imagen[0],"br")
    while True:
        contenido = archivo.read(1450)
        paquete = "{0:3d} ".format(num_paquete).encode()+"{} ".format(num).encode()+Datos_imagen[0].encode()+" ".encode()+contenido 
        num_paquete +=1
        #print(len(paquete))    
        while contenido:
            print("Enviando imagen "+str(num)+" paquete: "+str(num_paquete))
            server.sendto(paquete, ("<broadcast>", puerto))
            contenido = archivo.read(1450)
            paquete = "{0:3d} ".format(num_paquete).encode()+"{} ".format(num).encode()+Datos_imagen[0].encode()+" ".encode()+contenido 
            num_paquete +=1 
        break
    archivo.close()


if __name__ == "__main__":
    obtener_imagenes()
    while True:
        num_imagen = 0
        for imagen_data in Imagenes.keys():
            #print(Imagenes[imagen_data])
            num_imagen += 1
            #print( num_imagen)
            enviar_imagen(Imagenes[imagen_data],num_imagen)
            time.sleep(1)
