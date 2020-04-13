#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "string.h"

void *Hola(void*);

typedef struct grupo{
    char cadena[60];
    int nums[2];
    float x;
}grp;



void main(int argc,char *argv[]){
    pthread_t *hilos;
    int i=0;
    grp *est;
    grp **res;

    if (argc>1){
        int Tam = atoi(*(argv+1));

        hilos = (pthread_t *)malloc(sizeof(pthread_t)*Tam);
        est = (grp *)malloc(sizeof(grp)*Tam);
        (res) = (grp **)malloc(sizeof(grp)*Tam);
        //creacion de un hilo
        //checar casteo antes de poner el 3er parametro      
        for(i=0;i<Tam;i++){
            strcpy((est+i)->cadena,"Hola soy un hilo, escrito desde el padre");
            (est+i)->nums[0]=5;
            (est+i)->nums[1]=6;
            (est+i)->x=5.15;
            pthread_create(hilos+i,NULL,Hola,(void*)(est+i));
        }
        //paso 2
        //El proceso padre espera al hilo
        for(i=0;i<Tam;i++){
            pthread_join(*(hilos+i),(void *)&(*(res+i)));
            
            printf("Mostrar desde Padre\n");
            printf("Cadena: %s\n",(*(res+i))->cadena);
            printf("Numero 1 = %d,Numero 2 = %d\n",(*(res+i))->nums[0],(*(res+i))->nums[1]);
            printf("Flotante %f\n",(*(res+i))->x);
            
        }
        
    }else
        perror("Te equivocas bro");
}

void *Hola(void *estructura){
    grp *est2 = (grp *)malloc(sizeof(grp));
    grp *est = (grp*)estructura;
    
    printf("\tDesde el hilo\n");
    printf("\tHilo-Cadena: %s\n",(est)->cadena);
    printf("\tHilo-Numero 1 = %d,Numero 2 = %d\n",(est)->nums[0],(est)->nums[1]);
    printf("\tHilo-Flotante %f\n",(est)->x);

    strcpy((est2)->cadena,"Hola soy un hilo, escrito desde el hilo");
    (est2)->nums[0]=(rand()%10)+10;
    (est2)->nums[1]=rand()%21+20;
    (est2)->x=rand();
    pthread_exit((void *)est2);
}