from flask import Blueprint
from flask import abort,render_template,request, flash,redirect,url_for
from flask_login import current_user,login_user,logout_user,login_required
from . import login_manager
from .consts import *
from .forms import LoginForm, RegisterForm,TaskForm,Dhcp_Sub,DHCP_PCstatic,IP_trusted,DNS_zonas
from .models import User,Task
from .backups import do_back
import sys,os
sys.setrecursionlimit(1600000000)
page = Blueprint('page',__name__)

conf_base_dhcp = 'option domain-name-servers 192.168.1.4;\ndefault-lease-time 600;\nmax-lease-time 7200;\nddns-update-style none;\nlog-facility local7;\n\n'
config_dhcp_fin = ''

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)

@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/error_404.html'),404

@page.route('/')
def index():
    return render_template('index.html',title="Redes2",active='index')

@page.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT)
    return redirect(url_for('.login'))

@page.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".servers"))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(LOGIN_CORRECT)
            return redirect(url_for('page.servers'))
        else:
            flash(ERROR_LOGIN,'error') 
            
    return render_template('auth/login.html',title='Login',form=form,active='login')


@page.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".servers"))
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User.create_element(form.username.data,form.password.data,form.email.data)
            flash(USER_CREATED)
            login_user(user)
            return redirect(url_for('page.servers'))
        
    return render_template('auth/register.html',title='Register',form =form,active='Register')










step = -1
ips_trusteds = []
Dominio = ""
ips_respuestas = []

#Servidores
@page.route('/servers')
@login_required
def servers():
    return render_template('servers/list.html',title='Servidores',active='servers')

#DNS
@page.route('/servers/dns',methods =['GET'])
@login_required
def dns():
    global step
    ip_trusted = IP_trusted(request.form)
    form_dom = DNS_zonas(request.form)
    return render_template('servers/dns.html',form_trus=ip_trusted,form_dom=form_dom,step=step,title='Servidor DNS',active='servers')

@page.route('/servers/dns/<int:paso>',methods =['GET','POST'])
@login_required
def dns_gest(paso):
    global step,ips_trusteds,Dominio,ips_respuestas
    ip_trusted = IP_trusted()
    form_dom = DNS_zonas()

    if(paso == 0):
        if(step != -1):
            ips_trusteds = []
            ips_respuestas = []
            Dominio =""
            step = -1
            return render_template('servers/dns.html',form_trus=ip_trusted,form_dom=form_dom,step=step,title='Servidor DNS',active='servers')

        ip_trusted = IP_trusted(request.form)
        if request.method == 'POST' and ip_trusted.validate():
            ips_trusteds.append(ip_trusted.ip.data)
            #print(ips_trusteds)    
            ip_trusted = IP_trusted()
            flash("Ip Guardado")
            return render_template('servers/dns.html',step=step+1,form_trus=ip_trusted,form_dom=form_dom,title='Servidor DNS',active='servers')
        return render_template('servers/dns.html',step=step+1,form_trus=ip_trusted,form_dom=form_dom,title='Servidor DNS',active='servers')

    elif paso == 1:
        #print(ips_trusteds)
        if(step > 1):
            #Resetear todo
            ips_trusteds = []
            Dominio =""
            step = -1
            ips_respuestas = []
            return render_template('servers/dns.html',form_trus=ip_trusted,form_dom=form_dom,step=step,title='Servidor DNS',active='servers')
        
        form_dom = DNS_zonas(request.form)
        if request.method == 'POST' and form_dom.validate():
            step += 2
            Dominio = form_dom.dominio.data
            #print(Dominio)
            #print(ips_trusteds)
            return render_template('servers/dns.html',step=step+1,form_trus=ip_trusted,form_dom=form_dom,title='Servidor DNS',active='servers')
        else:
            return render_template('servers/dns.html',step=step+2,form_trus=ip_trusted,form_dom=form_dom,title='Servidor DNS',active='servers')
        return render_template('servers/dns.html',step=-1,form_trus=ip_trusted,form_dom=form_dom,title='Servidor DNS',active='servers')

    elif paso == 2:
        #print(ips_trusteds)
        #print(Dominio)
        if(step != 1):
            ips_trusteds = []
            ips_respuestas = []
            Dominio =""
            step = -1
            return render_template('servers/dns.html',form_trus=ip_trusted,form_dom=form_dom,step=step,title='Servidor DNS',active='servers')
        ip_trusted = IP_trusted(request.form)
        if request.method == 'POST' and ip_trusted.validate():
            ips_respuestas.append(ip_trusted.ip.data)
            print(ips_respuestas)    
            ip_trusted = IP_trusted()
            flash("Ip Guardado")
            return render_template('servers/dns.html',step=step+1,form_trus=ip_trusted,form_dom=form_dom,title='Servidor DNS',active='servers')
        return render_template('servers/dns.html',step=step+1,form_trus=ip_trusted,form_dom=form_dom,title='Servidor DNS',active='servers')
    elif paso == 3:
        
        step +=2
        #print(Dominio,ips_trusteds,ips_respuestas)
        return render_template('servers/dns.html',step=step,form_trus=ip_trusted,form_dom=form_dom,title='Servidor DNS',active='servers')
    else:
        flash("Error paso no reconocido",'error')
    return redirect(url_for('page.servers'))

