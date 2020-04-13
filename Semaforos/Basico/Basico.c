#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
void* productor();
void* consumidor();

int nproductos=0;
sem_t s_t, s_t2;

int main (int argc, char *argv[])
{
    
    pthread_t t_productor, t_consumidor;
    if (sem_init(&s_t, 0, 1 ) < 0 ){
        printf ("Error al crear el semáforo\n");
        exit(-1);
    }
    if (sem_init(&s_t2, 0, 0 ) < 0 ){
        printf ("Error al crear el semáforo\n");
        exit(-1);
    }

    pthread_create(&t_productor, NULL, productor,NULL );
    pthread_create(&t_consumidor, NULL, consumidor,NULL );

    pthread_join (t_productor, NULL);
    pthread_join (t_consumidor, NULL);

    sem_destroy(&s_t);
    
    return 0;
}
void* productor(){
    for (int i =1;i<21;i++){
        sem_wait(&s_t);
        nproductos=i;
        printf ("Produciendo %d\n", nproductos);
        sem_post(&s_t2);
    }
    return 0;
}
void* consumidor(){
    for (int i = 1; i < 21; i++){
        sem_wait(&s_t2);
        printf ("Consumiendo %d\n", nproductos); 
        sem_post(&s_t);
    }
    return 0;
}
//No iniciar el semaforo dentro de algún hilos porque solo sera accesible para este hilo