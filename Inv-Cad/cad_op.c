#include <stdio.h>
#include <stdlib.h>

int Longitud(char * );
void Invertir(char * ,int);
void invertir_op(char*);

void main(){
	char *cadena;
    cadena = (char *)malloc(10000);
    printf("Ingrese la Cadena: ");
    fflush(stdin);
    fgets(cadena,10000,stdin);
    invertir_op(cadena);
	printf("%s\n",cadena);
}
void invertir_op(char *cadena){
    char *inicio,*final;
    char aux;
    unsigned int i=0;
    inicio=cadena;
    while (*(cadena+i+1)!='\0'){
        final=(cadena+i);
        i++;
    }
    for(inicio,final;inicio<=final;inicio++,final--){
        aux = *(inicio);
		*(inicio) = *(final);
		*(final) = aux;
    }
    
}