@page.route('/servers/dns/<string:name>')
@login_required
def dns_config(name):
    global step,ips_trusteds,Dominio,ips_respuestas
    named_conf_options_ini = 'acl "trusted" {\n     '
    named_conf_options_fin = '};\noptions {\n       directory "/var/cache/bind";\n       recursion yes;\n       allow-recursion{ trusted;};\n       listen-on {192.168.1.4;};\n       allow-transfer {none;};\n       forwarders {\n            192.168.3.4;\n       };\n       dnssec-validation auto;\n       listen-on-v6 { any; };\n};\n'
    
    named_conf_local_ini = 'zone "'
    named_conf_local_sig2 = '" {\n       type master;\n       file "/etc/bind/zones/db.'
    named_conf_local_sig3 = '";\n};\nzone "168.192.in-addr.arpa" {\n        type master;\n        file "/etc/bind/zones/db.192.168";\n};\n'
    
    zona_local_direc_ini = '$TTL    604800\n@       IN      SOA     '
    zona_local_direc_sig2 = '. admin.'
    zona_local_direc_sig3 = '. (\n                             '
    zona_local_direc_sig4 = '         ; Serial\n                         604800         ; Refresh\n                          86400         ; Retry\n                        2419200         ; Expire\n                         604800 )       ; Negative Cache TTL\n; name server - NS records\n@               IN     NS       '
    zona_local_direc_ina = '.              IN      A       '

    zona_local_indirecta_inptr = '             IN              PTR             '

    if(name == "guardada"):

        named_conf_options = named_conf_options_ini
        for ip in ips_trusteds:
            named_conf_options = named_conf_options + ip + ";\n     "
        named_conf_options = named_conf_options + named_conf_options_fin

        named_conf_local = named_conf_local_ini + Dominio + named_conf_local_sig2 + Dominio + named_conf_local_sig3

        serial = os.popen("sudo -S cat /etc/bind/zones/db.192.168 | grep 'Serial'").read()
        serial = serial.strip().split(" ")[0]
        serial = serial.split("\t")[0]
        serial = int(serial)

        zona_local_direc = zona_local_direc_ini + Dominio + zona_local_direc_sig2 + Dominio + zona_local_direc_sig3 + str(serial+1) + zona_local_direc_sig4 + 'ns1.' + Dominio + '.\n\n'
        zona_local_direc = zona_local_direc + 'ns1.' + Dominio + zona_local_direc_ina + '192.168.1.4\nns2.' + Dominio + zona_local_direc_ina + '192.168.3.4\n'
        for indi,ip_p in enumerate(ips_respuestas):
            zona_local_direc = zona_local_direc + "cli" + str(indi+1) + '.' + Dominio + zona_local_direc_ina + ip_p + "\n"
        
        zona_local_indirecta = zona_local_direc_ini + Dominio + zona_local_direc_sig2 + Dominio + zona_local_direc_sig3 + str(serial+1) + zona_local_direc_sig4 + 'ns1.' + Dominio + '.\n\n'
        zona_local_indirecta = zona_local_indirecta + '4.1' + zona_local_indirecta_inptr + 'ns1.' + Dominio + '.\n4.3' + zona_local_indirecta_inptr + 'ns2.' + Dominio + '.\n'
        for indi,ip_p in enumerate(ips_respuestas):
            ip_cad = ip_p.split(".")
            ip_cad = ip_cad[3] + "." + ip_cad[2]
            zona_local_indirecta = zona_local_indirecta + ip_cad + zona_local_indirecta_inptr + 'cli' + str(indi+1) +'.' + Dominio + '.\n'

        cof = '\n'+named_conf_options + '\n\n' + named_conf_local + '\n\n' + zona_local_direc + '\n\n' + zona_local_indirecta + '\n\n'
        return render_template('servers/show.html',title='Configuracion Desarrollandose',tit="Configuracion realizado",cof=cof)
    elif(name == "eliminar"):
        ips_trusteds = []
        Dominio = ''
        ips_respuestas = []
        step = -1
        flash("Configuracion eliminada")
        return redirect(url_for('page.dns'))
    elif name == "cargar" :

        named_conf_options = named_conf_options_ini
        for ip in ips_trusteds:
            named_conf_options = named_conf_options + ip + ";\n     "
        named_conf_options = named_conf_options + named_conf_options_fin

        named_conf_local = named_conf_local_ini + Dominio + named_conf_local_sig2 + Dominio + named_conf_local_sig3

        serial = os.popen("sudo -S cat /etc/bind/zones/db.192.168 | grep 'Serial'").read()
        serial = serial.strip().split(" ")[0]
        serial = serial.split("\t")[0]
        serial = int(serial)

        zona_local_direc = zona_local_direc_ini + Dominio + zona_local_direc_sig2 + Dominio + zona_local_direc_sig3 + str(serial+1) + zona_local_direc_sig4 + 'ns1.' + Dominio + '.\n\n'
        zona_local_direc = zona_local_direc + 'ns1.' + Dominio + zona_local_direc_ina + '192.168.1.4\nns2.' + Dominio + zona_local_direc_ina + '192.168.3.4\n'
        for indi,ip_p in enumerate(ips_respuestas):
            zona_local_direc = zona_local_direc + "cli" + str(indi+1) + '.' + Dominio + zona_local_direc_ina + ip_p + "\n"
        
        zona_local_indirecta = zona_local_direc_ini + Dominio + zona_local_direc_sig2 + Dominio + zona_local_direc_sig3 + str(serial+1) + zona_local_direc_sig4 + 'ns1.' + Dominio + '.\n\n'
        zona_local_indirecta = zona_local_indirecta + '4.1' + zona_local_indirecta_inptr + 'ns1.' + Dominio + '.\n4.3' + zona_local_indirecta_inptr + 'ns2.' + Dominio + '.\n'
        for indi,ip_p in enumerate(ips_respuestas):
            ip_cad = ip_p.split(".")
            ip_cad = ip_cad[3] + "." + ip_cad[2]
            zona_local_indirecta = zona_local_indirecta + ip_cad + zona_local_indirecta_inptr + 'cli' + str(indi+1) +'.'+ Dominio + '.\n'

        cof_op = open("./named.conf.options",'w')
        cof_op.write("\n"+named_conf_options)
        cof_op.close()

        conf_local = open("./named.conf.local",'w')
        conf_local.write("\n"+named_conf_local)
        conf_local.close()

        zon_dire = open("./db."+Dominio,'w')
        zon_dire.write("\n"+zona_local_direc)
        zon_dire.close()
        
        zon_indi = open("./db.192.168",'w')
        zon_indi.write("\n"+zona_local_indirecta)
        zon_indi.close()


        os.popen("sudo -S rm -R /etc/bind/zones").read()
        os.popen("sudo -S mkdir /etc/bind/zones").read()

        os.popen("sudo -S mv ./named.conf.options /etc/bind/named.conf.options").read()
        os.popen("sudo -S mv ./named.conf.local /etc/bind/named.conf.local").read()
        os.popen("sudo -S mv ./db." + Dominio + " /etc/bind/zones/")
        os.popen("sudo -S mv ./db.192.168 /etc/bind/zones/")
        
        checkconf= os.popen("sudo -S named-checkconf").read()
        if checkconf == '':
            checkzone_dir = os.popen("sudo -S named-checkzone " + Dominio + " /etc/bind/zones/db."+Dominio+" | grep 'OK' ").read()
            if checkzone_dir != '':
                checkzone_indir = os.popen("sudo -S named-checkzone  168.192.in-addr.arpa /etc/bind/zones/db.192.168 | grep 'OK' ").read()
                if checkzone_indir != '':
                    dom_old = os.popen("sudo -S cat /etc/dhcp/dhcpd.conf |grep 'option domain-name '").read()
                    dhcpp = os.popen("sudo -S cat /etc/dhcp/dhcpd.conf").read()
                    dom_new = 'option domain-name "'+Dominio+'";\n'
                    dhcpp = dhcpp.replace(dom_old,dom_new)

                    confi_dhcp = open("./dhcpd.conf",'w')
                    confi_dhcp.write('\n'+dhcpp)
                    confi_dhcp.close()
                    os.popen("sudo -S mv ./dhcpd.conf /etc/dhcp/dhcpd.conf").read()
                    os.popen("sudo -S systemctl restart isc-dhcp-server").read()
                    os.popen("sudo -S systemctl restart bind9").read()
                    flash("Configuracion cargada, servidor reiniciado")
            else:
                flash("Error al configurar la zona directa",'error')
        else:
            flash("Error en la configuracion",'error')
        
        return redirect(url_for('page.dns'))
    else:
        flash("Opcion Invalida",'error')
    
    #return render_template('servers/show.html',title='Backup',tit=name,cof=cof)
    return redirect(url_for('page.dns'))


