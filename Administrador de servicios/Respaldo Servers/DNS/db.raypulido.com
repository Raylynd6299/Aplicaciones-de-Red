;
; BIND data file for local loopback interface
;
$TTL	604800
@	IN	SOA	raypulido.com. admin.raypulido.com. (
			      9		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;

; name server - NS records
@ 			  	IN     NS     	ns1.raypulido.com.
;@				IN     NS	ns2.raypulido.com.

;aqui tebe de poner todos los servidores con los que trabajara

; name server - A records
ns1.raypulido.com.		IN	A	192.168.1.4
ns2.raypulido.com.		IN	A	192.168.3.4

;192.168.0.0/24 -A records
cli1.raypulido.com.		IN	A	192.168.4.4
cli2.raypulido.com.		IN	A 	192.168.2.4

;pc1.raypulido.com.		IN	A	192.168.1.2
;pc2.raypulido.com.		IN 	A	192.168.1.3


 
