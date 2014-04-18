from django.contrib import admin
from administracion.models import Rol, Permiso, TipoAtributo, Proyecto

admin.site.register(Rol)
admin.site.register(Permiso)
admin.site.register(TipoAtributo)
admin.site.register(Proyecto)