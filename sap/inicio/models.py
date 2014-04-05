from django.db import models

class TimeStampedModel(models.Model):
    """
    Una clase base abstracta que provee los campos actualizables 
    'creado' y 'modificado'. Los cuales representan el momento 
    de creacion y el momento de actualizacion, respectivamente.
    """
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True