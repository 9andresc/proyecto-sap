from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from desarrollo.models import Item, Fase, TipoItem
from desarrollo.views import fases_proyecto_view
from desarrollo.views
from desarrollo.views import items_fase_view, crear_item_view, modificar_item_view, eliminar_item_view

class FaseTestCase(TestCase):
    fixtures = ['fases_testdata.json'] + ['proyectos_testdata.json'] + ['roles_testdata.json'] + ['usuarios_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_gestion_fases_view(self):
        print "Prueba: Gestion de fases"
        print ""
        request = self.factory.get('/administracion/gestion_fases/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = gestion_fases_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de fases retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fases' in response.content, "[GET] No se ha encontrado el contenido fases en la pagina retornada.")
        print "Gestion de fases sin errores\n"        
    
    def test_crear_fase_view(self):
        print "Prueba: Crear fase"
        print ""
        request = self.factory.get('/administracion/gestion_fases/crear_fase/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = crear_fase_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_fases/crear_fase/', {'nombre': 'Fase', 'descripcion':'Descripcion de la fase.', 'fecha_inicio':'19/12/2014', 'proyecto':6, 'duracion':2})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de fase no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_fases/', "[POST] La direccion de la pagina de creacion de fase retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_fases/"%response['Location'])
        
        fase = Fase.objects.get(pk=5)
        
        self.assertTrue(fase, "No se ha encontrado la fase recientemente creada.")
        print "Creacion de fase sin errores\n"

    def test_modificar_fase_view(self):
        print "Prueba: Modificar fase"
        print ""
        request = self.factory.get('/administracion/gestion_fases/modificar_fase/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = modificar_fase_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_fases/modificar_fase/1/', {'nombre': 'Fase Nueva', 'descripcion':'Descripcion de la fase.', 'fecha_inicio':'19/12/2014', 'proyecto':6, 'duracion':2})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_fases/fase/1', "[POST] La direccion de la pagina de modificacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_fases/fase/1"%response['Location'])
        
        nombre = Fase.objects.get(pk=1).nombre
        
        self.assertEqual(nombre, 'Fase Nueva', "La modificacion de la fase no se ha concretado correctamente.")
        print "Modificacion de fase sin errores\n"

    def test_eliminar_fase_view(self):
        print "Prueba: Eliminar fase"
        print ""
        request = self.factory.get('/administracion/gestion_fases/eliminar_fase/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = eliminar_fase_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_fases/eliminar_fase/1/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_fases/', "[POST] La direccion de la pagina de eliminacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_fases/"%response['Location'])
        
        fase = Fase.objects.filter(pk=1)
        
        self.assertFalse(fase, "Se ha encontrado la fase recientemente eliminada.")
        print "Eliminacion de fase sin errores\n"
    
    def test_roles_fase_view(self):
        print "Prueba: Gestion de roles de fase"
        print ""
        request = self.factory.get('/administracion/gestion_fases/roles/fase/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = roles_fase_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de roles de una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('roles' in response.content, "[GET] No se ha encontrado el contenido roles en la pagina retornada.")
        print "Gestion de roles de fase sin errores\n"
    
    def test_confirmacion_fase_agregar_rol_view(self):
        print "Prueba: Confirmacion de agregacion de rol a fase"
        print ""
        request = self.factory.get('/administracion/gestion_fases/confirmacion_agregar_rol/fase/1/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = confirmacion_fase_agregar_rol_view(request, 1, 2)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de rol a una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        
        fase = Fase.objects.get(pk=1)
        rol = fase.roles.filter(pk=2)
        
        self.assertTrue(rol, "No se ha encontrado el rol recientemente agregado a la fase.")
        print "Confirmacion de agregacion de rol a fase sin errores\n"
    
    def test_fase_quitar_rol_view(self):
        print "Prueba: Quitar rol de fase"
        print ""
        request = self.factory.get('/administracion/gestion_fases/quitar_rol/fase/1/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = fase_quitar_rol_view(request, 1, 2)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para quitar un rol de una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        
        fase = Fase.objects.get(pk=1)
        rol = fase.roles.filter(pk=2)
        
        self.assertFalse(rol, "Se ha encontrado el rol recientemente quitado de la fase.")
        print "Quitar rol de fase sin errores\n"
        
class TipoItemTestCase(TestCase):
    fixtures = ['tipos_item_testdata.json'] + ['tipos_atributo_testdata.json'] + ['roles_testdata.json'] + ['usuarios_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_gestion_tipos_item_view(self):
        print "Prueba: Gestion de tipos de item"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_item/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = gestion_tipos_item_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de tipos de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('tipos_item' in response.content, "[GET] No se ha encontrado el contenido tipos_item en la pagina retornada.")
        print "Gestion de tipos de item sin errores\n"        

    def test_crear_tipo_item_view(self):
        print "Prueba: Crear tipo de item"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_item/crear_tipo_item/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = crear_tipo_item_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_item/crear_tipo_item/', {'nombre': 'Tipo de item', 'descripcion':'Descripcion del tipo de item.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de tipo de item no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_item/', "[POST] La direccion de la pagina de creacion de fase retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/tipos_item/"%response['Location'])
        
        tipo_item = TipoItem.objects.get(pk=3)
        
        self.assertTrue(tipo_item, "No se ha encontrado el tipo de item recientemente creado.")
        print "Creacion de tipo de item sin errores\n"
        
    def test_modificar_tipo_item_view(self):
        print "Prueba: Modificar tipo de item"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_item/modificar_tipo_item/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = modificar_tipo_item_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_item/modificar_tipo_item/1/', {'nombre': 'Tipo de item Nuevo', 'descripcion':'Descripcion del tipo de item.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_item/tipo_item/1', "[POST] La direccion de la pagina de modificacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_tipos_item/tipo_item/1"%response['Location'])
        
        nombre = TipoItem.objects.get(pk=1).nombre
        
        self.assertEqual(nombre, 'Tipo de item Nuevo', "La modificacion del tipo de item no se ha concretado correctamente.")
        print "Modificacion de tipo de item sin errores\n"
        
    def test_eliminar_tipo_item_view(self):
        print "Prueba: Eliminar tipo de item"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_item/eliminar_tipo_item/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = eliminar_tipo_item_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/administracion/gestion_tipos_item/eliminar_tipo_item/1/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/administracion/gestion_tipos_item/', "[POST] La direccion de la pagina de eliminacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/administracion/gestion_tipos_item/"%response['Location'])
        
        tipo_item = TipoItem.objects.filter(pk=1)
        
        self.assertFalse(tipo_item, "Se ha encontrado el tipo de item recientemente eliminado.")
        print "Eliminacion de tipo de item sin errores\n"
    
    def test_tipos_atributo_tipo_item_view(self):
        print "Prueba: Gestion de tipos de atributo de tipo de item"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_item/tipos_atributo/tipo_item/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = tipos_atributo_tipo_item_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de tipos de atributo de un tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('tipo_item' in response.content, "[GET] No se ha encontrado el contenido tipo_item en la pagina retornada.")
        self.assertTrue('tipos_atributo' in response.content, "[GET] No se ha encontrado el contenido tipos_atributo en la pagina retornada.")
        print "Gestion de tipos de atributo de tipo de item sin errores\n"

    def test_confirmacion_agregar_tipo_atributo_view(self):
        print "Prueba: Confirmacion de agregacion de tipo de atributo a tipo de item"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_item/confirmacion_agregar_tipo_atributo/tipo_item/1/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = confirmacion_agregar_tipo_atributo_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de tipo de atributo a un tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('tipo_item' in response.content, "[GET] No se ha encontrado el contenido tipo_item en la pagina retornada.")
        
        tipo_item = TipoItem.objects.get(pk=1)
        tipo_atributo = tipo_item.tipos_atributo.filter(pk=1)
        
        self.assertTrue(tipo_atributo, "No se ha encontrado el tipo de atributo recientemente agregado al tipo de item.")
        print "Confirmacion de agregacion de tipo de atributo a tipo de item sin errores\n"
    
    def test_quitar_tipo_atributo_view(self):
        print "Prueba: Quitar tipo de atributo de tipo de item"
        print ""
        request = self.factory.get('/administracion/gestion_tipos_item/quitar_tipo_atributo/fase/1/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = quitar_tipo_atributo_view(request, 1, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para quitar un tipo de atributo de un tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('tipo_item' in response.content, "[GET] No se ha encontrado el contenido tipo_item en la pagina retornada.")
        
        tipo_item = TipoItem.objects.get(pk=1)
        tipo_atributo = tipo_item.tipos_atributo.filter(pk=1)
        
        self.assertFalse(tipo_atributo, "Se ha encontrado el tipo de atributo recientemente quitado del tipo de item.")
        print "Quitar tipo de atributo de tipo de item sin errores\n"

class ItemTestCase(TestCase):
    fixtures = ['items_testdata.json'] + ['fases_testdata.json'] + ['proyectos_testdata.json'] + ['tipos_item_testdata.json'] + ['tipos_atributo_testdata.json'] + ['roles_testdata.json'] + ['usuarios_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_items_fase_view(self):
        print "Prueba: Gestion de items de fase"
        print ""
        request = self.factory.get('/desarrollo/items/fase/1/proyecto/6/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = items_fase_view(request, 1, 6)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de gestion de items de fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('items' in response.content, "[GET] No se ha encontrado el contenido items en la pagina retornada.")
        print "Gestion de items de fase sin errores\n"        

    def test_crear_item_view(self):
        print "Prueba: Crear item"
        print ""
        request = self.factory.get('/desarrollo/items/crear_item/fase/1/proyecto/6/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = crear_item_view(request, "1", "6")
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/desarrollo/items/crear_item/fase/1/proyecto/6/', {'nombre': 'Item', 'descripcion':'Descripcion del item.', 'complejidad':5, 'costo':150, 'tipo_item':1})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de item no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/items/fase/1/proyecto/6/', "[POST] La direccion de la pagina de creacion de fase retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/items/fase/1/proyecto/6/"%response['Location'])
        
        item = Item.objects.filter(pk=7)
        
        self.assertTrue(item, "No se ha encontrado el item recientemente creado.")
        print "Creacion de item sin errores\n"
        
    def test_modificar_item_view(self):
        print "Prueba: Modificar item"
        print ""
        request = self.factory.get('/desarrollo/items/modificar_item/4/fase/1/proyecto/6/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = modificar_item_view(request, "4", "1", "6")
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/desarrollo/items/modificar_item/4/fase/1/proyecto/6/', {'nombre': 'Item Nuevo', 'descripcion':'Descripcion del item.', 'complejidad':5, 'costo':150})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/items/item/4/fase/1/proyecto/6/', "[POST] La direccion de la pagina de modificacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/items/item/4/fase/1/proyecto/6/"%response['Location'])
        
        nombre = Item.objects.get(pk=4).nombre
        
        self.assertEqual(nombre, 'Item Nuevo', "La modificacion del item no se ha concretado correctamente.")
        print "Modificacion de item sin errores\n"
        
    def test_eliminar_item_view(self):
        print "Prueba: Eliminar item"
        print ""
        request = self.factory.get('/desarrollo/items/eliminar_item/4/fase/1/proyecto/6/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = eliminar_item_view(request, "4", "1", "6")
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        
        self.client.login(username='gustavo', password='cabral')
        
        response = self.client.post('/desarrollo/items/eliminar_item/4/fase/1/proyecto/6/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/items/fase/1/proyecto/6/', "[POST] La direccion de la pagina de eliminacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/items/fase/1/proyecto/6/"%response['Location'])
        
        item = Item.objects.filter(pk=4)
        
        self.assertFalse(item, "Se ha encontrado el item recientemente eliminado.")
        print "Eliminacion de item sin errores\n"