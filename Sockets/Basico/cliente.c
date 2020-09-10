#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "SocketTCP.h"

void main(int argc,char *argv[]){
    if (argc >=3){
        char *ip = argv[1];
        short int puerto = (short)atoi(argv[2]);

        int id_socket;
        struct sockaddr_in specs;

        char buffer[50];
        strcpy(buffer,"Hola mundo");
        int tam = strlen(buffer);

        CreateSocketTCP(&id_socket);
        
        ConnectionSpecs(&specs,puerto,ip);

        if (BuildConnection(&id_socket,&specs)){
            printf("Coneccion con la Red, Exitosa!!");
        }
        
        SendMessage(&id_socket,(void*)buffer,tam,0);

        printf("Mensaje enviado: '%s'",buffer);

        ReciveMessage(&id_socket,(void *)buffer,sizeof(buffer),0);
    
        printf("\nMensaje recibido del servidor %s",buffer);

        close (id_socket);
    }else{
        perror("Faltan los parametros, IP, Puerto");
    }
}