#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>

#define TAM_MAX_BUFF 65536

int main(int argc, char*argv[]){
    if(argc<2){
        printf("se necesita argumento puerto");
        exit(EXIT_FAILURE);
    }

  int sockets, status,puerto = atoi(*(argv+1));
  int sinlen = sizeof(struct sockaddr_in);
  char *buffer;
  struct sockaddr_in sock_in;
  int yes = 1;

  buffer = (char *)malloc(sizeof(char)*TAM_MAX_BUFF);
  memset(&sock_in, 0, sinlen);

  

  printf("Creando socket del servidor Broadcast ....");
  if((sockets = socket (AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1){
    printf("Error creando el socket\n");
    exit(EXIT_FAILURE);
  }else{
    printf("OK\n");
  }
  sock_in.sin_addr.s_addr = htonl(INADDR_ANY);
  sock_in.sin_port = htons(0);
  sock_in.sin_family = AF_INET;

  printf("Asignando nombre (publicando) al socket del servidor ...");
  if ((status = bind(sockets, (struct sockaddr *)&sock_in, sinlen)) <0 ){
    printf("Error asignando nombre. \n");
    exit(EXIT_FAILURE);
  }else{
    printf ("OK.\n");
  }
  /* Modificación de la configuracion para el Broadcast */
  printf("Modificando configuracion...");
  if((status=setsockopt(sockets,SOL_SOCKET,SO_BROADCAST,&yes,sizeof(int)))==-1){
    printf("Error modificando\n");
    exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
  
 
   /* Modificación del puerto al cual va llegar el mensaje del cliente */
  sock_in.sin_addr.s_addr=htonl(-1); /* send message to 255.255.255.255 */
  sock_in.sin_port = htons(puerto); /* port number */
  sock_in.sin_family = AF_INET;

  sprintf(buffer, "Bis später");//hasta luego en aleman
  //Enviando paquete al srvidor 
  printf("Enviando mensaje a servidor ..."); 
  if((status = sendto(sockets,buffer,strlen(buffer),0,(struct sockaddr *)&sock_in,sinlen))==-1){
    printf("Error enviando paquete\n");
    exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
    printf("sendto Status = %d\n", status);

  shutdown(sockets, SHUT_RDWR);
  close(sockets);
  free(buffer);
}