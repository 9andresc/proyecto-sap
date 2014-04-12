from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from administracion.models import Rol, TipoAtributo
from administracion.views import gestion_usuarios_view, crear_usuario_view, modificar_usuario_view, eliminar_usuario_view, roles_usuario_view, agregar_rol_view, confirmacion_agregar_rol_view, quitar_rol_view
from administracion.views import gestion_roles_view, crear_rol_view, modificar_rol_view, eliminar_rol_view, permisos_rol_view, agregar_permiso_view, confirmacion_agregar_permiso_view, quitar_permiso_view
from administracion.views import gestion_tipos_atributo_view, crear_tipo_atributo_view, modificar_tipo_atributo_view, eliminar_tipo_atributo_view

class UserTestCase(TestCase):
    fixtures = ['usuarios_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_gestion_usuarios_view(self):
        request = self.factory.get('/administracion/gestion_usuarios/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = gestion_usuarios_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('usuarios' in response.content)
        
    def test_crear_usuario_view(self):
        request = self.factory.get('/administracion/gestion_usuarios/crear_usuario/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = crear_usuario_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_usuarios/crear_usuario/', {'username': 'rodrigo', 'email':'rodrigo@gmail.com', 'password_uno':'santos', 'password_dos':'santos', 'first_name':'Rodrigo', 'last_name':'Santos', 'direccion':'', 'telefono':''})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_usuarios/')
        
        usuario = User.objects.get(pk=2)
        
        self.assertTrue(usuario)
        
    def test_modificar_usuario_view(self):
        request = self.factory.get('/administracion/gestion_usuarios/modificar_usuario/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = modificar_usuario_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        self.assertTrue('usuario' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_usuarios/modificar_usuario/1/', {'username': 'rodrigo', 'email':'rodrigo@gmail.com', 'password_uno':'santos', 'password_dos':'santos', 'first_name':'Rodrigo', 'last_name':'Santos', 'direccion':'', 'telefono':''})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_usuarios/usuario/1')
        
        username = User.objects.get(pk=1).username
        
        self.assertEqual(username, 'rodrigo')
        
    def test_eliminar_usuario_view(self):
        request = self.factory.get('/administracion/gestion_usuarios/eliminar_usuario/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = eliminar_usuario_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('usuario' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_usuarios/eliminar_usuario/1/')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_usuarios/')
        
        usuario = User.objects.filter(pk=1)
        
        self.assertFalse(usuario)
        
    def test_roles_usuario_view(self):
        request = self.factory.get('/administracion/gestion_usuarios/roles/usuario/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = roles_usuario_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('usuario' in response.content)
        self.assertTrue('roles' in response.content)
        
    def test_agregar_rol_view(self):
        request = self.factory.get('/administracion/gestion_usuarios/roles/usuario/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = agregar_rol_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('usuario' in response.content)
        self.assertTrue('roles' in response.content)
        
    def test_confirmacion_agregar_rol_view(self):
        request = self.factory.get('/administracion/gestion_usuarios/confirmacion_agregar_rol/usuario/1/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = confirmacion_agregar_rol_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('usuario' in response.content)
        self.assertTrue('rol' in response.content)
        
        usuario = User.objects.get(pk=1)
        rol = usuario.roles.filter(pk=1)
        
        self.assertTrue(rol)
        
    def test_quitar_rol_view(self):
        request = self.factory.get('/administracion/gestion_usuarios/quitar_rol/usuario/1/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = quitar_rol_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('usuario' in response.content)
        self.assertTrue('rol' in response.content)
        
        usuario = User.objects.get(pk=1)
        rol = usuario.roles.filter(pk=1)
        
        self.assertFalse(rol)
        
class RolTestCase(TestCase):
    fixtures = ['roles_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_gestion_roles_view(self):
        request = self.factory.get('/administracion/gestion_roles/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = gestion_roles_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('roles' in response.content)
        
    def test_crear_rol_view(self):
        request = self.factory.get('/administracion/gestion_roles/crear_rol/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = crear_rol_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_roles/crear_rol/', {'nombre': 'Lider', 'descripcion':'Posee todos los permisos para gestionar proyectos.'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_roles/')
        
        rol = Rol.objects.get(pk=2)
        
        self.assertTrue(rol)
        
    def test_modificar_rol_view(self):
        request = self.factory.get('/administracion/gestion_roles/modificar_rol/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = modificar_rol_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        self.assertTrue('rol' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_roles/modificar_rol/1/', {'nombre': 'Desarrollador', 'descripcion':'Posee todos los permisos para alterar los codigos fuentes.'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_roles/rol/1')
        
        nombre = Rol.objects.get(pk=1).nombre
        
        self.assertEqual(nombre, 'Desarrollador')
    
    def test_eliminar_rol_view(self):
        request = self.factory.get('/administracion/gestion_roles/eliminar_rol/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = eliminar_rol_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rol' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_roles/eliminar_rol/1/')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_roles/')
        
        rol = Rol.objects.filter(pk=1)
        
        self.assertFalse(rol)
    
    def test_permisos_rol_view(self):
        request = self.factory.get('/administracion/gestion_roles/permisos/rol/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = permisos_rol_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rol' in response.content)
        self.assertTrue('permisos' in response.content)
    
    def test_agregar_permiso_view(self):
        request = self.factory.get('/administracion/gestion_roles/permisos/rol/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = agregar_permiso_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rol' in response.content)
        self.assertTrue('permisos' in response.content)
    
    def test_confirmacion_agregar_permiso_view(self):
        request = self.factory.get('/administracion/gestion_roles/confirmacion_agregar_permiso/rol/1/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = confirmacion_agregar_permiso_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rol' in response.content)
        self.assertTrue('permiso' in response.content)
        
        rol = Rol.objects.get(pk=1)
        permiso = rol.permisos.filter(pk=1)
        
        self.assertTrue(permiso)
    
    def test_quitar_permiso_view(self):
        request = self.factory.get('/administracion/gestion_roles/quitar_permiso/rol/1/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = quitar_permiso_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rol' in response.content)
        self.assertTrue('permiso' in response.content)
        
        rol = Rol.objects.get(pk=1)
        permiso = rol.permisos.filter(pk=1)
        
        self.assertFalse(permiso)
        
class TipoAtributoTestCase(TestCase):
    fixtures = ['tipos_atributo_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_gestion_tipos_atributo_view(self):
        request = self.factory.get('/administracion/gestion_tipos_atributo/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = gestion_tipos_atributo_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tipos_atributo' in response.content)
    
    def test_crear_tipo_atributo_view(self):
        request = self.factory.get('/administracion/gestion_tipos_atributo/crear_tipo_atributo/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = crear_tipo_atributo_view(request)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_atributo/crear_tipo_atributo/', {'nombre': 'Marca', 'descripcion':'Describe el fabricante del item.', 'tipo_dato':'3'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_atributo/')
        
        tipo_atributo = TipoAtributo.objects.get(pk=2)
        
        self.assertTrue(tipo_atributo)
    """
    def test_modificar_tipo_atributo_view(self):
        request = self.factory.get('/administracion/gestion_tipos_atributo/modificar_tipo_atributo/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = modificar_tipo_atributo_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.content)
        self.assertTrue('tipo_atributo' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_atributo/modificar_tipo_atributo/1/', {'nombre': 'Valido', 'descripcion':'Indica si un item es valido.', 'tipo_dato':'4'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_atributo/tipo_atributo/1')
        
        nombre = TipoAtributo.objects.get(pk=1).nombre
        
        self.assertEqual(nombre, 'Valido')

    def test_eliminar_tipo_atributo_view(self):
        request = self.factory.get('/administracion/gestion_tipos_atributo/eliminar_tipo_atributo/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = eliminar_tipo_atributo_view(request, 1)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('tipo_atributo' in response.content)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_atributo/eliminar_tipo_atributo/1/')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_atributo/')
        
        tipo_atributo = TipoAtributo.objects.filter(pk=1)
        
        self.assertFalse(tipo_atributo)
    """