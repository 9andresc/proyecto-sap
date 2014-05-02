from django.db import models
from django.contrib.auth.models import User

class Permiso(models.Model):
    """
    Clase que especifica los atributos de los Permisos.
    """
    nombre = models.CharField(max_length=50, blank=False)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]

class Rol(models.Model):
    """
    Clase que especifica los atributos de los Roles.
    """
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    permisos = models.ManyToManyField(Permiso, blank=False)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]

TIPO_DATO = (
    (0, "Numerico"),
    (1, "Fecha"),
    (2, "Texto"),
    (3, "Logico"),
) 

class TipoAtributo(models.Model):
    """
    Clase que especifica los atributos de los Tipos atributo.
    """
    nombre = models.CharField(max_length=50, blank=False)
    tipo_dato  = models.IntegerField(max_length=30,choices= TIPO_DATO, default=0)
    descripcion = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]
    
ESTADOS_PROYECTO = (
    (0, "Inactivo"),
    (1, "En Curso"),
    (2, "Finalizado"),
)

class Proyecto(models.Model):
    """
    Clase que especifica los atributos de los Proyectos.
    """
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    estado = models.IntegerField(max_length=30, choices=ESTADOS_PROYECTO, default=0)
    presupuesto = models.FloatField(null=True, blank=True, default=0)
    complejidad = models.IntegerField(null=True, blank=True, default=0)
    usuario_lider = models.ForeignKey(User, null=True, blank=True)
    usuarios = models.ManyToManyField(User, related_name='usuarios_proyecto', blank=True)
    comite_de_cambios = models.ManyToManyField(User, related_name='comite_de_cambios_proyecto', blank=True)
    roles = models.ManyToManyField(Rol, related_name='roles_proyecto', null=True, blank=True)
  
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]

ESTADOS_FASE = (
    (0, "Inactivo"),
    (1, "En curso"),
    (2, "Finalizada"),
)

class Fase(models.Model):
    """
    Clase que especifica los atributos de las Fases.
    """
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)
    estado = models.IntegerField(max_length=30, choices=ESTADOS_FASE, default=0)
    fecha_inicio = models.DateField(null=True)
    duracion = models.IntegerField(null=True, blank=True, default=0)
    roles = models.ManyToManyField(Rol, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, related_name="fases", null=True, blank=True)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]
        
class TipoItem(models.Model):
    """
    Clase que especifica los atributos de los Tipos item
    """
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    tipos_atributo = models.ManyToManyField(TipoAtributo, null=True, blank=True)

    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]

class ValorAtributo(models.Model):
    item = models.ForeignKey('desarrollo.Item', related_name="valores", null=True, blank=True)
    tipo_item = models.ForeignKey(TipoItem, null=True, blank=True)
    tipo_atributo = models.ForeignKey(TipoAtributo, null=True, blank=True)
    valor_fecha = models.DateField(null=True)
    valor_numerico = models.DecimalField(max_digits=30, decimal_places=10, null=True)
    valor_logico = models.NullBooleanField()
    valor_texto = models.CharField(max_length=300, blank=True)

ESTADOS_USUARIO = (
    (0, "Activo"),
    (1, "Inactivo"),
)

User.add_to_class('estado', models.IntegerField(max_length=30, choices=ESTADOS_USUARIO, default=1))
User.add_to_class('telefono', models.CharField(max_length=100, blank=True))
User.add_to_class('direccion', models.CharField(max_length=100, blank=True))
User.add_to_class('roles', models.ManyToManyField(Rol, null=True, blank=True))