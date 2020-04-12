import subprocess
import os
import sys
import socket
import socketserver
import time
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QPushButton,QInputDialog,QListWidgetItem,QFileDialog
from PyQt5.QtCore import pyqtSignal, QTimer, Qt,QDir
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, \
    QApplication, QStyle, QListWidget, QStyleOptionButton, QListWidgetItem
import GUI

import signal



#Mensajes 0 ENVIADOS ; 1 RECIVIDOS
#PAR [TIPO,MENSAJE]
Chats = {}
Canales = {}
Nicks = {}
socket_servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP_servidor = ""
Puerto = sys.argv[1]
IP_LOCAL = ""
IP_activas = []
MI_NICKNAME = sys.argv[2]
Error = 0


def obtener_IPs():
    global IP_LOCAL
    global MASCARA
    mask = os.popen('ifconfig|grep "inet"').read()
    datos = mask.split('\n')[2].strip().split(" ")
    IP_LOCAL = datos[1]
    MASCARA = datos[4]
    print("IP_L:{}, mask={}".format(IP_LOCAL,MASCARA))
    p_IP = IP_LOCAL.split(".")
    ip = p_IP[0]+"."+p_IP[1]+"."+p_IP[2]+"."
    Hilos = [None] * 32
    i = 1
    for j in range(0,32):
        if(j == 31):
            Hilos[j] = Thread(target=checar_IP,args=(ip,i,i+5),daemon=True)
            i +=5
        else:
            Hilos[j] = Thread(target=checar_IP,args=(ip,i,i+8),daemon=True)
            i +=8
    for i in range(len(Hilos)):
            Hilos[i].start()
    for i in range(len(Hilos)):
            Hilos[i].join()

    IP_activas.remove(IP_LOCAL)
        

def checar_IP(*args,**kwargs):
    global IP_activas
    for i in range(args[1],args[2]+1):
        IP = args[0]+str(i)
        #print(IP)
        ping = os.popen("ping "+IP+" -c 1 -w 5 -q").readlines()
        if(len(ping)>2):
            #print ( ping[3])
            if (ping[3].find("errors") == -1):
                IP_activas.append(IP)



def Cliente(*args,**kwargs):#*args= [IP,Puerto]
    global Error
    try:
        global Puerto
        global Canales
        global Chats
        conector = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        conector.connect((args[0],int(Puerto)))

        mensaje = "0".encode()
        conector.sendall(mensaje)

        nickname = conector.recv(1024)
        print(nickname.decode())
        Nicks[args[0]]=nickname.decode()
        
        if conector.recv(1024).decode() == "0":
            mensaje = MI_NICKNAME.encode()
            conector.sendall(mensaje)
        time.sleep(0.5)
        mensaje = args[1].encode()
        conector.sendall(mensaje)

        Canales[(args[0],Puerto)]=conector
        Chats[(args[0],Puerto)] = []
        Chats[(args[0],Puerto)].append((0,mensaje.decode()))
        if(gui.chat_activo == args[0]):
            try:
                gui.ui.Qlist_chat.addItem("\t\t\t"+mensaje.decode())
            except :
                pass
        reciviendo = Thread(target=Recibiendo,args=(conector,(args[0],Puerto),Chats))
        reciviendo.start()
    except :
        print("Error creando conexion con"+args[0])
        Error = -1
    
   
            
def Servidor(*args,**kwargs):
    global IP_servidor
    global Puerto
    try:
        socket_servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_servidor.bind((IP_servidor,int(Puerto)))
        print("Publicado en {} {}".format(IP_servidor,Puerto))
        socket_servidor.listen(40)
    except :
        print("Error al crear el servidor")
        sys.exit()
    
    Hilos = [None]*40
    i = 0
    while(1):
        canal,info = socket_servidor.accept()
        #Canales[info[0]]=canal
        #Chats[info[0]]=[]

        Canales[info]=canal
        Chats[info]=[]

        canal.setblocking(True)
        Hilos[i] = Thread(target=comunicacion,args=(canal,info,Canales,Chats))
        Hilos[i].start()
        i +=1
        

def comunicacion(*args,**kwargs):# Si dato = 0 ->Nickname, 1->archivo, 
    canal = args[0]
    info = args[1]
    print("Conectado con: {}".format(info))

    data = canal.recv(1024)
    if data.decode() == "0":
        mensaje = MI_NICKNAME.encode()
        canal.sendall(mensaje)
    time.sleep(0.5)
    mensaje = "0".encode()
    canal.sendall(mensaje)

    canal.setblocking(True)
    nickname2 = canal.recv(1024)
    Nicks[info[0]] = nickname2.decode()
    print(nickname2.decode())

    reciviendo = Thread(target=Recibiendo,args=(canal,info,args[3]))
    reciviendo.start()

