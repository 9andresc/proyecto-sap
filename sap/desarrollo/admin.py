from django.contrib import admin
from desarrollo.models import Item, Fase, TipoItem, LineaBase, SolicitudCambio

admin.site.register(Item)
admin.site.register(Fase)
admin.site.register(TipoItem)
admin.site.register(LineaBase)
admin.site.register(SolicitudCambio)