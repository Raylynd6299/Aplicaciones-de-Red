 
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>

//struct ip_mreq {
//	struct in_addr imr_multiaddr;	/* IP multicast address of group */
//	struct in_addr imr_interface;	/* local IP address of interface */
//};

#define MAXBUFSIZE 65536


void main(int argc, char *argv[]) {
  if(argc<2){
    printf("Error necesario argumento\n");
    exit(EXIT_FAILURE);
  }
  int sock, status,puerto=atoi(*(argv+1));
  unsigned socklen;
  char *buffer;
  struct sockaddr_in saddr;
  struct ip_mreq imreq;

  buffer=(char*)malloc(sizeof(char)*MAXBUFSIZE);

  
  memset(&saddr, 0, sizeof(struct sockaddr_in));
  memset(&imreq, 0, sizeof(struct ip_mreq));

  printf("Creando socket...");
  if((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP)) < 0){
    perror("Error creando socket\n");
    exit(EXIT_FAILURE);
  }else{
      printf("OK.");
  }
  

  saddr.sin_family = AF_INET;
  saddr.sin_port = htons(puerto);
  saddr.sin_addr.s_addr = htonl(INADDR_ANY);
  
  printf("Asignando nombre (publicando) al socket del servidor ...");
  if((status = bind(sock, (struct sockaddr *)&saddr, sizeof(struct sockaddr_in)))<0){
    printf("Error enlazando el nombre al socket\n");
    exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
  

  /* Creacion del grupo de multicast en una direccion ya pre-establecida */
  imreq.imr_multiaddr.s_addr = inet_addr("226.0.0.1");
  imreq.imr_interface.s_addr = INADDR_ANY; // use DEFAULT interface

  /* uniendo al grupo de multicast */
  printf("Uniendo al grupo...");
  if((status=setsockopt(sock, IPPROTO_IP, IP_ADD_MEMBERSHIP,(const void *)&imreq, sizeof(struct ip_mreq)))==-1){
    printf("Error uniendo al grupo.\n");
    exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
  

  socklen = sizeof(struct sockaddr_in);

  /* Recepcion de paquetes del multicast */
  printf("Recibiendo mensajes...");
  if((status=recvfrom(sock, buffer, MAXBUFSIZE, 0,(struct sockaddr *)&saddr, &socklen))==-1){
    printf("Error recibiendo mensaje.\n");
    exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
  
  printf("Se recibio: %s\n",buffer);
  shutdown(sock,SHUT_RDWR);
  close(sock);
  free(buffer);

}