def Recibiendo(*args,**kwargs):
    while True:
        try:
            datos = args[0].recv(1024).decode()
            #print("R: {}".format(datos))
            if(datos == "1"):
                print("Recibiendo archivos")
                datos = args[0].recv(1024).decode()
                os.popen("mkdir "+args[1][0])
                time.sleep(0.5)
                archivo_recv = open("./"+args[1][0]+"/"+datos,"bw")
                print("./"+args[1][0]+"/"+datos)

                args[2][args[1]].append((1,"Archivo: '{}'".format(datos)))
                if(gui.chat_activo == args[1][0]):
                    try:
                        gui.ui.Qlist_chat.addItem("Archivo: '{}'".format(datos))
                    except:
                        pass


                while(True):
                    print("recibiendo las partes del archivo")
                    data_archivo = args[0].recv(1024)
                    if(datos == ""):
                        Canales[args[1]].close()
                        print("Error al recivir")
                        del Canales[args[1]]
                        break
                    try:
                        if data_archivo.decode() == "9": # caracter final de archivo
                            if(gui.chat_activo == args[1][0]):
                                try:
                                    gui.ui.Qlist_chat.addItem("archivo recibido")
                                except:
                                    pass
                            print("Archivo terminado")
                            archivo_recv.close()
                            break
                        else:
                            print("escribiendo")
                            archivo_recv.write(data_archivo)
                    except :
                        print("escribiendo")
                        archivo_recv.write(data_archivo)
            elif(datos == ""):
                Canales[args[1]].close()
                print("Error al recivir")
                del Canales[args[1]]
                break
                #del Canales[args[1]]
                #print(Canales)
                
            else:
                args[2][args[1]].append((1,datos))
                if(gui.chat_activo == args[1][0]):
                    try:
                        gui.ui.Qlist_chat.addItem(datos)
                    except :
                        pass
        except :
            print("Error al recivir")
            del Canales[args[1]]
            #print(Canales)
            break
        


def enviar_mensaje(IP_a_enviar, msj):
    global Canales
    global Error
    Canal_para_enviar = None
    for info_canales in Canales.keys():
        if info_canales[0] == IP_a_enviar:
            Canal_para_enviar= Canales[info_canales]
            Chats[info_canales].append((0,msj))
            if(gui.chat_activo == IP_a_enviar):
                try:
                    gui.ui.Qlist_chat.addItem("\t\t\t"+msj)
                except:
                    pass
    if Canal_para_enviar == None:
        clint = Thread(target=Cliente,args=(IP_a_enviar,msj))
        clint.start()
        time.sleep(1)

        if(Error == -1):
            Error = 0
            return -1
    else:
        Canal_para_enviar.sendall(msj.encode())


def enviar_achivo(IP_a_enviar, path):
    global Canales
    Canal_para_enviar = None
    for info_canales in Canales.keys():
        if info_canales[0] == IP_a_enviar:
            Canal_para_enviar= Canales[info_canales]
            Chats[info_canales].append((0,"Archivo"+path))
            Chats[info_canales].append((0,"Enviando...."))
            if(gui.chat_activo == IP_a_enviar):
                print("Canal para archivo encontrado")
                try:
                    gui.ui.Qlist_chat.addItem("\t\t\t"+"Archivo"+path)
                    gui.ui.Qlist_chat.addItem("\t\t\tEnviando....")
                except:
                    pass

            break
    if Canal_para_enviar == None:
        print("Primero entable comunicacion")
    else: 
        Canal_para_enviar.send("1".encode())
        patth = path.split("/")
        nombre_archivo = patth[-1]
        print(nombre_archivo)
        Canal_para_enviar.send(nombre_archivo.encode())
        time.sleep(0.5)
        print("Canal listo para enviar archivo")
        archivo = open(path,"br")
        while True:
            
            contenido = archivo.read(1024)
            while contenido:
                print("Enviando")
                Canal_para_enviar.send(contenido)
                contenido = archivo.read(1024)
            break
        try:
            time.sleep(0.5)
            Canal_para_enviar.sendall("9".encode())
            archivo.close()
        except:
            pass
            
        Chats[info_canales].append((0,"Enviado..."))
        if(gui.chat_activo == IP_a_enviar):
            try:
                gui.ui.Qlist_chat.addItem("\t\t\t"+"Enviado...")
            except:
                pass
        

def obtener_chat(IP_del_canal):
    global Chats
    global Nicks
    global Canales
    Chat_buscado = None
    for info_chats in Chats.keys():
        if info_chats[0] == IP_del_canal:
            Chat_buscado= Chats[info_chats]
            
    if Chat_buscado != None:
        return Chat_buscado
    else:
        #print("Iniciando chat......perron")
        errorcito = enviar_mensaje(IP_del_canal,"-")
        #print ("errorcito es {}".format(errorcito))
        if( errorcito== -1):
            return "No activo"
        return Chat_buscado
     
