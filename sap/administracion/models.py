from django.db import models
from django.contrib.auth.models import User

class Permiso(models.Model):
    nombre = models.CharField(max_length=50, blank=False)
    
    def __unicode__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    permisos = models.ManyToManyField(Permiso, blank=False)
    
    def __unicode__(self):
        return self.nombre

TIPO_DATO = (
    (0, "Numerico"),
    (1, "Fecha"),
    (2, "Texto"),
    (3, "Logico"),
) 

class TipoAtributo(models.Model):
    nombre = models.CharField(max_length=50, blank=False)
    tipo_dato  = models.IntegerField(max_length=30,choices= TIPO_DATO, default=1)
    descripcion = models.TextField(blank=True)
    valor = models.CharField(max_length=50, blank=True)
    
    
    def __unicode__(self):
        return self.nombre
    
   

ESTADOS_USUARIO = (
    (0, "Activo"),
    (1, "Inactivo"),
)


def url_foto(self, filename):
    """
    Define y retorna la ruta de una foto adjuntada a un usuario.
    """
    ruta = "images/%s/%s"%(self.user.username, filename)
    return ruta

User.add_to_class('estado', models.IntegerField(max_length=30, choices=ESTADOS_USUARIO, default=1))
User.add_to_class('telefono', models.CharField(max_length=100, blank=True))
User.add_to_class('direccion', models.CharField(max_length=100, blank=True))
User.add_to_class('url_foto', url_foto)
User.add_to_class('foto', models.ImageField(upload_to=url_foto, blank=True, null=True))
User.add_to_class('roles', models.ManyToManyField(Rol, null=True, blank=True))