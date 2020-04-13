#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

void main(int argc,char *argv[]){
    if (argc >=3){
        short int puerto = (short)atoi(argv[2]);
        char *ip = argv[1];
        int id_socket;
        struct sockaddr_in servidor;
        char buffer[50];
        strcpy(buffer,"Hola mundo");
        int tam = strlen(buffer);

        id_socket = socket(AF_INET,SOCK_STREAM,0);
        if (id_socket < 0){
            perror("No se pudo abrir el socket");
            exit(0);
        }
        
        servidor.sin_family = AF_INET;
        servidor.sin_port = htons(puerto);
        servidor.sin_addr.s_addr = inet_addr(ip);

        if(connect(id_socket,(struct sockaddr *)&servidor,sizeof(struct sockaddr_in))==-1){
            perror("Error en el connect");
            close(id_socket);
            exit(-1);
        }
        
        
        if(send(id_socket,(void *)buffer,tam,0) == -1){//el numero de bits enviados o -1 si hay error
            perror("Error en el send,  al enviar el mensaje");
            close(id_socket);
            exit(-1);
        }

        printf("Mensaje enviado '%s'",buffer);

        tam = recv(id_socket,(void *)buffer,sizeof(buffer),0);
        if(tam<0){//el numero de bits recividos
            perror("Erros en la recepcion");
            close(id_socket);
            exit(-1);
        }
        buffer[tam]= '\0';
        printf("\nMensaje recibido del servido %s",buffer);

        close (id_socket);
    }else{
        perror("Faltan los parametros, IP, Puerto");
    }
}