import datetime
from django import forms
from desarrollo.models import Fase, TipoItem, LineaBase

class CustomDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d/%m/%Y",))
        super(CustomDateField, self).__init__(*args, **kwargs)

class CrearSolicitudForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la creacion de una solicitud.
        
        Se verifica que la descripcion de la solicitud no sobrepase el 
        limite establecido por el modelo. Ademas, se verifica si se ha 
        ingresado alguna descripcion puesto que es obligatoria.
        
    """
    ACCIONES = (
        (1, "Modificar item"),
        (2, "Eliminar item"),
        (3, "Agregar relacion a item"),
        (4, "Quitar relacion de item"),
        (5, "Reversionar item"),
    )
    descripcion = forms.CharField(label="Descripcion", required=True, max_length=250, error_messages={'max_length':'Longitud maxima 250'})
    accion = forms.ChoiceField(label="Accion", choices=ACCIONES, required=True)

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
    nombre = forms.CharField(label="Nombre de tipo de item", required=True, max_length=20, error_messages={'max_length': 'Longitud maxima 20'})
    descripcion = forms.CharField(label="Descripcion", required=False, max_length=300, error_messages={'max_length':'Longitud maxima 300'})
  
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
    nombre = forms.CharField(label="Nombre de tipo de item", required=True, max_length=20, error_messages={'max_length': 'Longitud maxima 20'})
    descripcion = forms.CharField(label="Descripcion", required=False, max_length=300, error_messages={'max_length':'Longitud maxima 300'})

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
    nombre = forms.CharField(label="Nombre de item", required=True, max_length=50, error_messages={'max_length': 'Longitud maxima 50'})
    descripcion = forms.CharField(label="Descripcion", required=False, max_length=300, error_messages={'max_length':'Longitud maxima 300'})
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
    nombre = forms.CharField(label="Nombre de item", required=True, max_length=50, error_messages={'max_length': 'Longitud maxima 50'})
    descripcion = forms.CharField(label="Descripcion", required=False, max_length=300, error_messages={'max_length':'Longitud maxima 300'})
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
    nombre = forms.CharField(label="Nombre de la linea base", required=True, max_length=50, error_messages={'max_length': 'Longitud maxima 50'})
    descripcion = forms.CharField(label="Descripcion", required=False, max_length=300, error_messages={'max_length':'Longitud maxima 300'})