#DHCP
@page.route('/servers/dhcp',methods =['GET'])
@login_required
def dhcp():
    form1 = Dhcp_Sub(request.form)
    form2 = DHCP_PCstatic(request.form)
    return render_template('servers/dhcp.html',title='Servidor DHCP',form1=form1,form2=form2,active='servers')

@page.route('/servers/dhcp/subnet',methods =['POST'])
@login_required
def dhcp_subnet():
    global config_dhcp_fin
    form = Dhcp_Sub(request.form)
    if request.method == 'POST' and form.validate():
        f_line = 'subnet ' + form.ip_subnet.data + ' netmask ' + form.mask.data + ' {\n'
        s_line = '      range ' + form.range_down.data + ' ' + form.range_up.data +';\n'
        t_line = '      option routers ' + form.ip_router.data + ';\n'
        c_line = '      option broadcast-address ' + form.ip_broadcast.data + ';\n}\n'
        config_dhcp_fin = f_line + s_line + t_line + c_line + config_dhcp_fin
        print(config_dhcp_fin)
        flash("Configuracion de subred GUARDADA")
        return redirect(url_for('page.dhcp'))
    flash("Error en el Formulario",'error')
    return redirect(url_for('page.dhcp'))

@page.route('/servers/dhcp/static',methods =['POST'])
@login_required
def dhcp_static():
    global config_dhcp_fin
    form = DHCP_PCstatic(request.form)
    if request.method == 'POST' and form.validate():
        f_line = 'host ' + form.Nombre.data + ' {\n'
        s_line = '      hardware ethernet ' + form.MAC.data +';\n'
        t_line = '      fixed-address ' + form.ip_static.data + ';\n'
        c_line = '      option routers ' + form.ip_router.data + ';\n'
        q_line = '      option subnet-mask ' + form.mask.data + ';\n}\n'
        config_dhcp_fin = config_dhcp_fin + f_line + s_line + t_line + c_line + q_line
        #print(config_dhcp_fin)
        flash("Configuracion de ip estatica GUARDADA")
        return redirect(url_for('page.dhcp'))
    flash("Error en el Formulario",'error')
    return redirect(url_for('page.dhcp'))

