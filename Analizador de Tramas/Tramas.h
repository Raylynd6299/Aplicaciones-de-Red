#include <stdio.h>
#include "colors.h"


void Analizar_Trama_UDP(unsigned char *T){
	unsigned char Tam_cabecera = (T[14]&15)*4;
    unsigned char OriginPort = ((T[34+((Tam_cabecera-20)/4)]<<8)|T[35+((Tam_cabecera-20)/4)]) ; 
    unsigned char DestinoPort = ((T[36+((Tam_cabecera-20)/4)]<<8)|T[37+((Tam_cabecera-20)/4)]) ;
    unsigned short LenghtTrama = (unsigned short)((T[38+((Tam_cabecera-20)/4)]<<8)|T[39+((Tam_cabecera-20)/4)]);
	printf("%s+++Cabecera UDP+++%s\n",KBLU,KNRM);
		printf("Puerto de origen: ");
		switch (OriginPort){
			case 7:
				printf("echo\n");
				break;
			case 19:
				printf("chargen\n");
				break;
			case 37:
				printf("time\n");
				break;
			case 53:
				printf("domain\n");
				break;
			case 67:
				printf("bootps\n");
				break;
			case 68:
				printf("bootpc\n");
				break;
			case 69:
				printf("tftp\n");
				break;
			case 137:
				printf("netbios-ns\n");
				break;
			case 138:
				printf("netbios-dgm\n");
				break;
			case 161:
				printf("snmp\n");
				break;
			case 162:
				printf("snmp-trap\n");
				break;
			case 500:
				printf("isakmp\n");
				break;
			case 514:
				printf("syslog\n");
				break;
			case 520:
				printf("rip\n");
				break;
			case 33434:
				printf("traceroute\n");
				break;
			default:
				printf("Otro\n");
				break;
		}
		printf("Puerto de Destino: ");
		switch (DestinoPort){
			case 7:
				printf("echo\n");
				break;
			case 19:
				printf("chargen\n");
				break;
			case 37:
				printf("time\n");
				break;
			case 53:
				printf("domain\n");
				break;
			case 67:
				printf("bootps\n");
				break;
			case 68:
				printf("bootpc\n");
				break;
			case 69:
				printf("tftp\n");
				break;
			case 137:
				printf("netbios-ns\n");
				break;
			case 138:
				printf("netbios-dgm\n");
				break;
			case 161:
				printf("snmp\n");
				break;
			case 162:
				printf("snmp-trap\n");
				break;
			case 500:
				printf("isakmp\n");
				break;
			case 514:
				printf("syslog\n");
				break;
			case 520:
				printf("rip\n");
				break;
			case 33434:
				printf("traceroute\n");
				break;
			default:
				printf("Otro\n");
				break;
		}
		printf("Lenght %d bytes\n",LenghtTrama);
		
		UDP(T,(33+(((T[14]&15)*4)-20)));
		
		printf("\nFin de UDP\n");
}
