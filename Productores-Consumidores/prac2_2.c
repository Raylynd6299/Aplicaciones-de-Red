#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <sys/stat.h>
//Funciones a usar
void *Productor(void *);
void *Consumidor(void *);
void escribir_archivo(int);
void crear_dir_archivos();
//Estructuras de informacion
typedef struct par{
    int letra;
    int numero;
}datos;
//Secciones Criticas
int letras[4],numeros[4];
FILE *archivos[10];//a.txt,b.txt,c.txt,d.txt,e.txt,zero.txt,uno.txt,dos.txt,tres.txt,cuatro.txt

//Semaphore's Globales 
sem_t semaforo_global_productores_letras,semaforo_global_consumidores_letras;
sem_t semaforo_global_productores_numeros,semaforo_global_consumidores_numeros;
sem_t sem_letras_productor[4],sem_numeros_productor[4],sem_letras_consumidor[4],sem_numeros_consumidor[4];
sem_t sem_archivos[10];

void main (int argc, char *argv[]){
    pthread_t *Productores;
    pthread_t *Consumidores;
    datos infor[5];//arreglo para los datos por hilo
    char letras[5] = {'A','B','C','D','E'};
    int Error;//Variable para los errores
    crear_dir_archivos();//Creamos archivos y carpeta

    //Espacio para los hilos
    Productores = (pthread_t *)malloc(5*sizeof(pthread_t));
    Consumidores = (pthread_t *)malloc(5*sizeof(pthread_t));
    //Asignacion de la informacion para los hilos
    for(int i = 0; i < 5 ; i++){
        infor[i].letra = letras[i];
        infor[i].numero = (i+1);
    }

	Error = sem_init(&semaforo_global_productores_letras, 0, 4);
	if(Error < 0){
		printf("Error al crear el semaforo 'semaforo_global_productores_letras'\n");
		exit(-1);
	}

    Error = sem_init(&semaforo_global_productores_numeros, 0, 4);
	if(Error < 0){
		printf("Error al crear el semaforo 'semaforo_global_productores_numeros'\n");
		exit(-1);
	}

	Error = sem_init(&semaforo_global_consumidores_letras, 0, 0);
	if(Error < 0){
		printf("Error al crear el semaforo 'semaforo_global_consumidores_letras'\n");
		exit(-1);
	}

    Error = sem_init(&semaforo_global_consumidores_numeros, 0, 0);
	if(Error < 0){
		printf("Error al crear el semaforo 'semaforo_global_consumidores_numeros'\n");
		exit(-1);
	}
    //Creamos los semaforos para los indices internos de cada seccion critica
    for(int i = 0;i < 4; i++){
        Error = sem_init(sem_letras_productor+i,0,1);
        if(Error < 0){
		    printf("Error al crear el semaforo 'semaforo_consumidores_numeros'\n");
		exit(-1);
        }
        Error = sem_init(sem_numeros_productor+i,0,1);
        if(Error < 0){
		    printf("Error al crear el semaforo 'semaforo_consumidores_numeros'\n");
		exit(-1);
	    }
        Error = sem_init(sem_letras_consumidor+i,0,0);
        if(Error < 0){
		    printf("Error al crear el semaforo 'semaforo_consumidores_numeros'\n");
		exit(-1);
        }
        Error = sem_init(sem_numeros_consumidor+i,0,0);
        if(Error < 0){
		    printf("Error al crear el semaforo 'semaforo_consumidores_numeros'\n");
		exit(-1);
	    }
    }
    //Creamos los semaforos para los archivos
    for(int i = 0;i < 10; i++){
        Error = sem_init(sem_archivos+i,0,1);
        if(Error < 0){
		    printf("Error al crear el semaforo 'sem_archivos'\n");
		    exit(-1);
        }
        
    }

    
    for(int i = 0;i<5;i++){
        pthread_create(Productores+i,NULL,(void *)Productor,infor+i);
    }
    for(int i = 0;i<5;i++){
        pthread_create(Consumidores+i,NULL,(void *)Consumidor,infor+i);
    }
    //Parte para esperar a los hilos 
    for(int i = 0;i<5;i++){
        pthread_join(*(Productores+i),NULL);
    }
    for(int i = 0;i<5;i++){
        pthread_join(*(Consumidores+i),NULL);
    }
    //Parte para destuir semaforos 
    sem_destroy(&semaforo_global_productores_letras);
    sem_destroy(&semaforo_global_consumidores_letras);
    sem_destroy(&semaforo_global_productores_numeros);
    sem_destroy(&semaforo_global_consumidores_numeros);
    for(int i = 0;i < 4; i++){
        sem_destroy(sem_letras_productor+i);
        
        sem_destroy(sem_numeros_productor+i);
        
        sem_destroy(sem_letras_consumidor+i);
        
        sem_destroy(sem_numeros_consumidor+i);
    }
    //cerramos archivos
    for(int j = 0;j < 10 ; j++){
        fclose(archivos[j]);
    }
}
//Funcion para crear/abrir archvos y crear carpeta
void crear_dir_archivos(){
    mkdir("./archivos",0777);
    archivos[0] = fopen("./archivos/a.txt","a");
    archivos[1] = fopen("./archivos/b.txt","a");
    archivos[2] = fopen("./archivos/c.txt","a");
    archivos[3] = fopen("./archivos/d.txt","a");
    archivos[4] = fopen("./archivos/e.txt","a");
    archivos[5] = fopen("./archivos/uno.txt","a");
    archivos[6] = fopen("./archivos/dos.txt","a");
    archivos[7] = fopen("./archivos/tres.txt","a");
    archivos[8] = fopen("./archivos/cuatro.txt","a");
    archivos[9] = fopen("./archivos/cinco.txt","a");  
}
//Funcion para escribir en archivos los datos
void escribir_archivo(int dato){
    if (dato > 10){
        int new_dato = dato-65;
        sem_wait(sem_archivos+new_dato);
        fprintf(archivos[new_dato],"%c\n",dato);
        sem_post(sem_archivos+new_dato);
    }else if ( dato <=5 && dato > 0){
        int new_dato = dato + 4;
        sem_wait(sem_archivos+new_dato);
        fprintf(archivos[new_dato],"%d\n",dato);
        sem_post(sem_archivos+new_dato);
    }
}


