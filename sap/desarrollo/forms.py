import datetime
from django import forms
from desarrollo.models import Fase, TipoItem, LineaBase

class CustomDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d/%m/%Y",))
        super(CustomDateField, self).__init__(*args, **kwargs)

class CrearFaseForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la creacion de una fase.
        
        Se especifican todos los atributos de la fase que deben 
        ingresarse estableciendo como required=True, si es indispensable
        completar ese atributo para la creacion de la fase o caso 
        contrario required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
        Se utiliza una funciona para verificar que la fecha ingresada sea valida.
        
    """
    nombre = forms.CharField(label="Nombre de fase", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    duracion = forms.IntegerField(label="Duracion", required=True)
    fecha_inicio = CustomDateField(required=True)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        try:
            fase = Fase.objects.get(nombre=nombre)
        except Fase.DoesNotExist:
            return nombre
        raise forms.ValidationError('Nombre de fase ya registrado.')
        
    def clean_duracion(self):
        duracion = self.cleaned_data['duracion']
        if duracion > 0:
            return duracion
        else:
            raise forms.ValidationError('El valor de la duracion (en semanas) debe ser mayor a cero.')
        
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio >= datetime.date.today():
            return fecha_inicio
        else:
            raise forms.ValidationError('La fecha introducida es anterior a la fecha actual. Ingrese una fecha posterior.')
        
class ModificarFaseForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la modificacion de una fase.
        
        Se especifican todos los atributos de la fase que deben 
        ingresarse sin posibilidad de dejar el campo vacio estableciendo
        como required=True, caso contrarios required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
        Se utiliza una funciona para verificar que la fecha ingresada sea valida.
        
    """
    nombre = forms.CharField(label="Nombre de fase", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    duracion = forms.IntegerField(label="Duracion", required=True)
    fecha_inicio = CustomDateField(required=True)

    def clean_nombre(self): 
        nombre = self.cleaned_data['nombre'] 
        try: 
            fase = Fase.objects.get(nombre=nombre) 
            if fase.nombre == nombre:
                return nombre 
        except Fase.DoesNotExist:
            return nombre 
        raise forms.ValidationError('Nombre de fase ya registrado.')
        
    def clean_duracion(self):
        duracion = self.cleaned_data['duracion']
        if duracion > 0:
            return duracion
        else:
            raise forms.ValidationError('El valor de la duracion (en semanas) debe ser mayor a cero.')
        
    def clean_fecha_inicio(self):
        nombre = self.cleaned_data['nombre']
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio >= datetime.date.today() or fecha_inicio == Fase.objects.get(nombre=nombre).fecha_inicio:
            return fecha_inicio
        else:
            raise forms.ValidationError('La fecha introducida es distinta a la fecha original o anterior a la fecha actual. Ingrese una fecha valida.')

class CrearTipoItemForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la creacion de un tipo de item.
        
        Se especifican todos los atributos del tipo de item que deben 
        ingresarse estableciendo como required=True, si es indispensable
        completar ese atributo para la creacion del tipo de item o caso 
        contrario required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
    """
    nombre = forms.CharField(label="Nombre de tipo de item", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
  
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        try:
            tipo_item = TipoItem.objects.get(nombre=nombre)
        except TipoItem.DoesNotExist:
            return nombre
        raise forms.ValidationError('Nombre de tipo de item ya registrado.')  
    
class ModificarTipoItemForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la modificacion de un tipo de item.
        
        Se especifican todos los atributos del tipo de item que deben 
        ingresarse sin posibilidad de dejar el campo vacio estableciendo
        como required=True, caso contrarios required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
    """
    nombre = forms.CharField(label="Nombre de tipo de item", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)

    def clean_nombre(self): 
        nombre = self.cleaned_data['nombre'] 
        try: 
            tipo_item = TipoItem.objects.get(nombre=nombre) 
            if tipo_item.nombre == nombre:
                return nombre 
        except TipoItem.DoesNotExist:
            return nombre 
        raise forms.ValidationError('Nombre de tipo de item ya registrado.')

class CrearItemForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la creacion de un item.
        
        Se especifican todos los atributos del item que deben 
        ingresarse estableciendo como required=True, si es indispensable
        completar ese atributo para la creacion del item o caso 
        contrario required=False.
        
        Se verifica mediante una funcion que el valor de la complejidad sea valido.
        
        Se verifica mediante una funcion que el valor del costo sea valido.
    """
    nombre = forms.CharField(label="Nombre de item", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    complejidad = forms.IntegerField(label="Complejidad", required=True)
    costo_monetario = forms.FloatField(label="Costo monetario", required=True)
    costo_temporal = forms.FloatField(label="Costo temporal", required=True)
    
    def clean_complejidad(self):
        complejidad = self.cleaned_data['complejidad']
        if complejidad > 0 and complejidad <= 10:
            return complejidad
        else:
            raise forms.ValidationError('El valor de la complejidad debe estar en el rango [1, 10].')
        
    def clean_costo_monetario(self):
        costo_monetario = self.cleaned_data['costo_monetario']
        if costo_monetario >= 0:
            return costo_monetario
        else:
            raise forms.ValidationError('El valor del costo monetario debe ser igual o mayor a cero.')
        
    def clean_costo_temporal(self):
        costo_temporal = self.cleaned_data['costo_temporal']
        if costo_temporal >= 0:
            return costo_temporal
        else:
            raise forms.ValidationError('El valor del costo temporal debe ser igual o mayor a cero.')
        
class ModificarItemForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la modificacion de un item.
        
        Se especifican todos los atributos del item que deben 
        ingresarse sin posibilidad de dejar el campo vacio estableciendo
        como required=True, caso contrarios required=False.
        
        Se verifica mediante una funcion que el valor de la complejidad sea valido.
        
        Se verifica mediante una funcion que el valor del costo sea valido.
    """
    nombre = forms.CharField(label="Nombre de item", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    complejidad = forms.IntegerField(label="Complejidad", required=True)
    costo_monetario = forms.FloatField(label="Costo monetario", required=True)
    costo_temporal = forms.FloatField(label="Costo temporal", required=True)
    
    def clean_complejidad(self):
        complejidad = self.cleaned_data['complejidad']
        if complejidad > 0 and complejidad <= 10:
            return complejidad
        else:
            raise forms.ValidationError('El valor de la complejidad debe estar en el rango [1, 10].')
        
    def clean_costo_monetario(self):
        costo_monetario = self.cleaned_data['costo_monetario']
        if costo_monetario >= 0:
            return costo_monetario
        else:
            raise forms.ValidationError('El valor del costo monetario debe ser igual o mayor a cero.')
        
    def clean_costo_temporal(self):
        costo_temporal = self.cleaned_data['costo_temporal']
        if costo_temporal >= 0:
            return costo_temporal
        else:
            raise forms.ValidationError('El valor del costo temporal debe ser igual o mayor a cero.')
        
class CrearLineaBaseForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la creacion de una linea base.
        
        Se especifican todos los atributos de la linea base que deben 
        ingresarse estableciendo como required=True, si es indispensable
        completar ese atributo para la creacion de la linea base o caso 
        contrario required=False.
    """
    nombre = forms.CharField(label="Nombre de la linea base", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
