from django import forms
from django.contrib.auth.models import User

class CrearUsuarioForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", required=True)
    email = forms.EmailField(label="Email", required=True)
    password_uno = forms.CharField(label="Contrasenha", required=True)
    password_dos = forms.CharField(label="Confirmar contrasenha", required=True)
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellido", required=True)
    direccion = forms.CharField(label="Direccion", required=False)
    telefono = forms.CharField(label="Telefono", required=False)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Nombre de usuario ya registrado')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya registrado')
    
    def clean_password_dos(self):
        password_uno = self.cleaned_data['password_uno']
        password_dos = self.cleaned_data['password_dos']
        if password_uno == password_dos:
            pass
        else:
            raise forms.ValidationError('Las claves no coinciden')
        
class ModificarUsuarioForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", required=True)
    email = forms.EmailField(label="Email", required=True)
    password_uno = forms.CharField(label="Contrasenha", required=True)
    password_dos = forms.CharField(label="Confirmar contrasenha", required=True)
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellido", required=True)
    direccion = forms.CharField(label="Direccion", required=False)
    telefono = forms.CharField(label="Telefono", required=False)
    
    def clean_password_dos(self):
        password_uno = self.cleaned_data['password_uno']
        password_dos = self.cleaned_data['password_dos']
        if password_uno == password_dos:
            pass
        else:
            raise forms.ValidationError('Las claves no coinciden')