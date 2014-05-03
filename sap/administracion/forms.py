import datetime
from django import forms
from django.contrib.auth.models import User
from administracion.models import Rol
from administracion.models import TipoAtributo, TIPO_DATO
from administracion.models import Proyecto, ESTADOS_PROYECTO
from administracion.models import Fase
from administracion.models import TipoItem

class CustomDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('input_formats', ("%d/%m/%Y",))
        super(CustomDateField, self).__init__(*args, **kwargs)

class CrearUsuarioForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la creacion de un usuario.
        
        Se especifican todos los atributos del usuario que deben 
        ingresarse estableciendo como required=True, si es indispensable
        completar ese atributo para la creacion del usuario o caso contrarios 
        required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema, ni tampoco el email.
        
        Por ultimo se revisa que los dos campos de contrasenha coincidan.
        
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
        raise forms.ValidationError('Nombre de usuario ya registrado.')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya registrado.')
    
    def clean_password_dos(self):
        password_dos = self.cleaned_data['password_dos']
        if 'password_uno' in self.cleaned_data:
            password_uno = self.cleaned_data['password_uno']
        else:
            raise forms.ValidationError('Las claves no coinciden.')
        if password_dos == password_uno:
            pass
        else:
            raise forms.ValidationError('Las claves no coinciden.')
    
    
        
class ModificarUsuarioForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la modificacion de un usuario.
        
        Se especifican todos los atributos del usuario que deben 
        ingresarse sin posibilidad de dejar el campo vacio estableciendo
        como required=True, caso contrarios required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema, ni tampoco el email.
        
        Por ultimo se revisa que los dos campos de contrasenha coincidan y se procede a reemplazar la contrasenha.

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
        raise forms.ValidationError('Nombre de usuario ya registrado.')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            usuario = User.objects.get(email=email)
            if usuario.email == email:
                return email
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email ya registrado.')
    
class CambiarContrasenhaForm(forms.Form):
    password_uno = forms.CharField(label="Contrasenha", required=True)
    password_dos = forms.CharField(label="Confirmar contrasenha", required=True)
    
    def clean_password_dos(self):
        password_dos = self.cleaned_data['password_dos']
        if 'password_uno' in self.cleaned_data:
            password_uno = self.cleaned_data['password_uno']
        else:
            raise forms.ValidationError('Las claves no coinciden.')
        if password_dos == password_uno:
            pass
        else:
            raise forms.ValidationError('Las claves no coinciden.')
    
        
class CrearRolForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la creacion de un rol.
        
        Se especifican todos los atributos del rol que deben 
        ingresarse estableciendo como required=True, si es indispensable
        completar ese atributo para la creacion del rol o caso contrarios 
        required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
    """
    nombre = forms.CharField(label="Nombre de rol", required=True)
    descripcion = forms.CharField(label="Descripcion", required=False)
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        try:
            rol = Rol.objects.get(nombre=nombre)
        except Rol.DoesNotExist:
            return nombre
        raise forms.ValidationError('Nombre de rol ya registrado.')

class ModificarRolForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la modificacion de un rol.
        
        Se especifican todos los atributos del rol que deben 
        ingresarse sin posibilidad de dejar el campo vacio estableciendo
        como required=True, caso contrarios required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
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
        raise forms.ValidationError('Nombre de rol ya registrado.')

class CrearTipoAtributoForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la creacion de un tipo atributo.
        
        Se especifican todos los atributos del tipo atributo que deben 
        ingresarse estableciendo como required=True, si es indispensable
        completar ese atributo para la creacion del tipo atributo o caso 
        contrario required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
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
        raise forms.ValidationError('Nombre de tipo atributo ya registrado.')

class ModificarTipoAtributoForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la modificacion de un tipo atributo.
        
        Se especifican todos los atributos del tipo atributo que deben 
        ingresarse sin posibilidad de dejar el campo vacio estableciendo
        como required=True, caso contrarios required=False.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
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
        raise forms.ValidationError('Nombre de tipo atributo ya registrado.')
    
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
    ::
    
        Formulario utilizado para la creacion de un proyecto.
        
        Se especifican todos los atributos del proyecto que deben 
        ingresarse estableciendo como required=True, si es indispensable
        completar ese atributo para la creacion del proyecto o caso 
        contrario required=False.
        
        Se utiliza una funcion opcion lider, para listar todos los usuarios 
        registrados y que se pueda elegir a uno como lider del proyecto.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
        Se utiliza una funciona para verificar que la fecha ingresada sea valida.
        
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
        raise forms.ValidationError('Nombre de proyecto ya registrado.')
    
    def clean_complejidad(self):
        complejidad = self.cleaned_data['complejidad']
        if complejidad > 0 and complejidad <= 10:
            return complejidad
        else:
            raise forms.ValidationError('El valor de la complejidad debe estar en el rango [1, 10].')
        
    def clean_presupuesto(self):
        presupuesto = self.cleaned_data['presupuesto']
        if presupuesto >= 0:
            return presupuesto
        else:
            raise forms.ValidationError('El valor del presupuesto debe ser igual o mayor a cero.')
        
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio >= datetime.date.today():
            return fecha_inicio
        else:
            raise forms.ValidationError('La fecha introducida es anterior a la fecha actual. Ingrese una fecha posterior.')

class ModificarProyectoForm(forms.Form):
    """
    ::
    
        Formulario utilizado para la modificacion de un proyecto.
        
        Se especifican todos los atributos del proyecto que deben 
        ingresarse sin posibilidad de dejar el campo vacio estableciendo
        como required=True, caso contrarios required=False.
        
        Se utiliza una funcion opcion lider, para listar todos los usuarios 
        registrados y que se pueda elegir a uno como nuevo lider del proyecto.
        
        Se utilizan funciones para verificar que el nombre no este registrado
        en el sistema.
        
        Se utiliza una funciona para verificar que la fecha ingresada sea valida.
        
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
            if proyecto.nombre == nombre:
                return nombre 
        except Proyecto.DoesNotExist:
            return nombre 
        raise forms.ValidationError('Nombre de proyecto ya registrado.')
    
    def clean_complejidad(self):
        complejidad = self.cleaned_data['complejidad']
        if complejidad > 0 and complejidad <= 10:
            return complejidad
        else:
            raise forms.ValidationError('El valor de la complejidad debe estar en el rango [1, 10].')
        
    def clean_presupuesto(self):
        presupuesto = self.cleaned_data['presupuesto']
        if presupuesto >= 0:
            return presupuesto
        else:
            raise forms.ValidationError('El valor del presupuesto debe ser igual o mayor a cero.')
        
    def clean_fecha_inicio(self):
        nombre = self.cleaned_data['nombre']
        fecha_inicio = self.cleaned_data['fecha_inicio']
        if fecha_inicio >= datetime.date.today() or fecha_inicio == Proyecto.objects.get(nombre=nombre).fecha_inicio:
            return fecha_inicio
        else:
            raise forms.ValidationError('La fecha introducida es distinta a la fecha original o anterior a la fecha actual. Ingrese una fecha valida.')
        
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