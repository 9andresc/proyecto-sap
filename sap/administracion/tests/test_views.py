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
        print "Prueba 1: Gestion de usuarios"
        print ""
        request = self.factory.get('/administracion/gestion_roles/')

        self.user = User.objects.get(pk=1)
        request.user = self.user

        response = gestion_usuarios_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de usuarios retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('usuarios' in response.content, "[GET] No se ha encontrado el contenido usuarios en la pagina retornada.")
        print "Gestion de usuarios sin errores\n"
        
    def test_crear_usuario_view(self):
        print "Prueba 2: Crear usuario"
        print ""
        request = self.factory.get('/administracion/gestion_usuarios/crear_usuario/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = crear_usuario_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_usuarios/crear_usuario/', {'username': 'andres', 'email':'andres@gmail.com', 'password_uno':'cabral', 'password_dos':'cabral', 'first_name':'Andres', 'last_name':'Cabral', 'direccion':'', 'telefono':''})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_usuarios/', "[POST] La direccion de la pagina de creacion de usuario retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_usuarios/"%response['Location'])
        
        usuario = User.objects.get(pk=2)
        
        self.assertTrue(usuario, "No se ha encontrado el usuario recientemente creado.")
        print "Creacion de usuario sin errores\n"
        
    def test_modificar_usuario_view(self):
        print "Prueba 3: Modificar usuario"
        print ""
        request = self.factory.get('/administracion/gestion_usuarios/modificar_usuario/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = modificar_usuario_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('usuario' in response.content, "[GET] No se ha encontrado el contenido usuario en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_usuarios/modificar_usuario/1/', {'username': 'andres', 'email':'andres@gmail.com', 'password_uno':'cabral', 'password_dos':'cabral', 'first_name':'Andres', 'last_name':'Cabral', 'direccion':'', 'telefono':''})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_usuarios/usuario/1', "[POST] La direccion de la pagina de modificacion de usuario retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_usuarios/usuario/1"%response['Location'])
        
        username = User.objects.get(pk=1).username
        
        self.assertEqual(username, 'andres', "La modificacion del usuario no se ha concretado correctamente.")
        print "Modificacion de usuario sin errores\n"
        
    def test_eliminar_usuario_view(self):
        print "Prueba 4: Eliminar usuario"
        print ""
        request = self.factory.get('/administracion/gestion_usuarios/eliminar_usuario/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = eliminar_usuario_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('usuario' in response.content, "[GET] No se ha encontrado el contenido usuario en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_usuarios/eliminar_usuario/1/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_usuarios/', "[POST] La direccion de la pagina de eliminacion de usuario retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_usuarios/"%response['Location'])
        
        usuario = User.objects.filter(pk=1)
        
        self.assertFalse(usuario, "Se ha encontrado el usuario recientemente eliminado.")
        print "Eliminacion de usuario sin errores\n"
        
    def test_roles_usuario_view(self):
        print "Prueba 5: Gestion de roles de usuario"
        print ""
        request = self.factory.get('/administracion/gestion_usuarios/roles/usuario/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = roles_usuario_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de roles de un usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('usuario' in response.content, "[GET] No se ha encontrado el contenido usuario en la pagina retornada.")
        self.assertTrue('roles' in response.content, "[GET] No se ha encontrado el contenido roles en la pagina retornada.")
        print "Gestion de roles de usuario sin errores\n"
        
    def test_agregar_rol_view(self):
        print "Prueba 6: Agregacion de roles a usuario"
        print ""
        request = self.factory.get('/administracion/gestion_usuarios/roles/usuario/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = agregar_rol_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de agregacion de roles a un usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('usuario' in response.content, "[GET] No se ha encontrado el contenido usuario en la pagina retornada.")
        self.assertTrue('roles' in response.content, "[GET] No se ha encontrado el contenido roles en la pagina retornada.")
        print "Agregacion de roles a usuario sin errores\n"
        
    def test_confirmacion_agregar_rol_view(self):
        print "Prueba 7: Confirmacion de agregacion de rol a usuario"
        print ""
        request = self.factory.get('/administracion/gestion_usuarios/confirmacion_agregar_rol/usuario/1/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = confirmacion_agregar_rol_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de rol a un usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('usuario' in response.content, "[GET] No se ha encontrado el contenido usuario en la pagina retornada.")
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        
        usuario = User.objects.get(pk=1)
        rol = usuario.roles.filter(pk=1)
        
        self.assertTrue(rol, "No se ha encontrado el rol recientemente agregado al usuario.")
        print "Confirmacion de agregacion de rol a usuario sin errores\n"
        
    def test_quitar_rol_view(self):
        print "Prueba 8: Quitar rol de usuario"
        print ""
        request = self.factory.get('/administracion/gestion_usuarios/quitar_rol/usuario/1/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = quitar_rol_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para quitar un rol de un usuario retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('usuario' in response.content, "[GET] No se ha encontrado el contenido usuario en la pagina retornada.")
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        
        usuario = User.objects.get(pk=1)
        rol = usuario.roles.filter(pk=1)
        
        self.assertFalse(rol, "Se ha encontrado el rol recientemente quitado del usuario.")
        print "Quitar rol de usuario sin errores\n"
        
class RolTestCase(TestCase):
    fixtures = ['usuarios_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_gestion_roles_view(self):
        print "Prueba 9: Gestion de roles"
        print ""
        request = self.factory.get('/administracion/gestion_roles/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = gestion_roles_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de roles retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('roles' in response.content, "[GET] No se ha encontrado el contenido roles en la pagina retornada.")
        print "Gestion de roles sin errores\n"
        
    def test_crear_rol_view(self):
        print "Prueba 10: Crear rol"
        print ""
        request = self.factory.get('/administracion/gestion_roles/crear_rol/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = crear_rol_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_roles/crear_rol/', {'nombre': 'Lider', 'descripcion':'Posee todos los permisos para gestionar proyectos.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_roles/', "[POST] La direccion de la pagina de creacion de rol retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_roles/"%response['Location'])
        
        rol = Rol.objects.get(pk=2)
        
        self.assertTrue(rol, "No se ha encontrado el rol recientemente creado.")
        print "Creacion de rol sin errores\n"
        
    def test_modificar_rol_view(self):
        print "Prueba 11: Modificar rol"
        print ""
        request = self.factory.get('/administracion/gestion_roles/modificar_rol/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = modificar_rol_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_roles/modificar_rol/1/', {'nombre': 'Desarrollador', 'descripcion':'Posee todos los permisos para alterar los codigos fuentes.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_roles/rol/1', "[POST] La direccion de la pagina de modificacion de rol retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_roles/rol/1"%response['Location'])
        
        nombre = Rol.objects.get(pk=1).nombre
        
        self.assertEqual(nombre, 'Desarrollador', "La modificacion del rol no se ha concretado correctamente.")
        print "Modificacion de rol sin errores\n"
    
    def test_eliminar_rol_view(self):
        print "Prueba 12: Eliminar rol"
        print ""
        request = self.factory.get('/administracion/gestion_roles/eliminar_rol/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = eliminar_rol_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_roles/eliminar_rol/1/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_roles/', "[POST] La direccion de la pagina de eliminacion de rol retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_roles/"%response['Location'])
        
        rol = Rol.objects.filter(pk=1)
        
        self.assertFalse(rol, "Se ha encontrado el rol recientemente eliminado.")
        print "Eliminacion de rol sin errores\n"
    
    def test_permisos_rol_view(self):
        print "Prueba 13: Gestion de permisos de rol"
        print ""
        request = self.factory.get('/administracion/gestion_roles/permisos/rol/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = permisos_rol_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de permisos de un rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        self.assertTrue('permisos' in response.content, "[GET] No se ha encontrado el contenido permisos en la pagina retornada.")
        print "Gestion de permisos de rol sin errores\n"
        
    def test_agregar_permiso_view(self):
        print "Prueba 14: Agregacion de permisos a rol"
        print ""
        request = self.factory.get('/administracion/gestion_roles/permisos/rol/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = agregar_permiso_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de agregacion de permisos a un rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        self.assertTrue('permisos' in response.content, "[GET] No se ha encontrado el contenido permisos en la pagina retornada.")
        print "Agregacion de permisos a rol sin errores\n"
    
    def test_confirmacion_agregar_permiso_view(self):
        print "Prueba 15: Confirmacion de agregacion de permiso a rol"
        print ""
        request = self.factory.get('/administracion/gestion_roles/confirmacion_agregar_permiso/rol/1/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = confirmacion_agregar_permiso_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de permiso a un rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        self.assertTrue('permiso' in response.content, "[GET] No se ha encontrado el contenido permiso en la pagina retornada.")
        
        rol = Rol.objects.get(pk=1)
        permiso = rol.permisos.filter(pk=1)
        
        self.assertTrue(permiso, "No se ha encontrado el permiso recientemente agregado al rol.")
        print "Confirmacion de agregacion de permiso a rol sin errores\n"
    
    def test_quitar_permiso_view(self):
        print "Prueba 16: Quitar permiso de rol"
        print ""
        request = self.factory.get('/administracion/gestion_roles/quitar_permiso/rol/1/1/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = quitar_permiso_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para quitar un permiso de un rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        self.assertTrue('permiso' in response.content, "[GET] No se ha encontrado el contenido permiso en la pagina retornada.")
        
        rol = Rol.objects.get(pk=1)
        permiso = rol.permisos.filter(pk=1)
        
        self.assertFalse(permiso, "Se ha encontrado el permiso recientemente quitado del rol.")
        print "Quitar permiso de rol sin errores\n"
        
class TipoAtributoTestCase(TestCase):
    fixtures = ['tipos_atributo_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_gestion_tipos_atributo_view(self):
        print "Prueba 17: Gestion de tipos de atributo"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_atributo/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = gestion_tipos_atributo_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de tipos de rol retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('tipos_atributo' in response.content, "[GET] No se ha encontrado el contenido tipos_atributo en la pagina retornada.")
        print "Gestion de tipos de atributo sin errores\n"
    
    def test_crear_tipo_atributo_view(self):
        print "Prueba 18: Crear tipo de atributo"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_atributo/crear_tipo_atributo/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = crear_tipo_atributo_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de tipo de atributo retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_atributo/crear_tipo_atributo/', {'nombre': 'Marca', 'descripcion':'Describe el fabricante del item.', 'tipo_dato':'3'})
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_atributo/')
        
        tipo_atributo = TipoAtributo.objects.get(pk=2)
        
        self.assertTrue(tipo_atributo, "No se ha encontrado el tipo de atributo recientemente creado.")
        print "Creacion de tipo de atributo sin errores\n"

    def test_modificar_tipo_atributo_view(self):
        print "Prueba 19: Modificar tipo de atributo"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_atributo/modificar_tipo_atributo/2/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = modificar_tipo_atributo_view(request, 2)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de tipo de atributo retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_atributo/modificar_tipo_atributo/2/', {'nombre': 'Valido', 'descripcion':'Indica si un item es valido.', 'tipo_dato':'2'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de tipo de atributo retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_atributo/tipo_atributo/2', "[POST] La direccion de la pagina de modificacion de tipo de atributo retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_tipos_atributo/tipo_atributo/2"%response['Location'])
        
        nombre = TipoAtributo.objects.get(pk=2).nombre
        
        self.assertEqual(nombre, 'Valido', "La modificacion del tipo de atributo no se ha concretado correctamente.")
        print "Modificacion de tipo de atributo sin errores\n"
        
    def test_eliminar_tipo_atributo_view(self):
        print "Prueba 20: Eliminar tipo de atributo"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_atributo/eliminar_tipo_atributo/2/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = eliminar_tipo_atributo_view(request, 2)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de tipo de atributo retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_atributo/eliminar_tipo_atributo/2/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de tipo de atributo retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_atributo/', "[POST] La direccion de la pagina de eliminacion de tipo de atributo retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_tipos_atributo/"%response['Location'])
        
        tipo_atributo = TipoAtributo.objects.filter(pk=2)
        
        self.assertFalse(tipo_atributo)

