from argparse import ArgumentParser
import sys
import socket
import os

parser = ArgumentParser(description='Servidor Broadcast')
parser.add_argument('Puerto', help='El puerto de salida', type=int)
args = parser.parse_args()
puerto = args.Puerto

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 

client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(('', puerto))

Imagen = {}
cad = "Imagen "

os.popen("mkdir Imagenes_recividas")
imagenes_llegadas={}
while True:
    data, addr = client.recvfrom(1465)
    num_paquete = int(data[0:3].decode())
    num_imagen = int(data[4:5].decode())
    nombre_archivo = data[6:15].decode()
    contenido = data[15:]
    if(num_paquete == 0):
        if( (cad + str(num_imagen)) not in Imagen.keys()): #la primera vez que llega la imagen
            num_imagen_aux = num_imagen
            Imagen[cad + str(num_imagen)]=1
            Imagen_recv = open("./Imagenes_recividas/"+nombre_archivo,"bw")
            Imagen_recv.write(contenido)
            while num_imagen_aux == num_imagen:
                data, addr = client.recvfrom(1465)
                num_paquete = int(data[0:3].decode())
                num_imagen = int(data[4:5].decode())
                nombre_archivo = data[6:15].decode()
                contenido = data[15:]
                if(num_imagen_aux == num_imagen):
                    Imagen_recv.write(contenido)
            Imagen_recv.close()
        else:
            pass
    else:
        pass

    if (len(Imagen.keys()) == 5):
        break