@page.route('/servers/dhcp/<string:name>')
@login_required
def dhcp_config(name):
    global config_dhcp_fin,conf_base_dhcp

    if(name == 'actual'):
        cof = os.popen("cat /etc/dhcp/dhcpd.conf").read()
        return render_template('servers/show.html',title='Configuracion Actual',tit="Configuracion Actual",cof=cof)
    elif(name == "guardada"):
        dom_old = os.popen("sudo -S cat /etc/dhcp/dhcpd.conf |grep 'option domain-name '").read()
        cof = '\n'+dom_old+'\n'+ conf_base_dhcp + config_dhcp_fin
        return render_template('servers/show.html',title='Configuracion Desarrollandose',tit="Configuracion Actual",cof=cof)
    elif(name == "eliminar"):
        config_dhcp_fin = ''
        flash("Configuracion eliminada")
        return redirect(url_for('page.dhcp'))
    elif name == "cargar" :
        dom_old = os.popen("sudo -S cat /etc/dhcp/dhcpd.conf |grep 'option domain-name '").read()
        confi = open("/home/ray/Desktop/dhcpd.conf",'w')
        confi.write('\n'+dom_old+'\n'+ conf_base_dhcp + config_dhcp_fin)
        confi.close()

        os.popen("sudo -S mv /home/ray/Desktop/dhcpd.conf /etc/dhcp/dhcpd.conf").read()
        config_dhcp_fin = ''
        os.popen("sudo -S systemctl restart isc-dhcp-server").read()
        flash("Configuracion cargada, servidor reiniciado")
    else:
        flash("Opcion Invalida",'error')
    
    #return render_template('servers/show.html',title='Backup',tit=name,cof=cof)
    return redirect(url_for('page.dhcp'))






