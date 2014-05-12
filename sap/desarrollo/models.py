from django.db import models
from administracion.models import Rol, Proyecto, TipoAtributo

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
        num_secuencia: define el orden numerico de la fase dentro de un proyecto.
        fecha de inicio: fecha de inicio de la fase.
        duracion: duracion de la fase.
        roles: roles asociados a la fase.
        proyecto: el proyecto al cual pertenece la fase.
    """
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)
    estado = models.IntegerField(max_length=1, choices=ESTADOS_FASE, default=0)
    num_secuencia = models.IntegerField(max_length=30, null=True)
    fecha_inicio = models.DateField(null=True)
    duracion = models.IntegerField(null=True, blank=True, default=0)
    roles = models.ManyToManyField(Rol, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, related_name="fases", null=True, blank=True)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["num_secuencia"]

class TipoItem(models.Model):
    """
    ::
    
        Clase que describe la estructura de cada instancia de un Tipo de item, los atributos 
        que posee un tipo de item son:

        nombre: nombre del tipo de item.
        descripcion: breve descripcion del tipo de item.
        tipos_atributo: tipos de atributo que posee el tipo de item.
        fase: la fase a la cual pertenece el tipo de item.
    """
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    tipos_atributo = models.ManyToManyField(TipoAtributo, null=True, blank=True)
    fase = models.ForeignKey(Fase, related_name="tipos_item", null=True, blank=True)

    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]

class Item(models.Model):
    """
    ::
    
        Clase que describe la estructura de cada instancia de un Item, los atributos 
        que posee un Item son:

        nombre: nombre del item.
        descripcion: una breve descripcion sobre el item.
        costo_*: costo del item.
        complejidad: complejidad respectiva del item.
        estado: estado actual del item.
        fase: fase en la que esta el item.
        tipo_item: tipo de item vinculado al item.
        padre: es item padre/antecesor del item.
        tipo_relacion: indica que tipo de relacion tiene el item con el padre/antecesor (Hijo o Sucesor).
    """
    ESTADOS_ITEM = (
        (0, "En construccion"),
        (1, "Aprobado"),
        (2, "Bloqueado"),
        (3, "En revision"),
    )
    TIPOS_RELACION = (
        (0, "Hijo"),
        (1, "Sucesor"),
    )
    
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    costo_monetario = models.FloatField(null=True, blank=True, default=0)
    costo_temporal = models.FloatField(null=True, blank=True, default=0)
    complejidad = models.IntegerField(null=True, blank=True, default=0)
    estado = models.IntegerField(max_length=1, choices=ESTADOS_ITEM, default=0)
    fase = models.ForeignKey(Fase, related_name="items", null=True, blank=True)
    tipo_item = models.ForeignKey(TipoItem, related_name="items", null=True, blank=True)
    adan = models.IntegerField(null=True)
    cain = models.IntegerField(null=True)
    padre = models.ForeignKey('desarrollo.Item', related_name="relaciones", null=True, blank=True)
    tipo_relacion = models.IntegerField(max_length=1, choices=TIPOS_RELACION, null=True)
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]
        
class VersionItem(models.Model):
    """
    ::
    
        Clase que describe la estructura de cada instancia de una VersionItem, los atributos 
        que posee una VersionItem son:

        version: numero de serie de la version del item.
        id_item: identificador del item.
        nombre: nombre del item.
        descripcion: una breve descripcion sobre el item.
        costo_*: costo del item.
        complejidad: complejidad respectiva del item.
        estado: estado actual del item.
        fase: fase en la que esta el item.
        tipo_item: tipo de item vinculado al item.
        padre: el padre (o antecesor) del item.
        tipo_relacion: indica que clase de relacion se mantiene con el item padre o antecesor.
        fecha_version: fecha de la creacion de la version.
    """
    version = models.FloatField(null=False, default=1.0)
    id_item = models.IntegerField(null=False)
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    costo_monetario = models.FloatField(null=True, blank=True, default=0)
    costo_temporal = models.FloatField(null=True, blank=True, default=0)
    complejidad = models.IntegerField(null=True, blank=True, default=0)
    estado = models.IntegerField(max_length=30, choices=Item.ESTADOS_ITEM, default=0)
    fase = models.ForeignKey(Fase, null=True, blank=True)
    tipo_item = models.ForeignKey(TipoItem, null=True, blank=True)
    adan = models.IntegerField(null=True)
    cain = models.IntegerField(null=True)
    padre = models.IntegerField(null=True)
    tipo_relacion = models.IntegerField(max_length=1, choices=Item.TIPOS_RELACION, null=True)
    fecha_version = models.DateTimeField(null=True)
    
    class Meta:
        ordering = ["id_item", "version"]
        
class ValorAtributo(models.Model):
    """
    ::
    
        Clase que describe la relacion entre un tipo de atributo con un tipo de item y un item, los atributos 
        que posee son:

        item: item al que va ligado.
        tipo_item:tipo de item al que va ligado.
        tipo_atributo: tipo de atributo al que va ligado.
        valor_*: valor del tipo de atributo, que puede ser Fecha, Numerico, Logico, Texto grande o Texto chico.
    """
    item = models.ForeignKey(Item, related_name="valores", null=True, blank=True)
    tipo_item = models.ForeignKey(TipoItem, null=True, blank=True)
    tipo_atributo = models.ForeignKey(TipoAtributo, null=True, blank=True)
    valor_fecha = models.DateField(null=True)
    valor_numerico = models.DecimalField(max_digits=30, decimal_places=10, null=True)
    valor_logico = models.BooleanField(default=True)
    valor_texto_grande = models.TextField(blank=True)
    valor_texto_chico = models.CharField(max_length=50, blank=True)