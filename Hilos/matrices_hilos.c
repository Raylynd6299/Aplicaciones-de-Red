#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

//pre_compilados y estructura de funciones
void *Multiplicar(void *);
void llenar (int **,int, int);
void mostrar (int **,int,int);

//Estructuras
typedef struct informacion{
    int Inicio;
    int Final;
    int Filas_A;
    int Columnas_A;
    int Filas_B;
    int Columnas_B;
}info;

//Variables globales
int **Mat_A,**Mat_B,**Mat_C;

void main(int argc,char **argv){
    if(argc>1){
        //variables
        int F_A,C_A,F_B,C_B, i;
        int NumHilos = atoi(*(argv+1));
        info *infor  = NULL;
        int fxh = 0;
        int residuo = 0;
        pthread_t *Hilos = NULL;
        int indice=0;

        //Pedimos el tamaño de las matrices
        printf("Ingrese las dimensiones de la Matriz A: NxM: ");
        scanf("%dx%d",&F_A,&C_A);
        printf("Ingrese las dimensiones de la Matriz B: NxM: ");
        scanf("%dx%d",&F_B,&C_B);
       
        if(C_A == F_B && C_A>0&&F_A>0&&C_B>0&&F_B>0){
            //obteniendo datos
            fxh = F_A/NumHilos;
            residuo = F_A%NumHilos;

            //asignamos espacios de memoria a las matrices
            Mat_A = (int **)calloc(F_A,sizeof(int *));
            for(i=0;i<F_A;i++)
                *(Mat_A+i) = calloc(C_A,sizeof(int));
            Mat_B = (int **)calloc(F_B,sizeof(int *));
            for(i=0;i<F_B;i++)
                *(Mat_B+i) = calloc(C_B,sizeof(int));
            Mat_C = (int **)calloc(F_A,sizeof(int *));
            for(i=0;i<F_A;i++)
                *(Mat_C+i) = calloc(C_B,sizeof(int));
            
            //Llenar
            llenar(Mat_A,F_A,C_A);
            llenar(Mat_B,F_B,C_B);
            
            //mostrar llenas
            printf("Matriz A \n");
            mostrar(Mat_A,F_A,C_A);
            printf("Matriz B \n");
            mostrar(Mat_B,F_B,C_B);
            //printf("Matriz C \n");
            //mostrar(Mat_C,F_A,C_B);

            //Espacio para hilos e informacion
            Hilos = (pthread_t *)malloc(NumHilos * sizeof(pthread_t));
            infor = (info *)malloc(NumHilos * sizeof(info));

            if(F_A>=NumHilos){//Si hay mas filas en A que hilos
                for(i = 0; i<NumHilos ; i++){
                    if(i != (NumHilos-1)){
                        (infor+i)->Inicio = indice;
                        indice += (fxh-1);
                        (infor+i)->Final = indice;
                        indice ++;
                    }else{
                        (infor+i)->Inicio = indice;
                        indice += (fxh-1+residuo);
                        (infor+i)->Final = indice;
                        indice ++;
                    }
                    (infor+i)->Filas_A = F_A;
                    (infor+i)->Columnas_A = C_A;
                    (infor+i)->Filas_B = F_B;
                    (infor+i)->Columnas_B = C_B;
                    //printf("Hilos #%d, inicio = %d, final = %d,\n, matriz A : Filas = %d, Columnas = %d,\n matriz B: Filas = %d, Columnas = %d\n",i,infor[i].Inicio,infor[i].Final,infor[i].Filas_A,infor[i].Columnas_A,infor[i].Filas_B,infor[i].Columnas_B);
                }

                //enviando a los hilos a hacer su trabajo
                for(i = 0;i<NumHilos;i++)
                    pthread_create(Hilos+i,NULL,Multiplicar,(void *)(infor+i));
                
                for(i=0;i<NumHilos;i++)
                    pthread_join(*(Hilos+i),NULL);

                printf("Matriz C \n");
                mostrar(Mat_C,F_A,C_B);
                
            }else{//si hay mas hilos que filas en A
                for(i = 0; i<F_A ; i++){
                    
                    (infor+i)->Inicio = indice;
                    (infor+i)->Final = indice;
                    indice ++;
                    
                    (infor+i)->Filas_A = F_A;
                    (infor+i)->Columnas_A = C_A;
                    (infor+i)->Filas_B = F_B;
                    (infor+i)->Columnas_B = C_B;
                    //printf("Hilos #%d, inicio = %d, final = %d,\n, matriz A : Filas = %d, Columnas = %d,\n matriz B: Filas = %d, Columnas = %d\n",i,infor[i].Inicio,infor[i].Final,infor[i].Filas_A,infor[i].Columnas_A,infor[i].Filas_B,infor[i].Columnas_B);
                }
                //llamar hillos
                for(i = 0;i<F_A;i++)
                    pthread_create((Hilos+i),NULL,Multiplicar,(void *)(infor+i));
                
                for(i=0;i<F_A;i++)
                    pthread_join(*(Hilos+i),NULL);

                printf("Matriz C \n");
                mostrar(Mat_C,F_A,C_B);
            }
        }else{
            perror("Bro tus matrices no tienen el tamaño adecuado");
        }
    }else{
        perror("Te equivocaste Bro, pon el numero de Hilos");
    }
}
void *Multiplicar(void *indexs){
    info *infor = (info *)indexs;
    int res=0;
    int FA,CA,FB,CB;
    for(FA = infor->Inicio; FA <= infor->Final ;FA++){
        for(CB = 0;CB < infor->Columnas_B;CB++){
            for(CA = 0,FB = 0;CA < infor->Columnas_A,FB < infor->Filas_B;CA ++,FB++){
                res += ( *(*(Mat_A+FA)+CA) * *(*(Mat_B+FB)+CB));
            }
            *(*(Mat_C+FA)+CB) = res;
            res = 0;
        }
    }
}

void llenar (int **matrice,int filas,int columnas){
    int f,c;
    for(f = 0;f < filas;f++)
        for(c = 0;c < columnas;c++)
            *(*(matrice+f)+c) = (rand()%6 + 1);
}
void mostrar (int **matrice,int filas,int columnas){
    int f,c;
    for(f = 0;f < filas;f++){
        for(c = 0;c < columnas;c++) 
            printf(" %d ",*(*(matrice+f)+c));
        printf("\n");
    }
    printf("\n");
}