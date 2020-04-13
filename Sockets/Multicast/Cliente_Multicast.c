#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#define MAXBUFSIZE 65536


void main(int argc, char *argv[]){
  if(argc<2){
    printf("Error se necesita puerto \n");
    exit(EXIT_FAILURE);
  }
  
  int sock, status, socklen,puerto=atoi(*(argv+1));
  char *buffer;
  struct sockaddr_in saddr;
  struct in_addr iaddr;
  unsigned char ttl = 3;
  unsigned char one = 1;

  buffer = (char*)malloc(sizeof(char)*MAXBUFSIZE);

  memset(&saddr, 0, sizeof(struct sockaddr_in));
  memset(&iaddr, 0, sizeof(struct in_addr));

  printf("Creando socket del servidor Broadcast ....");
  if((sock = socket (AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1){
    printf("Error creando el socket\n");
    exit(EXIT_FAILURE);
  }else{
    printf("OK\n");
  }

  saddr.sin_family = AF_INET;
  saddr.sin_port = htons(0); // Use the first free port
  saddr.sin_addr.s_addr = htonl(INADDR_ANY); // bind socket to any interface

  printf("Asignando nombre al socket...");
  if((status = bind(sock, (struct sockaddr *)&saddr, sizeof(struct sockaddr_in)))<0){
    perror("Error nombrando socket");
    exit(EXIT_FAILURE);
  }


  iaddr.s_addr = INADDR_ANY; // use DEFAULT interface

  /* Configuracion del socket para multicast */
  printf("Configurando para Multicast...");
  if(setsockopt(sock, IPPROTO_IP, IP_MULTICAST_IF, &iaddr,sizeof(struct in_addr))==-1){
    printf("Error al configurar\n" );
    exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
  
  printf("Configurando el alcance de los datagramas...");
  if(setsockopt(sock, IPPROTO_IP, IP_MULTICAST_TTL, &ttl,sizeof(unsigned char))==-1){
      printf("Error al configurar TTL.\n");
      exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
  
  printf("Permitiendo la redifusion...");
  if(setsockopt(sock, IPPROTO_IP, IP_MULTICAST_LOOP,&one, sizeof(unsigned char))==-1){
    printf("Error permitiendo IP_MULTICAST_LOOP\n" );
    exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
  

  /* Modificacion del destino de multicast */
  saddr.sin_family = AF_INET;
  saddr.sin_addr.s_addr = inet_addr("226.0.0.1");
  saddr.sin_port = htons(puerto);


  strcpy(buffer, "Hello world in multicast\n");


  printf("Enviando mensaje...");
  if((status=sendto(sock, buffer, strlen(buffer), 0,(struct sockaddr *)&saddr, sizeof(struct sockaddr_in)))==-1){
    printf("Error enviando el mensaje\n");
    exit(EXIT_FAILURE);
  }else{
      printf("OK.\n");
  }
  
  printf("Se envio %s\n",buffer);
  shutdown(sock, SHUT_RDWR);
  close(sock);
  free(buffer);

}
