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

ESTADOS_USUARIO = (
    (0, "Activo"),
    (1, "Inactivo"),
)

User.add_to_class('estado', models.IntegerField(max_length=30, choices=ESTADOS_USUARIO, default=1))
User.add_to_class('telefono', models.CharField(max_length=100, blank=True))
User.add_to_class('direccion', models.CharField(max_length=100, blank=True))
User.add_to_class('roles', models.ManyToManyField(Rol, null=True, blank=True))