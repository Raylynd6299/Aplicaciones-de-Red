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
        short int puerto = atoi(argv[2]);
        int id_socket;
        struct sockaddr_in specs;
        struct sockaddr_in cliente;//estructura a llenar por la funcion accept

        int tam_cliente;
        int canal ;
        char buffer[50];
        int tam ;

        CreateSocketTCP(&id_socket);
        
        ConnectionSpecs(&specs,puerto,ip);
        
        StandServer(&id_socket,&specs);

        StayListen(&id_socket,2);

        tam_cliente = sizeof(cliente);
        
        canal = NextConnection(&id_socket,&cliente,&tam_cliente);

        recv(&canal,(void *)buffer,sizeof(buffer),0);
        printf("Mensaje recibido del servido '%s'\n",buffer);

        strcpy(buffer,"Hola amigo");
        tam = strlen(buffer);

        SendMessage(&canal,(void *)buffer,tam,0);
        
        printf("Mensaje enviado '%s'\n",buffer);
    
        close (canal);
        close (id_socket);
    }else{
        perror("Faltan los parametros, IP, Puerto");
    }
    
}