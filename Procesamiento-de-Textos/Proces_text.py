import subprocess
import os
import sys
from threading import Thread

def obtener_archivos():
    Cuentos = os.popen('cd Cuentos;ls').read()
    archivos = Cuentos.split("\n")
    if(archivos[len(archivos)-1]==""):
        archivos.pop()
    return archivos

def buscar_en_cuento(*args,**kwargs):
    #print(kwargs["Inicio"],kwargs["Fin"])
    for i in range(kwargs["Inicio"],kwargs["Fin"]+1):
        with open("./Cuentos/"+args[0][i],'r') as cuento:
            #print(args[0][i])
            for linea in cuento.readlines():
                palabras = (linea.strip()).split()
                for palabra in palabras:
                    palabra = palabra.replace(",","")
                    palabra = palabra.replace(".","")
                    palabra = palabra.replace("—","")
                    palabra = palabra.replace("¿","")
                    palabra = palabra.replace("?","")
                    palabra = palabra.replace("¡","")
                    palabra = palabra.replace("-","")
                    palabra = palabra.replace("!","")
                    palabra = palabra.replace(";","")
                    palabra = palabra.replace(":","")
                    if (palabra == "Alegria".lower()):
                        args[1][i][palabra] +=1
                    elif (palabra == "Amor".lower()):
                        args[1][i][palabra] +=1
                    elif (palabra == "Enojo".lower()):
                        args[1][i][palabra] +=1
                    elif (palabra == "Ira".lower()):
                        args[1][i][palabra] +=1
                    elif (palabra == "Sueño".lower()):
                        args[1][i][palabra] +=1
                    elif (palabra == "Aburrimiento".lower()):
                        args[1][i][palabra] +=1
                    args[1][i]["Total"] +=1
                    #print(palabra)
        #print("En el Cuento {},Hay:".format(args[0][i]))
        #print('"Alegria":{}, "Amor":{}, "Enojo":{}, "Ira":{}, "Sueño":{}, "Aburrimiento":{}, "Total":{}'.format(args[1][i]["alegria"],args[1][i]["amor"],args[1][i]["enojo"],args[1][i]["ira"],args[1][i]["sueño"],args[1][i]["aburrimiento"],args[1][i]["Total"]))
        #print("El Cuento es {}, Tiene las palabras {}".format(args[0][i],args[1][i]))


if(len(sys.argv)>1):
    """Profesor mi profesora Daniela Cortes dice que cuando sale con ella que eta bien guapo"""
    Hilos = [None] * int(sys.argv[1])
    lista = []
    palabras = {"Alegria".lower():0,"Amor".lower():0,"Enojo".lower():0,"Ira".lower():0,"Sueño".lower():0,"Aburrimiento".lower():0,"Total":0}
    Cuentos = obtener_archivos()

    for i in range(0,len(Cuentos)):
        lista.append(palabras.copy())

    if(len(Cuentos)>int(sys.argv[1])): #Si hay mas cuentos que hilos   
        #gestionar numero de cuentos por Hilos
        CxH = int(len(Cuentos)//int(sys.argv[1]))
        residuos = int(len(Cuentos)%int(sys.argv[1]))
        indice = 0
        for i in range(len(Hilos)):
            if(i != (len(Hilos)-1)):
                Hilos[i] = Thread(target=buscar_en_cuento,args=(Cuentos,lista),kwargs={"Inicio":indice,"Fin":(indice + (CxH-1))},daemon=True)
                indice+=(CxH); 
            else:
                Hilos[i] = Thread(target=buscar_en_cuento,args=(Cuentos,lista),kwargs={"Inicio":indice,"Fin":(indice + (CxH-1+residuos))},daemon=True)
                indice+= CxH+residuos; 
        for i in range(len(Hilos)):
            Hilos[i].start()
        for i in range(len(Hilos)):
            Hilos[i].join()
        for i in range(0,len(Cuentos)):
            for k in palabras.keys():
                palabras[k] += lista[i][k]

        for i in range(0,len(Cuentos)):
            print("\t\t\t\t\t\t\t\t\t\t\tEn el Cuento {},Hay:".format(Cuentos[i]))
            print('"Alegria":{}, "Amor":{}, "Enojo":{}, "Ira":{}, "Sueño":{}, "Aburrimiento":{}, "Total":{}'.format(lista[i]["alegria"],lista[i]["amor"],lista[i]["enojo"],lista[i]["ira"],lista[i]["sueño"],lista[i]["aburrimiento"],lista[i]["Total"]))

        for k in palabras.keys():
            if(k != "Total"):
                print("Porcentaje de aparicion de '{}' es:{}".format(k,((palabras[k])*100)/palabras["Total"]))
            
        print("El numero de palabras encontradas en {} Cuentos son {}".format(len(Cuentos),palabras))


    else:
        print("Hay mas Hilos que Cuentos")
        print("Se mandara un hilo por cuento")
        

        for i in range (len(Cuentos)):
            Hilos[i] = Thread(target=buscar_en_cuento,args=(Cuentos,lista,),kwargs={"Inicio":i,"Fin":i},daemon=True)

        for i in range (len(Cuentos)):
            Hilos[i].start() 
        for i in range(len(Cuentos)):
            Hilos[i].join()
        
        for i in range(0,len(Cuentos)):
            for k in palabras.keys():
                palabras[k] += lista[i][k]
        for i in range(0,len(Cuentos)):
            print("\t\t\t\t\t\t\t\t\t\t\tEn el Cuento {},Hay:".format(Cuentos[i]))
            print('"Alegria":{}, "Amor":{}, "Enojo":{}, "Ira":{}, "Sueño":{}, "Aburrimiento":{}, "Total":{}'.format(lista[i]["alegria"],lista[i]["amor"],lista[i]["enojo"],lista[i]["ira"],lista[i]["sueño"],lista[i]["aburrimiento"],lista[i]["Total"]))

        for k in palabras.keys():
            if(k != "Total"):
                print("Porcentaje de aparicion de '{}' es:{}".format(k,((palabras[k])*100)/palabras["Total"]))
            
        print("El numero de palabras encontradas en {} archivos son {}".format(len(Cuentos),palabras))

else:
    print("Bro te falto el parametro")
