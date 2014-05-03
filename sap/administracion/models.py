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
    (2, "Texto"),
    (3, "Logico"),
) 

class TipoAtributo(models.Model):
    """
    ::
    
        Clase que describe la estructura de cada instancia de un Tipo atributo, los atributos 
        que posee un tipo atributo son:

        nombre: nombre del tipo atributo.
        tipo de dato: el tipo de dato al que corresponde.
        descripcion: una breve descripcion del tipo atributo.
        valor: valor que posee el tipo atributo.
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

ESTADOS_FASE = (
    (0, "Inactivo"),
    (1, "En curso"),
    (2, "Finalizada"),
)

class Fase(models.Model):
    """
    ::
    
        Clase que describe la estructura de cada instancia de una Fase, los atributos 
        que posee una fase son:

        nombre: nombre de la fase.
        descripcion: una breve descripcion sobre la fase.
        estado: estado actual de la fase.
        fecha de inicio: fecha de inicio de la fase.
        duracion: duracion de la fase.
        roles: roles asociados a la fase.
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
    ::
    
        Clase que describe la estructura de cada instancia de un Tipo de item, los atributos 
        que posee un tipo de item son:

        nombre: nombre del tipo de item.
        descripcion: breve descripcion del tipo de item.
        tipos_atributo: tipos de atributo que posee el tipo de item.
    """
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    tipos_atributo = models.ManyToManyField(TipoAtributo, null=True, blank=True)

    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]

class ValorAtributo(models.Model):
    """
    ::
    
        Clase que describe la relacion entre un tipo de atributo con un tipo de item y un item, los atributos 
        que posee son:

        item: item al que va ligado.
        tipo_item:tipo de item al que va ligado.
        tipo_atributo: tipo de atributo al que va ligado.
        valor_XXX: valor del tipo de atributo, que puede ser Fecha, Numerico, Logico o Texto.
    """
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

User.add_to_class('estado', models.IntegerField(max_length=30, choices=ESTADOS_USUARIO, default=0))
User.add_to_class('telefono', models.CharField(max_length=100, blank=True))
User.add_to_class('direccion', models.CharField(max_length=100, blank=True))
User.add_to_class('roles', models.ManyToManyField(Rol, null=True, blank=True))
