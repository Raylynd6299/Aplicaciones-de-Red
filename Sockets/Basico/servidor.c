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
        int puerto = atoi(argv[2]);
        char *ip = argv[1];
        int id_socket;
        struct sockaddr_in servidor;
        struct sockaddr_in cliente;//estructura a llenar por la funcion accept
        int tam_cliente;
        int canal ;
        char buffer[50];
        int tam ;

        id_socket = socket(AF_INET,SOCK_STREAM,0);
        if (id_socket<0){
            perror("No se pudo abrir el socket");
            exit(-1);
        }

        
        servidor.sin_family = AF_INET;
        servidor.sin_port = htons(puerto);
        servidor.sin_addr.s_addr = inet_addr(ip);
        //bzero(&(servidor.sin_zero),8);

        //publica la direccion y el puerto donde se va a ejecutar
        if(bind(id_socket,(struct sockaddr *)&servidor,sizeof(struct sockaddr_in)) < 0){
            perror("No se pudo publicar el servidor ");
            close(id_socket);
            exit(-1);
        }

        if(listen(id_socket,2) == -1){
            perror("ERROR al hacer la lista");
            close(id_socket);
            exit(-1);
        }

        tam_cliente = sizeof(cliente);
        //accept devuelve el canal por el que se comunicaran
        
        if((canal = accept(id_socket,(struct sockaddr *)&cliente,&tam_cliente))==-1){
            perror("No se pudo establecer el canal");
            close(id_socket);
            exit(-1);
        }else{
            printf("Coneccion establecida desde %s\n",inet_ntoa(cliente.sin_addr));
        }

        if((tam = recv(canal,(void *)buffer,sizeof(buffer),0)) == -1){//el numero de bits recividos
            perror("Error en la recepcion");
            close(canal);
            close(id_socket);
            exit(-1);
        }

        buffer[tam]= '\0';
        printf("Mensaje recibido del servido '%s'\n",buffer);

        strcpy(buffer,"Hola amigo");
        tam = strlen(buffer);
        if(send(canal,(void *)buffer,tam,0) != tam){//el numero de bits enviados
            perror("Erros al enviar");
            close(canal);
            close(id_socket);
            exit(-1);
        }
        printf("Mensaje enviado '%s'\n",buffer);
    
        close (canal);
        close (id_socket);
    }else{
        perror("Faltan los parametros, IP, Puerto");
    }
    
}