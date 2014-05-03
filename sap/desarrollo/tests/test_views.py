from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from desarrollo.models import Item
from desarrollo.views import items_fase_view, crear_item_view, modificar_item_view, eliminar_item_view

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