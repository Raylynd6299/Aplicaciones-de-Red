#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>
//#include <time.h>


#define MAXBUF 65536

int main(){
  //Variables a utlizar...

  int sock, status;
  //obtenemos el tamaño del descriptor del socket
  unsigned int sinlen = sizeof(struct sockaddr_in);
  //Buffer para recibir el mensaje
  char *buffer;
  //Descriptor del socket del servidor
  struct sockaddr_in sock_in;
  //limpiamos el espacio de memoria del descriptor
  memset(&sock_in, 0, sinlen);
  buffer = (char *)malloc(sizeof(char)*MAXBUF);

  printf("Creando socket del servidor Broadcast ....");
  if((sock = socket (AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1){
    printf("Error creando el socket\n");
    exit(EXIT_FAILURE);
  }else{
    printf("OK\n");
  }
  //Nota: se cambio PF_INET por AF_INET, ya que segun la documentacion es lo correcto,
  //ademas que la definicion de PF_INET = 2, y la de AF_INET = PF_INET, por lo que es lo mismo


  //asignamos las promidades al socket del servidor
  sock_in.sin_addr.s_addr = htonl(INADDR_ANY);//asignamos la Ip de la interfaz de red
  sock_in.sin_port = htons(0);//el puerto se elegira aleatoriamente 
  sock_in.sin_family = AF_INET;

  //Publicamos el punto de conexion "asignamos un nombre al socket"
  printf("Asignando nombre (publicando) al socket del servidor ...");
  if ((status = bind(sock, (struct sockaddr *)&sock_in, sinlen)) <0 ){
    printf("Error asignando nombre. \n");
    exit(EXIT_FAILURE);
  }else{
    printf ("OK.\n");
  }
  
  printf("Bind Status = %d\n", status);

  /* Obtencion del puerto de conexion para el uso de Broadcast */
  printf("Obteniendo la informacion de la conexion...");
  if((status = getsockname(sock, (struct sockaddr *)&sock_in, &sinlen)) == -1 ){
      printf("Error obteniendo informacion\n");
      exit(EXIT_FAILURE); 
  }else{
    printf("OK.\n");
  }
  printf("Port access: %d\n",htons(sock_in.sin_port));
  
  //limpiamos el buffer
  memset(buffer, 0, MAXBUF);

  /* Espera el mensaje de Broadcast, se sabe que puede o no llegar  */
  printf("Esperando mensaje...");
  if((status = recvfrom(sock, buffer, MAXBUF, 0, (struct sockaddr *)&sock_in, &sinlen))== -1){
      printf("Error en la recepcion.\n");
      exit(EXIT_FAILURE);
  }else{
    printf("Mensaje Recibido.\n");
  }
  
  printf("Mensaje recibido %s, desde %s\n",buffer, inet_ntoa(sock_in.sin_addr));

  free(buffer);
  shutdown(sock, SHUT_RDWR);
  close(sock);
}