class Inter_pra3(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Inter_pra3, self).__init__(parent)
        self.ui = GUI.Ui_MainWindow()
        self.chat_activo=""
        self.ui.setupUi(self)
        self.ui.Qlist_usuarios.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOn)
        self.ui.Qlist_chat.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOn)
        self.ui.Qlist_chat.setUpdatesEnabled( True)
        self.ui.Qlist_usuarios.setUpdatesEnabled(True)
        self.ui.act_usuarios.clicked.connect(self.actu_usuarios)
        self.ui.Qlist_usuarios.itemSelectionChanged.connect(self.cargar_chat)
        self.ui.boton_enviar_mensaje.clicked.connect(self.send_meeess)
        self.ui.boton_enviar_archivo.clicked.connect(self.send_filee)


    def send_filee(self):
        file_to_send,_ =  QFileDialog.getOpenFileName(self,"Seleccione el archivo",QDir.homePath(),"All Files (*);;Text Files (*.txt)")
        if(file_to_send != ""):
            enviar_achivo(self.chat_activo,file_to_send)
        
    def send_meeess(self):
        if( self.ui.Mensaje_a_enviar.text() != ""):
            mensage = self.ui.Mensaje_a_enviar.text()
            #print(mensage)
            enviar_mensaje(self.chat_activo,mensage)
            self.ui.Mensaje_a_enviar.setText("")
            self.ui.Mensaje_a_enviar.setFocus()
        else:
            pass
    def actu_usuarios(self):
        global IP_activas 
        IP_activas = []
        self.ui.Qlist_usuarios.clear()
        obtener_IPs()
        print("Limpia")
        for i in IP_activas:
            self.ui.Qlist_usuarios.addItem(i)
        
        
    def cargar_chat(self):
        #print("enfrando en funcion cargar char")
        global Chats
        
        if(self.chat_activo != IP_activas[self.ui.Qlist_usuarios.currentRow()]):
            #print("\t\tAdios")
            self.chat_activo = IP_activas[self.ui.Qlist_usuarios.currentRow()]
            #self.ui.Qlist_usuarios.NoSelection()
            #self.uni.Qlist_usuarios
            print(self.chat_activo)
            chat_IP = obtener_chat(self.chat_activo)

            if chat_IP == None:##canal activo pero vacio
                print("conecion nueva")
                chat_IP = []
                self.ui.Qlist_chat.clear()
                for i in chat_IP: #0 Enviado,1 Recivido
                    if(i[0] == 0):   
                        self.ui.Qlist_chat.addItem("\t\t\t"+i[1])
                    else:
                        self.ui.Qlist_chat.addItem(i[1])
                try:
                    self.ui.label_3.setText("Chat con "+Nicks[self.chat_activo])
                    print(Nicks[self.chat_activo])
                except :
                    self.ui.label_3.setText("Chat")
                self.ui.Qlist_usuarios.clearSelection()
                
            elif (chat_IP == "No activo"):#no se pudo crear coneccion
                print("No se puede conectar")
                self.ui.label_3.setText("Chat")
                self.ui.Qlist_chat.clear()
                self.ui.Qlist_usuarios.clearSelection()
            else:
                self.ui.Qlist_chat.clear()
                for i in chat_IP: #0 Enviado,1 Recivido
                    if(i[0] == 0):   
                        self.ui.Qlist_chat.addItem("\t\t\t"+i[1])
                    else:
                        self.ui.Qlist_chat.addItem(i[1])

                self.ui.Qlist_usuarios.clearSelection()
                self.ui.label_3.setText("Chat con "+Nicks[self.chat_activo])
                print(Nicks[self.chat_activo])
                

        else:
            self.ui.Qlist_usuarios.clearSelection()
def informa():
    while True:
        print(Chats,"\n")
        print(Canales,"\n")
        print(Nicks,"\n")
        time.sleep(2)
        
app = QApplication(sys.argv)
gui = Inter_pra3()
def main():
    #infooo = Thread(target=informa)
    #infooo.start()
    Servidor_H = Thread(target=Servidor,args=(Canales,Chats))
    Servidor_H.start()
    
    gui.ui.Qlist_usuarios.updatesEnabled()
    gui.ui.Qlist_chat.updatesEnabled()
    
    gui.show()
    sys.exit(app.exec_())

def handler(signum, frame):
    for Canales_res in Canales.keys():

        Canales[Canales_res].close()
    print("Canales cerrados")
    socket_servidor.close()
    sys.exit()

signal.signal(signal.SIGTSTP, handler)
            
if __name__ == '__main__':
    gui.actu_usuarios()
    IP_servidor = IP_LOCAL
    main()

#Cliente(IP_servidor,Puerto)
#obtener_IPs()
#checar_IP("192.168.0.253")
#print(IP_activas)
#Servidor_H = Thread(target=Servidor,args=(Canales,Chats))
#Servidor_H.start()


    


