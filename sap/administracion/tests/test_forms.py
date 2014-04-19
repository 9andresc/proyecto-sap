"""
from django.test import TestCase
from administracion.forms import CrearUsuarioForm, ModificarUsuarioForm, CambiarContrasenhaForm, CrearRolForm, ModificarRolForm, CrearTipoAtributoForm, ModificarTipoAtributoForm

class CrearUsuarioFormTest(TestCase):
    def test_formulario_valido(self):
        data = {'username': 'rodrigo', 'email': 'rodrigo@gmail.com', 'password_uno': 'santos', 'password_dos': 'santos', 'first_name': 'Rodrigo', 'last_name': 'Santos',}
        form = CrearUsuarioForm(data=data)
        self.assertTrue(form.is_valid(), "El formulario de creacion de usuario no resulto valido.")
        
    def test_formulario_invalido(self):
        data = {'username': 'rodrigo', 'email': 'rodrigo@gmail.com', 'password_uno': 'santosss', 'password_dos': 'santos', 'first_name': 'Rodrigo', 'last_name': 'Santos',}
        form = CrearUsuarioForm(data=data)
        self.assertFalse(form.is_valid(), "El formulario de creacion de usuario resulto valido.")
        
class ModificarUsuarioFormTest(TestCase):
    def test_formulario_valido(self):
        data = {'username': 'rodrigo', 'email': 'rodrigo@gmail.com', 'password_uno': 'santos', 'password_dos': 'santos', 'first_name': 'Rodrigo', 'last_name': 'Santos',}
        form = ModificarUsuarioForm(data=data)
        self.assertTrue(form.is_valid(), "El formulario de modificacion de usuario no resulto valido.")
        
    def test_formulario_invalido(self):
        data = {'username': 'rodrigo', 'email': 'rodrigogmail.com', 'first_name': 'Rodrigo', 'last_name': 'Santos',}
        form = ModificarUsuarioForm(data=data)
        self.assertFalse(form.is_valid(), "El formulario de modificacion de usuario resulto valido.")
        
class CambiarContrasenhaFormTest(TestCase):
    def test_formulario_valido(self):
        data = {'password_uno': 'santos', 'password_dos': 'santos'}
        form = CambiarContrasenhaForm(data=data)
        self.assertTrue(form.is_valid(), "El formulario de cambio de contrasenha no resulto valido.")
        
    def test_formulario_invalido(self):
        data = {'password_uno': 'santoss', 'password_dos': 'santos'}
        form = CambiarContrasenhaForm(data=data)
        self.assertFalse(form.is_valid(), "El formulario de cambio de contrasenha resulto valido.")
        
class CrearRolFormTest(TestCase):
    fixtures = ['roles_testdata.json']
    
    def test_formulario_valido(self):
        data = {'nombre': 'Rol', 'descripcion': 'Descripcion de un rol.'}
        form = CrearRolForm(data=data)
        self.assertTrue(form.is_valid(), "El formulario de creacion de rol no resulto valido.")
        
    def test_formulario_invalido(self):
        data = {'nombre': 'Administrador', 'descripcion': 'Posee todos los permisos del modulo de administracion.'}
        form = CrearRolForm(data=data)
        self.assertFalse(form.is_valid(), "El formulario de creacion de rol resulto valido.")
        
class ModificarRolFormTest(TestCase):
    fixtures = ['roles_testdata.json']
    
    def test_formulario_valido(self):
        data = {'nombre': 'Rol', 'descripcion': 'Descripcion de un rol.'}
        form = ModificarRolForm(data=data)
        self.assertTrue(form.is_valid(), "El formulario de modificacion de rol no resulto valido.")
        
    def test_formulario_invalido(self):
        data = {'nombre': 'Administrador', 'descripcion': 'Posee todos los permisos del modulo de administracion.'}
        form = ModificarRolForm(data=data)
        self.assertFalse(form.is_valid(), "El formulario de modificacion de rol resulto valido.")
        
class CrearTipoAtributoFormTest(TestCase):
    def test_formulario_valido(self):
        data = {'nombre': 'Fecha de creacion', 'descripcion': 'Descripcion de un tipo de atributo.'}
        form = CrearTipoAtributoForm(data=data)
        self.assertTrue(form.is_valid(), "El formulario de creacion de tipo de atributo no resulto valido.")
        
    def test_formulario_invalido(self):
        data = {'nombre': 'Fecha de vencimiento', 'descripcion': 'Describe la fecha de vencimiento de un item.'}
        form = CrearTipoAtributoForm(data=data)
        self.assertFalse(form.is_valid(), "El formulario de creacion de tipo de atributo resulto valido.")
        
class ModificarTipoAtributoFormTest(TestCase):
    def test_formulario_valido(self):
        data = {'nombre': 'Fecha de creacion', 'descripcion': 'Descripcion de un tipo de atributo.'}
        form = ModificarTipoAtributoForm(data=data)
        self.assertTrue(form.is_valid(), "El formulario de modificacion de tipo de atributo no resulto valido.")
        
    def test_formulario_invalido(self):
        data = {'nombre': 'Fecha de vencimiento', 'descripcion': 'Describe la fecha de vencimiento de un item.'}
        form = ModificarTipoAtributoForm(data=data)
        self.assertFalse(form.is_valid(), "El formulario de modificacion de tipo de atributo resulto valido.")
"""