void *Productor(void *informacion){
    datos inform = *((datos *)informacion);
    int flag = 0,value;
    for(int i = 0; i < 10000; i ++){
        //printf("Productor %d, iteracion %d \n",inform.numero,i);
        sem_wait(&semaforo_global_productores_letras);
            while(flag == 0){
                for (int s = 0; s < 4;s++){
                    if(sem_getvalue(sem_letras_productor+s,&value)==0 && value >0){
                        sem_wait(sem_letras_productor+s);
                        flag ++;
                        *(letras+s)= inform.letra;
                        printf("Produciendo la letra %c en el espacio %d de letras \n",inform.letra,s);
                        sem_post(sem_letras_consumidor+s);
                        break;
                    }
                }
            }
            flag = 0;
        sem_post(&semaforo_global_consumidores_letras);

        sem_wait(&semaforo_global_productores_numeros);
            while(flag == 0){
                for(int s2 = 0; s2 < 4; s2++){
                    if(sem_getvalue(sem_numeros_productor+s2,&value)==0 && value >0){
                        sem_wait(sem_numeros_productor+s2);
                        flag ++;
                        *(numeros+s2)= inform.numero;
                        printf("Produciendo el numero %d en el espacio %d de numeros \n",inform.numero,s2);
                        sem_post(sem_numeros_consumidor+s2);
                        break;
                    }  
                } 
            }
            flag = 0;
        sem_post(&semaforo_global_consumidores_numeros);
        if(i == 9999){
            printf("Productor de %c y %d, Terminando\n",inform.letra,inform.numero);
        }
    }
}

void *Consumidor(void *arg){
    datos informe = *((datos *)arg);
    int inform;
    int flag = 0,value;
    for(int i = 0; i < 10000; i ++){
        //printf("Consumidor %d, iteracion %d\n",informe.numero,i);
        sem_wait(&semaforo_global_consumidores_letras);
            while(flag == 0){
                for(int s = 0;s <4;s++){
                    if(sem_getvalue(sem_letras_consumidor+s,&value)==0 && value >0){
                        sem_wait(sem_letras_consumidor+s);
                        flag ++;
                        inform = *(letras+s);
                        escribir_archivo(inform);
                        printf("Consumiendo la letra %c del espacio %d de letras \n",inform,s);
                        sem_post(sem_letras_productor+s);
                        break;
                    }
                }
            }
            
        sem_post(&semaforo_global_productores_letras);
        flag = 0;
        sem_wait(&semaforo_global_consumidores_numeros);
            while(flag == 0){
                for(int s2 = 0; s2 <4 ;s2 ++){
                    if(sem_getvalue(sem_numeros_consumidor+s2,&value)==0 && value >0){
                        sem_wait(sem_numeros_consumidor+s2);
                        flag ++;
                        inform = *(numeros+s2);
                        escribir_archivo(inform);
                        printf("Consumiendo el numero %d del espacio %d de numeros \n",inform,s2);
                        sem_post(sem_numeros_productor+s2);
                        break;
                    }
                }
            }
            flag = 0;
        sem_post(&semaforo_global_productores_numeros);
        if(i == 9999){
            printf("Consumidor %d, Terminando\n",informe.numero);
        }
    }
}