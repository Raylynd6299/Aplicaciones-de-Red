//4 Hilos prooductores, 4 consumidores,2 seccriticas
//20 valores cada uno
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

void *Productor(void *);
void *Consumidor(void *);

int seCri1,seCri2;

sem_t s_global,s_global2,s_global3,s_global4;

void main (int argc, char *argv[]){
    
    pthread_t *Productores;
    pthread_t *Consumidores;
    char letras[4] = {'A','B','C','D'};

    Productores = (pthread_t *)malloc(4*sizeof(pthread_t));
    Consumidores = (pthread_t *)malloc(4*sizeof(pthread_t));

    int err,err2,err3;
	int n;
	//Paso 1: Crear al semáforo
	err = sem_init(&s_global, 0, 1);
	if(err < 0){
		printf("Error al crear el semaforo\n");
		exit(-1);
	}
    err2 = sem_init(&s_global, 0, 1);
	if(err < 0){
		printf("Error al crear el semaforo\n");
		exit(-1);
	}
	err3 = sem_init(&s_global3, 0, 0);
	if(err3 < 0){
		printf("Error al crear el semaforo\n");
		exit(-1);
	}
    
    for(int i = 0;i<4;i++){
        pthread_create(Productores+i,NULL,(void *)Productor,letras+i);
    }
    for(int i = 0;i<4;i++){
        pthread_create(Consumidores+i,NULL,(void *)Consumidor,letras+i);
    }
    for(int i = 0;i<4;i++){
        pthread_join(*(Productores+i),NULL);
    }
    for(int i = 0;i<4;i++){
        pthread_join(*(Consumidores+i),NULL);
    }
}

void *Productor(void *letra){
    char let = *((char *)letra);
    int intento = 0;
    for(int i = 0;i<20;i++){
        if(sem_wait(&s_global) != -1){
            printf("Produciendo %c\n",let);
            seCri1 = let;
            sem_post(&s_global3);
        }else{//no se pudo decrementar
            intento ++;
        }
        if (intento == 1){
            if(sem_wait(&s_global2) != -1){
             printf("Produciendo %c\n",let);
            seCri2 = let;
             sem_post(&s_global4);
            }else{//no se pudo decrementar
                intento ++;
            }
        }else{
            intento = 0;
        }

    }
}

void *Consumidor(void *arg){
    char letra ;
    int intento = 0;
    for(int i = 0;i<20;i++){
        if(sem_wait(&s_global3) != -1){
            letra = seCri1;
            printf("consumiendo %c\n",letra);
            sem_post(&s_global);
            
        }else{//no se pudo decrementar
            intento ++;
        }
        if (intento == 1){
            if(sem_wait(&s_global4) != -1){
             letra = seCri2;
             
            printf("consumiendo %c\n",letra);
             sem_post(&s_global2);
            }else{//no se pudo decrementar
                intento ++;
            }
        }else{
            intento = 0;
        }
    }
}