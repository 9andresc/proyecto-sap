from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from desarrollo.models import Item, Fase, TipoItem, LineaBase
from desarrollo.views import iniciar_fase_view, finalizar_fase_view
from desarrollo.views import fase_confirmacion_agregar_rol_view, fase_quitar_rol_view
from desarrollo.views import crear_tipo_item_view, modificar_tipo_item_view, eliminar_tipo_item_view
from desarrollo.views import confirmacion_agregar_tipo_atributo_view, quitar_tipo_atributo_view
from desarrollo.views import crear_item_view, modificar_item_view, eliminar_item_view
from desarrollo.views import crear_linea_base_view, cerrar_linea_base_view
from desarrollo.views import linea_base_confirmacion_agregar_item_view, linea_base_quitar_item_view
"""
class FaseTestCase(TestCase):
    fixtures = ['fases_testdata.json'] + ['proyectos_testdata.json'] + ['roles_testdata.json'] + ['usuarios_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()

    def test_confirmacion_fase_agregar_rol_view(self):
        print "Prueba: Confirmacion de agregacion de rol a fase"
        print ""
        request = self.factory.get('/desarrollo/fases/confirmacion_agregar_rol/1/fase/4/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = fase_confirmacion_agregar_rol_view(request, 1, 4, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de rol a una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        
        fase = Fase.objects.get(pk=4)
        rol = fase.roles.filter(pk=1)
        
        self.assertTrue(rol, "No se ha encontrado el rol recientemente agregado a la fase.")
        print "Confirmacion de agregacion de rol a fase sin errores\n"

    def test_fase_quitar_rol_view(self):
        print "Prueba: Quitar rol de fase"
        print ""
        request = self.factory.get('/desarrollo/fases/quitar_rol/2/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = fase_quitar_rol_view(request, 1, 3, 2)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para quitar un rol de una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        
        fase = Fase.objects.get(pk=3)
        rol = fase.roles.filter(pk=2)
        
        self.assertFalse(rol, "Se ha encontrado el rol recientemente quitado de la fase.")
        print "Quitar rol de fase sin errores\n"
        
    def test_iniciar_fase_view(self):
        print "Prueba: Iniciar fase"
        print ""
        request = self.factory.get('/desarrollo/fases/iniciar_fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = iniciar_fase_view(request, 1, 3)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para iniciar una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        estado = Fase.objects.get(pk=3).estado
        
        self.assertEqual(estado, 1, "La iniciacion de la fase no se ha concretado correctamente.")
        print "Iniciar fase sin errores\n"
        
    def test_finalizar_fase_view(self):
        print "Prueba: Finalizar fase"
        print ""
        request = self.factory.get('/desarrollo/fases/finalizar_fase/2/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = finalizar_fase_view(request, 2, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para iniciar una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        estado = Fase.objects.get(pk=2).estado
        
        self.assertEqual(estado, 2, "La finalizacion de la fase no se ha concretado correctamente.")
        print "Finalizar fase sin errores\n"

class TipoItemTestCase(TestCase):
    fixtures = ['tipos_item_testdata.json'] + ['tipos_atributo_testdata.json'] + ['fases_testdata.json'] + ['proyectos_testdata.json'] + ['usuarios_testdata.json'] + ['roles_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()     

    def test_crear_tipo_item_view(self):
        print "Prueba: Crear tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/crear_tipo_item/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = crear_tipo_item_view(request, 3, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='gustavo')
        
        response = self.client.post('/desarrollo/fases/tipos_item/crear_tipo_item/fase/3/proyecto/1/', {'nombre': 'Tipo de item', 'descripcion':'Descripcion del tipo de item.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de tipo de item no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/tipos_item/fase/3/proyecto/1', "[POST] La direccion de la pagina de creacion de fase retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/tipos_item/fase/3/proyecto/1"%response['Location'])
        
        tipo_item = TipoItem.objects.get(pk=5)
        
        self.assertTrue(tipo_item, "No se ha encontrado el tipo de item recientemente creado.")
        print "Creacion de tipo de item sin errores\n"

    def test_modificar_tipo_item_view(self):
        print "Prueba: Modificar tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/modificar_tipo_item/4/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = modificar_tipo_item_view(request, 3, 4, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='gustavo')
        
        response = self.client.post('/desarrollo/fases/tipos_item/modificar_tipo_item/4/fase/3/proyecto/1/', {'nombre': 'Tipo de item Nuevo', 'descripcion':'Descripcion del tipo de item.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/tipos_item/tipo_item/4/fase/3/proyecto/1', "[POST] La direccion de la pagina de modificacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/tipos_item/tipo_item/4/fase/3/proyecto/1"%response['Location'])
        
        nombre = TipoItem.objects.get(pk=4).nombre
        
        self.assertEqual(nombre, 'Tipo de item Nuevo', "La modificacion del tipo de item no se ha concretado correctamente.")
        print "Modificacion de tipo de item sin errores\n"

    def test_eliminar_tipo_item_view(self):
        print "Prueba: Eliminar tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/eliminar_tipo_item/4/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = eliminar_tipo_item_view(request, 3, 4, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        
        self.client.login(username='gustavo', password='gustavo')
        
        response = self.client.post('/desarrollo/fases/tipos_item/eliminar_tipo_item/4/fase/3/proyecto/1/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/tipos_item/fase/3/proyecto/1', "[POST] La direccion de la pagina de eliminacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/tipos_item/fase/3/proyecto/1"%response['Location'])
        
        tipo_item = TipoItem.objects.filter(pk=4)
        
        self.assertFalse(tipo_item, "Se ha encontrado el tipo de item recientemente eliminado.")
        print "Eliminacion de tipo de item sin errores\n"

    def test_confirmacion_agregar_tipo_atributo_view(self):
        print "Prueba: Confirmacion de agregacion de tipo de atributo a tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/confirmacion_agregar_tipo_atributo/1/tipo_item/4/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = confirmacion_agregar_tipo_atributo_view(request, 3, 1, 4, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de tipo de atributo a un tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('tipo_item' in response.content, "[GET] No se ha encontrado el contenido tipo_item en la pagina retornada.")
        
        tipo_item = TipoItem.objects.get(pk=4)
        tipo_atributo = tipo_item.tipos_atributo.filter(pk=1)
        
        self.assertTrue(tipo_atributo, "No se ha encontrado el tipo de atributo recientemente agregado al tipo de item.")
        print "Confirmacion de agregacion de tipo de atributo a tipo de item sin errores\n"
    
    def test_quitar_tipo_atributo_view(self):
        print "Prueba: Quitar tipo de atributo de tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/quitar_tipo_atributo/2/tipo_item/4/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = quitar_tipo_atributo_view(request, 3, 2, 4, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para quitar un tipo de atributo de un tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('tipo_item' in response.content, "[GET] No se ha encontrado el contenido tipo_item en la pagina retornada.")
        
        tipo_item = TipoItem.objects.get(pk=4)
        tipo_atributo = tipo_item.tipos_atributo.filter(pk=2)
        
        self.assertFalse(tipo_atributo, "Se ha encontrado el tipo de atributo recientemente quitado del tipo de item.")
        print "Quitar tipo de atributo de tipo de item sin errores\n"

class ItemTestCase(TestCase):
    fixtures = ['items_testdata.json'] + ['fases_testdata.json'] + ['lineas_base_testdata.json'] + ['proyectos_testdata.json'] + ['tipos_item_testdata.json'] + ['tipos_atributo_testdata.json'] + ['valores_atributo_testdata.json'] + ['roles_testdata.json'] + ['usuarios_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()      

    def test_crear_item_view(self):
        print "Prueba: Crear item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/crear_item/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = crear_item_view(request, 3, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='gustavo')
        
        response = self.client.post('/desarrollo/fases/items/crear_item/fase/3/proyecto/1/', {'nombre': 'Item', 'descripcion':'Descripcion del item.', 'complejidad':5, 'costo_monetario':150, 'costo_temporal':0, 'tipo_item':4})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de item no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/items/fase/3/proyecto/1', "[POST] La direccion de la pagina de creacion de fase retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/items/fase/3/proyecto/1"%response['Location'])
        
        item = Item.objects.filter(pk=15)
        
        self.assertTrue(item, "No se ha encontrado el item recientemente creado.")
        print "Creacion de item sin errores\n"

    def test_modificar_item_view(self):
        print "Prueba: Modificar item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/modificar_item/14/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = modificar_item_view(request, 3, 14, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        
        self.client.login(username='gustavo', password='gustavo')
        
        response = self.client.post('/desarrollo/fases/items/modificar_item/14/fase/3/proyecto/1/', {'nombre': 'Item Nuevo', 'descripcion':'Descripcion del item.', 'complejidad':5, 'costo_monetario':150, 'costo_temporal':0})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/items/item/14/fase/3/proyecto/1', "[POST] La direccion de la pagina de modificacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/items/item/14/fase/3/proyecto/1"%response['Location'])
        
        nombre = Item.objects.get(pk=14).nombre
        
        self.assertEqual(nombre, 'Item Nuevo', "La modificacion del item no se ha concretado correctamente.")
        print "Modificacion de item sin errores\n"

    def test_eliminar_item_view(self):
        print "Prueba: Eliminar item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/eliminar_item/14/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = eliminar_item_view(request, 3, 14, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        
        self.client.login(username='gustavo', password='gustavo')
        
        response = self.client.post('/desarrollo/fases/items/eliminar_item/14/fase/3/proyecto/1/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/items/fase/3/proyecto/1', "[POST] La direccion de la pagina de eliminacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/items/fase/3/proyecto/1"%response['Location'])
        
        item = Item.objects.filter(pk=14)
        
        self.assertFalse(item, "Se ha encontrado el item recientemente eliminado.")
        print "Eliminacion de item sin errores\n"
        
class LineaBaseTestCase(TestCase):
    fixtures =  ['lineas_base_testdata.json'] + ['fases_testdata.json'] + ['items_testdata.json'] + ['proyectos_testdata.json'] + ['tipos_item_testdata.json'] + ['tipos_atributo_testdata.json'] + ['valores_atributo_testdata.json'] + ['roles_testdata.json'] + ['usuarios_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()      

    def test_crear_linea_base_view(self):
        print "Prueba: Crear linea base"
        print ""
        request = self.factory.get('/desarrollo/fases/lineas_base/crear_linea_base/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = crear_linea_base_view(request, 3, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de linea base retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='gustavo', password='gustavo')
        
        response = self.client.post('/desarrollo/fases/lineas_base/crear_linea_base/fase/3/proyecto/1/', {'nombre': 'Linea base', 'descripcion':'Descripcion de la linea base.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de linea base no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/lineas_base/fase/3/proyecto/1', "[POST] La direccion de la pagina de creacion de linea base retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/lineas_base/fase/3/proyecto/1"%response['Location'])
        
        lb = LineaBase.objects.filter(pk=6)
        
        self.assertTrue(lb, "No se ha encontrado la linea base recientemente creada.")
        print "Creacion de linea base sin errores\n"

    def test_cerrar_linea_base_view(self):
        print "Prueba: Cerrar linea base"
        print ""
        request = self.factory.get('/desarrollo/lineas_base/cerrar_linea_base/5/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = cerrar_linea_base_view(request, 3, 5, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de cierre de linea base no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        estado = LineaBase.objects.get(pk=5).estado
        
        self.assertEqual(estado, 1, "El cierre de la linea base no se ha concretado correctamente.")
        print "Cerrar linea base sin errores\n"
        
    def test_confirmacion_agregar_item_view(self):
        print "Prueba: Confirmacion de agregacion item a linea base"
        print ""
        request = self.factory.get('/desarrollo/lineas_base/confirmacion_agregar_item/13/linea_base/5/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = linea_base_confirmacion_agregar_item_view(request, 3, 5, 13, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de item a linea base retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        linea_base = LineaBase.objects.get(pk=5)
        item = linea_base.items.filter(pk=13)
        
        self.assertTrue(item, "No se ha encontrado el item recientemente agregado a la linea base.")
        print "Confirmacion de agregacion item a linea base sin errores\n"
    
    def test_quitar_item_view(self):
        print "Prueba: Quitar item de linea base"
        print ""
        request = self.factory.get('/desarrollo/lineas_base/quitar_item/13/linea_base/5/fase/3/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = linea_base_quitar_item_view(request, 3, 13, 5, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de quitado de item de la linea base retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        linea_base = LineaBase.objects.get(pk=5)
        item = linea_base.items.filter(pk=13)
        
        self.assertFalse(item, "Se ha encontrado el item recientemente quitado de la linea base.")
        print "Quitar item de linea base sin errores\n"
"""