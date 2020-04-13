#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
sem_t chat;
void *Fun_Can(void *);

void main(int argc,char *argv[]){
    if (argc >=3){
        int puerto = atoi(argv[2]);
        char *ip = argv[1];
        int id_socket;
        struct sockaddr_in servidor;
        struct sockaddr_in cliente;//estructura a llenar por la funcion accept
        int tam_cliente;
        int *canall ;
        char buffer[50];
        int tam ;
        
        pthread_t *sub_canales;
        
        
        sem_init(&chat, 0, 1);
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
        while (1){
                canall = (int *)malloc(sizeof(int));
                sub_canales = (pthread_t *)malloc(sizeof(pthread_t));
                if((*canall = accept(id_socket,(struct sockaddr *)&cliente,&tam_cliente))==-1){
                    perror("No se pudo establecer el canal");
                    exit(-1);
                }else{
                    pthread_create(sub_canales,NULL,(void *)Fun_Can,(void *)canall);
                }
                free(sub_canales);
                
                      
        }
        if(close (id_socket) == -1){
            perror("Error al cerrar el socket");
            exit(-1);
        }
    }else{
        perror("Faltan los parametros, IP, Puerto");
    }
    
}

void *Fun_Can(void *arg){
    int canall = *((int *)arg);
    int tam;
    char buffer[100];
    printf("Iniciamos chat\n");
    while(1){
        sem_wait(&chat);
        printf("Inicio de Chat\n");
        if((tam = recv(canall,(void *)buffer,sizeof(buffer),0)) == -1){//el numero de bits recividos
            perror("Error en la recepcion");
            //close(canal);
            //close(id_socket);
            exit(-1);
        }

        buffer[tam]= '\0';
        if(strcmp(buffer,"FIN") == 0){
            //printf("Adios\n");
            break;
        }
        printf("R:'%s'\n",buffer);

        printf(">>");
        fflush(stdin);
        scanf("%[^\n]%*c",buffer);
        
        tam = strlen(buffer);
        
        if(send(canall,(void *)buffer,tam,0) != tam){//el numero de bits enviados
            perror("Erros al enviar");
            //close(canal);
            //close(id_socket);
            exit(-1);
        }
        if(strcmp(buffer,"FIN") == 0){
            //printf("Adios\n");
            break;
        }
        printf("Fin de chat\n");
        sem_post(&chat);
        sleep(3);
        //printf("Mensaje enviado '%s'\n",buffer);
    }   
    if(close (canall) == -1){
        perror("Error al cerrar el canal");
        exit(-1);
    }
    free(arg);
}