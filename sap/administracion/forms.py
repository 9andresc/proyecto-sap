from django import forms
from django.contrib.auth.models import User
from administracion.models import Rol
from administracion.models import TipoAtributo, TIPO_DATO
from administracion.models import Proyecto, ESTADOS_PROYECTO

class CustomDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d/%m/%Y",))
        super(CustomDateField, self).__init__(*args, **kwargs)

class CrearUsuarioForm(forms.Form):
    """
    Formulario utilizado para la creacion de un usuario.
    """
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
        password_dos = self.cleaned_data['password_dos']
        if 'password_uno' in self.cleaned_data:
            password_uno = self.cleaned_data['password_uno']
        else:
            raise forms.ValidationError('Las claves no coinciden')
        if password_dos == password_uno:
            pass
        else:
            raise forms.ValidationError('Las claves no coinciden')
    
    
        
class ModificarUsuarioForm(forms.Form):
    """
    Formulario utilizado para la modificacion de un usuario.
    """
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(), required=True)
    email = forms.EmailField(label="Email", widget=forms.TextInput(), required=True)
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(), required=True)
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(), required=True)
    direccion = forms.CharField(label="Direccion", widget=forms.TextInput(), required=False)
    telefono = forms.CharField(label="Telefono", widget=forms.TextInput(), required=False)
        
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
    
class CambiarContrasenhaForm(forms.Form):
    password_uno = forms.CharField(label="Contrasenha", required=True)
    password_dos = forms.CharField(label="Confirmar contrasenha", required=True)
    
    def clean_password_dos(self):
        password_dos = self.cleaned_data['password_dos']
        if 'password_uno' in self.cleaned_data:
            password_uno = self.cleaned_data['password_uno']
        else:
            raise forms.ValidationError('Las claves no coinciden')
        if password_dos == password_uno:
            pass
        else:
            raise forms.ValidationError('Las claves no coinciden')
    
        
class CrearRolForm(forms.Form):
    """
    Formulario utilizado para la creacion de un rol.
    """
    nombre = forms.CharField(label="Nombre de rol", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        try:
            rol = Rol.objects.get(nombre=nombre)
        except Rol.DoesNotExist:
            return nombre
        raise forms.ValidationError('Nombre de rol ya registrado')

class ModificarRolForm(forms.Form):
    """
    Formulario utilizado para la modificacion de un rol.
    """
    nombre = forms.CharField(label="Nombre de rol", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
        
    def clean_nombre(self): 
        nombre = self.cleaned_data['nombre'] 
        try: 
            rol = Rol.objects.get(nombre=nombre) 
            if rol.nombre == nombre:
                return nombre 
        except Rol.DoesNotExist:
            return nombre 
        raise forms.ValidationError('Nombre de rol ya registrado')

class CrearTipoAtributoForm(forms.Form):
    """
    Formulario utilizado para la creacion de un tipo atributo.
    """
    nombre = forms.CharField(label="Nombre de tipo atributo", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    tipo_dato = forms.ChoiceField(label="Tipo dato", choices=TIPO_DATO, required=True)
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        try:
            tipo_atributo = TipoAtributo.objects.get(nombre=nombre)
        except TipoAtributo.DoesNotExist:
            return nombre
        raise forms.ValidationError('Nombre de tipo atributo ya registrado')

class ModificarTipoAtributoForm(forms.Form):
    """
    Formulario utilizado para la modificacion de un tipo atributo.
    """
    nombre = forms.CharField(label="Nombre de tipo atributo", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    tipo_dato = forms.ChoiceField(label="Tipo dato", choices=TIPO_DATO, required=False)
        
    def clean_nombre(self): 
        nombre = self.cleaned_data['nombre'] 
        try: 
            tipo_atributo = TipoAtributo.objects.get(nombre=nombre) 
            if tipo_atributo.nombre == nombre:
                return nombre 
        except TipoAtributo.DoesNotExist:
            return nombre 
        raise forms.ValidationError('Nombre de tipo atributo ya registrado')
    
def opcion_lider():
    usuarios = User.objects.all()
    resultado = []
    for usuario in usuarios: 
        if usuario.is_active:
            tupla = (usuario.id, usuario.username)
            resultado.append(tupla)
    return resultado
    
class CrearProyectoForm(forms.Form):
    """
    Formulario utilizado para la creacion de un proyecto.
    """
    nombre = forms.CharField(label="Nombre de proyecto", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    usuario_lider = forms.ChoiceField(label="Lider", choices=(opcion_lider()), required=True)
    presupuesto = forms.FloatField(label="Presupuesto", required=True)
    complejidad = forms.IntegerField(label="Complejidad", required=True)
    fecha_inicio = CustomDateField(required=True)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        try:
            proyecto = Proyecto.objects.get(nombre=nombre)
        except Proyecto.DoesNotExist:
            return nombre
        raise forms.ValidationError('Nombre de proyecto ya registrado')

class ModificarProyectoForm(forms.Form):
    """
    Formulario utilizado para la modificacion de un proyecto.
    """
    nombre = forms.CharField(label="Nombre de proyecto", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    presupuesto = forms.FloatField(label = 'Presupuesto', required=True)
    complejidad = forms.IntegerField(label = 'Complejidad', required=True)
        
    def clean_nombre(self): 
        nombre = self.cleaned_data['nombre'] 
        try: 
            proyecto = Proyecto.objects.get(nombre=nombre) 
            if proyecto.nombre == nombre:
                return nombre 
        except Proyecto.DoesNotExist:
            return nombre 
        raise forms.ValidationError('Nombre de proyecto ya registrado')
