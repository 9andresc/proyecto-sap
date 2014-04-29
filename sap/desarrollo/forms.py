from django import forms

class CrearItemForm(forms.Form):

    nombre = forms.CharField(label="Nombre de item", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    complejidad = forms.IntegerField(label="Complejidad", required=True)
    costo = forms.FloatField(label="Costo", required=True)
    
    def clean_complejidad(self):
        complejidad = self.cleaned_data['complejidad']
        if complejidad > 0 and complejidad <= 10:
            return complejidad
        else:
            raise forms.ValidationError('El valor de la complejidad debe estar en el rango [1, 10].')
        
    def clean_costo(self):
        costo = self.cleaned_data['costo']
        if costo >= 0:
            return costo
        else:
            raise forms.ValidationError('El valor del costo debe ser igual o mayor a cero.')
        
class ModificarItemForm(forms.Form):

    nombre = forms.CharField(label="Nombre de item", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    complejidad = forms.IntegerField(label="Complejidad", required=True)
    costo = forms.FloatField(label="Costo", required=True)
    
    def clean_complejidad(self):
        complejidad = self.cleaned_data['complejidad']
        if complejidad > 0 and complejidad <= 10:
            return complejidad
        else:
            raise forms.ValidationError('El valor de la complejidad debe estar en el rango [1, 10].')
        
    def clean_costo(self):
        costo = self.cleaned_data['costo']
        if costo >= 0:
            return costo
        else:
            raise forms.ValidationError('El valor del costo debe ser igual o mayor a cero.')