from django.db import models
from django.contrib.auth.models import User

class Permiso(models.Model):
    """
    ::
    
        Clase que describe la estructura de cada instancia de un Permiso, los atributos 
        que posee un permiso son:
    
        nombre: nombre del permiso.
    """
    nombre = models.CharField(max_length=50, blank=False)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]

class Rol(models.Model):
    """
    ::
    
        Clase que describe la estructura de cada instancia de un Rol, los atributos 
        que posee un rol son:

        nombre: nombre del rol.
        descripcion: breve descripcion del rol.
        permisos: permisos que posee el rol.
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
    (2, "Texto grande"),
    (3, "Texto chico"),
    (4, "Logico"),
    (5, "Archivo"),
) 

class TipoAtributo(models.Model):
    """
    ::
    
        Clase que describe la estructura de cada instancia de un Tipo atributo, los atributos 
        que posee un tipo atributo son:

        nombre: nombre del tipo atributo.
        tipo de dato: el tipo de dato al que corresponde.
        descripcion: una breve descripcion del tipo atributo.
        num_longitud: longitud de un tipo de dato Numerico.
        num_precision: precision decimal de un tipo de dato Numerico.
        textg_longitud: longitud de un tipo de dato Texto grande.
        textch_longitud: longitud de un tipo de dato Texto chico.
        obligatorio: valor booleano que indica si un atributo debe ser obligatorio o no.
    """
    nombre = models.CharField(max_length=50, blank=False)
    tipo_dato  = models.IntegerField(max_length=30,choices= TIPO_DATO, default=0)
    descripcion = models.TextField(blank=True)
    num_longitud = models.IntegerField(null=True, blank=True)
    num_precision = models.IntegerField(null=True, blank=True)
    textg_longitud = models.IntegerField(null=True, blank=True)
    textch_longitud = models.IntegerField(null=True, blank=True)
    obligatorio = models.BooleanField(default=False, blank=True)
    
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
    ::
    
        Clase que describe la estructura de cada instancia de un Proyecto, los atributos 
        que posee un proyecto son:

        nombre: nombre del proyecto.
        descripcion: una breve descripcion sobre el proyecto.
        fecha de inicio: fecha de inicio del proyecto. 
        estado: estado actual del proyecto.
        presupuesto: presupuesto total del proyecto.
        complejidad: nivel de complejidad del proyecto.
        usuario lider: usuario lider del proyecto.
        usuarios: usuarios que participan en el proyecto.
        comite de cambios: comite encargado de aprobar o rechazar solicitudes de cambio.
        roles: roles asociados al proyecto.
        fases: fases asociadas al proyecto.
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

ESTADOS_USUARIO = (
    (0, "Activo"),
    (1, "Inactivo"),
)

User.add_to_class('estado', models.IntegerField(max_length=30, choices=ESTADOS_USUARIO, default=0))
User.add_to_class('telefono', models.CharField(max_length=100, blank=True))
User.add_to_class('direccion', models.CharField(max_length=100, blank=True))
User.add_to_class('roles', models.ManyToManyField(Rol, null=True, blank=True))