#TFTP
@page.route('/servers/tftp',methods =['GET','POST'])
@login_required
def tftp():
    names =  []
    if request.method == 'POST':
        th = do_back()
        th.join()
        NameBackups = os.popen("cd /var/www/raypulido/app/Backups/; ls").read()
        NameBackups = NameBackups.strip().split("\n")
        flash("Operacion exitosa")
        return render_template('servers/tftp.html',backs=NameBackups,on=1,title='Servidor TFTP',active='servers')
    #flash("ESPERANDO INICIO",'error')
    NameBackups = os.popen("cd /var/www/raypulido/app/Backups/; ls").read()
    NameBackups = NameBackups.strip().split("\n")
    return render_template('servers/tftp.html',backs=NameBackups,on=0,title='Servidor TFTP',active='servers')

@page.route('/servers/tftp/<string:name>')
@login_required
def get_backup(name):
    cof = os.popen("cat /var/www/raypulido/app/Backups/"+name+"/"+name).read()
    return render_template('servers/show.html',title='Backup',tit=name,cof=cof)


#Panel de todos los Servers
@page.route('/servers/start/<int:type>',methods=['GET','POST'])
@login_required
def start_servers(type):
    names = []
    if (type == 0): #tftp
        respuesta = os.popen("sudo -S systemctl start tftpd-hpa").read()
        status = os.popen("sudo -S systemctl status tftpd-hpa| grep 'active' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "active":
            flash("El Servidor inicio CORRECTAMENTE")
        else:
            flash("Error al Iniciar el servicio",'error')
        return redirect(url_for('page.tftp'))
    elif (type == 1): #tftp
        respuesta = os.popen("sudo -S systemctl start isc-dhcp-server").read()
        status = os.popen("sudo -S systemctl status isc-dhcp-server| grep 'active' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "active":
            flash("El Servidor inicio CORRECTAMENTE")
        else:
            flash("Error al Iniciar el servicio",'error')
        return redirect(url_for('page.dhcp'))
    elif (type == 2): #dns
        respuesta = os.popen("sudo -S systemctl start bind9").read()
        status = os.popen("sudo -S systemctl status bind9| grep 'active' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "active":
            flash("El Servidor inicio CORRECTAMENTE")
        else:
            flash("Error al Iniciar el servicio",'error')
        return redirect(url_for('page.dns'))
    else:
        return redirect(url_for('page.servers'))
    return redirect(url_for('page.servers'))


@page.route('/servers/stop/<int:type>',methods=['GET','POST'])
@login_required
def stop_servers(type):
    names = []
    if (type == 0): #tftp
        respuesta = os.popen("sudo -S systemctl stop tftpd-hpa").read()
        status = os.popen("sudo -S systemctl status tftpd-hpa| grep 'inactive' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "inactive":
            flash("El Servidor detuvo CORRECTAMENTE")
        else:
            flash("Error al detener el servicio",'error')
        
        return redirect(url_for('page.tftp'))
    elif (type == 1): #dhcp
        respuesta = os.popen("sudo -S systemctl stop isc-dhcp-server").read()
        status = os.popen("sudo -S systemctl status isc-dhcp-server| grep 'inactive' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "inactive":
            flash("El Servidor detuvo CORRECTAMENTE")
        else:
            flash("Error al detener el servicio",'error')
        return redirect(url_for('page.dhcp'))
    elif (type == 2): #dns
        respuesta = os.popen("sudo -S systemctl stop bind9").read()
        status = os.popen("sudo -S systemctl status bind9| grep 'inactive' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "inactive":
            flash("El Servidor detuvo CORRECTAMENTE")
        else:
            flash("Error al detener el servicio",'error')
        return redirect(url_for('page.dns'))
    else:
        return redirect(url_for('page.servers'))
    return redirect(url_for('page.servers'))

@page.route('/servers/restart/<int:type>',methods=['GET','POST'])
@login_required
def restart_servers(type):
    names = []
    if (type == 0): #tftp
        respuesta = os.popen("sudo -S systemctl restart tftpd-hpa").read()
        status = os.popen("sudo -S systemctl status tftpd-hpa| grep 'active' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "active":
            flash("El Servidor se reinicio CORRECTAMENTE")
        else:
            flash("Error al reiniciar el servicio",'error')
        
        return redirect(url_for('page.tftp'))
    elif (type == 1): #dhcp
        respuesta = os.popen("sudo -S systemctl restart isc-dhcp-server").read()
        status = os.popen("sudo -S systemctl status isc-dhcp-server| grep 'active' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "active":
            flash("El Servidor se reinicio CORRECTAMENTE")
        else:
            flash("Error al reiniciar el servicio",'error')
        
        return redirect(url_for('page.dhcp'))
    elif (type == 2): #dns
        respuesta = os.popen("sudo -S systemctl restart bind9").read()
        status = os.popen("sudo -S systemctl status bind9| grep 'active' ").read()
        status = status.strip().split(":")
        status = status[1].strip().split(" ")
        status = status[0]
        if status == "active":
            flash("El Servidor se reinicio CORRECTAMENTE")
        else:
            flash("Error al reiniciar el servicio",'error')
        
        return redirect(url_for('page.dns'))
    else:
        return redirect(url_for('page.servers'))
    return redirect(url_for('page.servers'))

@page.route('/servers/status/<int:type>',methods=['GET','POST'])
@login_required
def status_servers(type):
    names = []
    if (type == 0): #tftp
        status = os.popen("sudo -S systemctl status tftpd-hpa| grep 'Active' ").read()
        status = status.strip()
        flash(status)
        return redirect(url_for('page.tftp'))

    elif (type == 1): #dhcp
        status = os.popen("sudo -S systemctl status isc-dhcp-server| grep 'Active' ").read()
        status = status.strip()
        flash(status)
        return redirect(url_for('page.dhcp'))

    elif (type == 2): #dns
        status = os.popen("sudo -S systemctl status bind9| grep 'Active' ").read()
        status = status.strip()
        flash(status)
        return redirect(url_for('page.dns'))
    else:
        return redirect(url_for('page.servers'))
    return redirect(url_for('page.servers'))
















