from wtforms import Form, HiddenField
from wtforms import validators
from wtforms import StringField, PasswordField,BooleanField,TextAreaField
from wtforms.fields.html5 import EmailField
from .models import User,Task

def codi_validator(form,field):
    if field.data == 'codi' or field.data == 'Codi':
        raise validators.ValidationError('El username codi no es permitido')
def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo los humanos pueden completar el registro!')
class LoginForm(Form):
    username = StringField('Username',[
        validators.length(min=4,max=50,message="EL username esta fuera de rango")
        ])
    password = PasswordField('Password',[validators.Required("El password es requerido")])
    
    
class RegisterForm(Form):
    honeypot = HiddenField("", [ length_honeypot] )
    username = StringField('Username',[codi_validator, validators.length(min=4,max=50)])
    email = EmailField('Correo', [validators.length(min = 6,max = 100),
                                  validators.Required(message="El email es requerido"),
                                  validators.Email(message =" Ingrese un email valido ")])
    password = PasswordField('Password',[
        validators.Required("El password es requerido"),
        validators.EqualTo('confirm_password',message="La contraseña no coincide")
    ])
    confirm_password = PasswordField("Confirma el password")
    accept = BooleanField("Acepto terminos y condiciones",[
                          validators.DataRequired()])
    def validate_username(self,username):
        if User.get_by_username(username.data):
            raise validators.ValidationError("El username ya esta en uso")
        
    def validate_email(self,email):
        if User.get_by_email(email.data):
            raise validators.ValidationError("El email ya esta en uso")
    
class TaskForm(Form):
    title = StringField('Titulo',[
        validators.length(min=4,max=50,message='Titulo fuera de rango'),
        validators.DataRequired(message='El titulo es requerido')
        ])
    description = TextAreaField("Descripcion",[
        validators.DataRequired(message='La descripcion es requerida'),
        
    ],render_kw={'rows':5})

class Dhcp_Sub(Form):
    ip_subnet = StringField("IP de Subnet",[
        validators.length(min=7,max=16,message='IP invalida'),
        validators.DataRequired(message='la Ip de subnet es requerida')
    ])

    mask = StringField("Mascara de subred",[
        validators.length(min=7,max=16,message='Mascara invalida'),
        validators.DataRequired(message='la Mascara de subnet es requerida')
    ])

    range_down = StringField("IP de rango inferior",[
        validators.length(min=7,max=16,message='IP invalida'),
        validators.DataRequired(message='la Ip de rango inferior es requerida')
    ])

    range_up = StringField("IP de rango superior",[
        validators.length(min=7,max=16,message='IP invalida'),
        validators.DataRequired(message='la Ip de rango superior es requerida')
    ])

    ip_router = StringField("IP de Gateway",[
        validators.length(min=7,max=16,message='IP invalida'),
        validators.DataRequired(message='la Ip de gateway es requerida')
    ])

    ip_broadcast = StringField("IP de Broadcast",[
        validators.length(min=7,max=16,message='IP invalida'),
        validators.DataRequired(message='la Ip de broadcast es requerida')
    ])

class DHCP_PCstatic(Form):
    Nombre = StringField("Nickname de la PC",[
        validators.length(min=2,max=16,message='nickname invalido'),
        validators.DataRequired(message='el nickname es requerido')
    ])

    MAC = StringField("MAC de la PC",[
        validators.length(min=16,max=18,message='MAC invalida'),
        validators.DataRequired(message='la MAC es necesaria')
    ])

    ip_static = StringField("IP a asignar",[
        validators.length(min=7,max=16,message='IP invalida'),
        validators.DataRequired(message='la Ip es requerida')
    ])

    ip_router = StringField("IP de Gateway",[
        validators.length(min=7,max=16,message='IP invalida'),
        validators.DataRequired(message='la Ip de gateway es requerida')
    ])

    mask = StringField("Mascara de subred",[
        validators.length(min=7,max=16,message='Mascara invalida'),
        validators.DataRequired(message='la Mascara de subnet es requerida')
    ])
class IP_trusted(Form):
    ip = StringField("IP a guardar",[
        validators.length(min=7,max=16,message='IP invalida'),
        validators.DataRequired(message='la Ip es requerida')
    ])
class DNS_zonas(Form):
    dominio = StringField("Dominio",[
        validators.DataRequired(message='El dominio es requerido')
    ])
    