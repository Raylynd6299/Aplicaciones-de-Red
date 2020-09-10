#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

void CreateSocketTCP (int *Socket) {
    *Socket = socket(AF_INET,SOCK_STREAM,0);
    if ( (*Socket) < 0){
        perror("Error al crear el Socket");
        exit(0);
    }
}
void ConnectionSpecs(struct sockaddr_in *ConnectionSpecs, short int Puerto, char * IP) {
    ConnectionSpecs->sin_family=AF_INET;
    ConnectionSpecs->sin_port=htons(Puerto);
    ConnectionSpecs->sin_addr.s_addr = inet_addr(IP);
}
short BuildConnection(int *Socket,struct sockaddr_in *ConnectionSpecs){
    if ( connect(*Socket,(struct sockaddr *)ConnectionSpecs,sizeof((*ConnectionSpecs))) == -1){
        perror("Error al crear la Coneccion a la red!");
        close(*Socket);
        exit(-1);
        return 0;
    }
    return 1;
}
int SendMessage(int *Socket, void *Message, int lenght,int flag){
    int retval=send(*Socket,Message,lenght,flag);//el numero de bits enviados o -1 si hay error
    if(retval == -1){
        perror("Error al enviar el Mensage");
        close(*Socket);
        exit(-1);
        return -1;
    }
    return retval;
}

void ReciveMessage(int *Socket,void *Buffer,int SizeBuffer,int flag){
    int RetVal = recv(*Socket,Buffer,SizeBuffer,flag);
    if (RetVal < 0) {
        perror("Error reciviendo el mensage");
        close(*Socket);
        exit(-1);
    }
    *(((char *)Buffer)+RetVal) = '\0';
}
void StandServer(int *Socket,struct sockaddr_in *ConnectionSpecs){
    if(bind(*Socket,(struct sockaddr *)ConnectionSpecs,sizeof(struct sockaddr_in)) < 0){
        perror("Error al levantar el Servidor");
        close(*Socket);
        exit(-1);
    }
}

void StayListen(int *Socket,int MaxLenghtList) {
    if ( listen(*Socket,MaxLenghtList) == -1 ){
        perror("Error al Configurar la lista de espera");
        close(*Socket);
        exit(-1);
    }
}
int NextConnection(int *Socket, struct sockaddr_in *InfoClienteConnection,int *tamcliente){
    int ConnectionPipe;
    if((ConnectionPipe = accept(*Socket,(struct sockaddr *)InfoClienteConnection,tamcliente))==-1){
        perror("Error obteniendo el Canal de Comunicacion");
        close(*Socket);
        exit(-1);
    }else{
        printf("Canal de Comunicacion obtenido Correctamente");
        //printf("Coneccion establecida con %s\n",inet_ntoa(cliente.sin_addr));
    }
    return ConnectionPipe;
}