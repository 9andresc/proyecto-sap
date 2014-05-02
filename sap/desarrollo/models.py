from django.db import models
from simple_history.models import HistoricalRecords
from administracion.models import Fase
from administracion.models import TipoItem

ESTADOS_ITEM = (
    (0, "En construccion"),
    (1, "Aprobado"),
    (2, "Bloqueado"),
    (3, "En revision"),
    (4, "Eliminado"),
)

def content_file_name(instance, filename):
    return '/'.join(['content', instance.nombre, filename])

class Item(models.Model):
    
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.TextField(blank=True)
    costo = models.FloatField(null=True, blank=True, default=0)
    complejidad = models.IntegerField(null=True, blank=True, default=0)
    estado = models.IntegerField(max_length=30, choices=ESTADOS_ITEM, default=0)
    archivos = models.FileField(upload_to=content_file_name)
    fase = models.ForeignKey(Fase, related_name="items", null=True, blank=True)
    tipo_item = models.ForeignKey(TipoItem, related_name="items", null=True, blank=True)
    
    history = HistoricalRecords()
    
    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]