from django import forms
from django.contrib.auth.models import User

class CrearUsuarioForm(forms.Form):
    """
    LALALALA.
    """
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(), required=True)
    email = forms.EmailField(label="Email", widget=forms.TextInput(), required=True)
    password_uno = forms.CharField(label="Contrasenha", widget=forms.PasswordInput(render_value=False), required=True)
    password_dos = forms.CharField(label="Confirmar contrasenha", widget=forms.PasswordInput(render_value=False), required=True)
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    direccion = forms.CharField(label="Direccion", widget=forms.TextInput(), required=False)
    telefono = forms.CharField(label="Telefono", widget=forms.TextInput(), required=False)
    
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
    """
    LALALALALA.
    """
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(), required=True)
    email = forms.EmailField(label="Email", widget=forms.TextInput(), required=True)
    password_uno = forms.CharField(label="Contrasenha", widget=forms.PasswordInput(render_value=False), required=True)
    password_dos = forms.CharField(label="Confirmar contrasenha", widget=forms.PasswordInput(render_value=False), required=True)
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    direccion = forms.CharField(label="Direccion", widget=forms.TextInput(), required=False)
    telefono = forms.CharField(label="Telefono", widget=forms.TextInput(), required=False)
    
    def clean_password_dos(self):
        password_uno = self.cleaned_data['password_uno']
        password_dos = self.cleaned_data['password_dos']
        if password_uno == password_dos:
            pass
        else:
            raise forms.ValidationError('Las claves no coinciden')
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            usuario = User.objects.get(username=username)
            if usuario.username == username:
                return username
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Nombre de usuario ya registrado')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            usuario = User.objects.get(email=email)
            if usuario.email == email:
                return email
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya registrado')
        
        