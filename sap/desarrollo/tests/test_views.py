from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from administracion.models import Fase, Proyecto, Rol
from desarrollo.models import TipoItem, LineaBase, Item, SolicitudCambio

from desarrollo.views import desarrollo_view, calcular_costo_view, finalizar_proyecto_view
from desarrollo.views import fases_proyecto_view
from desarrollo.views import roles_fase_view, fase_confirmacion_agregar_rol_view, iniciar_fase_view, finalizar_fase_view
from desarrollo.views import tipos_item_fase_view, crear_tipo_item_view, modificar_tipo_item_view, eliminar_tipo_item_view
from desarrollo.views import tipos_atributo_tipo_item_view, confirmacion_agregar_tipo_atributo_view, quitar_tipo_atributo_view
from desarrollo.views import items_fase_view, crear_item_view, modificar_item_view, eliminar_item_view, aprobar_item_view, desaprobar_item_view, calcular_impacto_view
from desarrollo.views import relaciones_item_view, versiones_item_view
from desarrollo.views import lineas_base_fase_view, crear_linea_base_view, linea_base_confirmacion_agregar_item_view, linea_base_quitar_item_view, cerrar_linea_base_view

class DesarrolloTestCase(TestCase):
    fixtures = ['proyectos_testdata.json'] + ['fases_testdata.json'] + ['usuarios_testdata.json'] + ['roles_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_desarrollo_view(self):
        print "Prueba: Desarrollo"
        print ""
        request = self.factory.get('/desarrollo/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = desarrollo_view(request)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de desarrollo retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('proyectos' in response.content, "[GET] No se ha encontrado el contenido proyectos en la pagina retornada.")
        
        print "Desarrollo sin errores\n"
        
    def test_calcular_costo_view(self):
        print "Prueba: Calcular costo de proyecto"
        print ""
        request = self.factory.get('/desarrollo/calcular_costo/proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = calcular_costo_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de calculo de costo de un proyecto retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Calcular costo de proyecto sin errores\n"
        
    def test_finalizar_proyecto_view(self):
        print "Prueba: Finalizar proyecto"
        print ""
        request = self.factory.get('/desarrollo/finalizar_proyecto/1/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = finalizar_proyecto_view(request, 1)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de finalizacion de un proyecto retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        estado_finalizado = Proyecto.objects.get(pk=1).estado
        
        self.assertEqual(estado_finalizado, 2, "El proyecto no ha sido finalizado.")
        
        print "Finalizar proyecto sin errores\n"
        
class FaseTestCase(TestCase):
    fixtures = ['proyectos_testdata.json'] + ['fases_testdata.json'] + ['usuarios_testdata.json'] + ['roles_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_fases_proyecto_view(self):
        print "Prueba: Fases de proyecto"
        print ""
        request = self.factory.get('/desarrollo/fases/proyecto/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = fases_proyecto_view(request, 2)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de fases de proyecto retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Fases de proyecto sin errores\n"
        
    def test_roles_fase_view(self):
        print "Prueba: Roles de fase"
        print ""
        request = self.factory.get('/desarrollo/fases/roles/fase/6/proyecto/3/')
        self.user = User.objects.get(pk=4)
        request.user = self.user
        response = roles_fase_view(request, 3, 6)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de roles de fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        self.assertTrue('roles' in response.content, "[GET] No se ha encontrado el contenido roles en la pagina retornada.")
        
        print "Roles de fase sin errores\n"
        
    def fase_confirmacion_agregar_rol_view(self):
        print "Prueba: Confirmacion de agregacion de rol a fase"
        print ""
        request = self.factory.get('/desarrollo/fases/confirmacion_agregar_rol/3/fase/6/proyecto/3/')
        self.user = User.objects.get(pk=4)
        request.user = self.user
        response = fase_confirmacion_agregar_rol_view(request, 3, 6, 3)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de rol a una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('rol' in response.content, "[GET] No se ha encontrado el contenido rol en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        proyecto = Proyecto.objects.get(pk=3)
        rol = proyecto.roles.filter(pk=3)
        
        self.assertTrue(rol, "No se ha encontrado el rol recientemente agregado a la fase.")
        
        print "Confirmacion de agregacion de rol a fase sin errores\n"
        
    def test_iniciar_fase_view(self):
        print "Prueba: Iniciar fase"
        print ""
        request = self.factory.get('/desarrollo/fases/iniciar_fase/6/proyecto/3/')
        self.user = User.objects.get(pk=4)
        request.user = self.user
        response = iniciar_fase_view(request, 3, 6)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para iniciar fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        
        print "Iniciar fase sin errores\n"
    
    def test_finalizar_fase_view(self):
        print "Prueba: Finalizar fase"
        print ""
        request = self.factory.get('/desarrollo/fases/finalizar_fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = finalizar_fase_view(request, 2, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina para finalizar fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        
        print "Finalizar fase sin errores\n"
    
class TipoItemTestCase(TestCase):
    fixtures = ['proyectos_testdata.json'] + ['fases_testdata.json'] + ['tipos_item_testdata.json'] + ['tipos_atributo_testdata.json'] + ['usuarios_testdata.json'] + ['roles_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_tipos_item_fase_view(self):
        print "Prueba: Tipos de item de fase"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = tipos_item_fase_view(request, 2, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de tipos de item de una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Tipos de item de fase sin errores\n"
        
    def test_crear_tipo_item_view(self):
        print "Prueba: Crear tipo item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/crear_tipo_item/fase/6/proyecto/3/')
        self.user = User.objects.get(pk=4)
        request.user = self.user
        response = crear_tipo_item_view(request, 3, 6)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        self.client.login(username='andres', password='andres')
        
        response = self.client.post('/desarrollo/fases/tipos_item/crear_tipo_item/fase/6/proyecto/3/', {'nombre': 'Tipo de item', 'descripcion':'Descripcion del tipo de item.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de tipo de item no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/tipos_item/fase/6/proyecto/3', "[POST] La direccion de la pagina de creacion de tipo de item retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/tipos_item/fase/6/proyecto/3"%response['Location'])
        
        tipo_item = TipoItem.objects.filter(pk=6)
        
        self.assertTrue(tipo_item, "No se ha encontrado el tipo de item recientemente creado.")
        
        print "Creacion de tipo de item sin errores\n"
        
    def test_modificar_tipo_item_view(self):
        print "Prueba: Modificar tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/crear_tipo_item/fase/6/proyecto/3/')
        self.user = User.objects.get(pk=4)
        request.user = self.user
        response = crear_tipo_item_view(request, 3, 6)
        resp = modificar_tipo_item_view(request, 2, 4, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        self.client.login(username='andres', password='andres')
        
        response = self.client.post('/desarrollo/fases/tipos_item/crear_tipo_item/fase/6/proyecto/3/', {'nombre': 'Tipo de item', 'descripcion':'Descripcion del tipo de item.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de tipo de item no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/tipos_item/fase/6/proyecto/3', "[POST] La direccion de la pagina de creacion de tipo de item retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/tipos_item/fase/6/proyecto/3"%response['Location'])
        
        tipo_item = TipoItem.objects.filter(pk=6)
        
        self.assertTrue(tipo_item, "No se ha encontrado el tipo de item recientemente creado.")
        
        print "Modificacion de tipo de item sin errores\n"

    def test_eliminar_tipo_item_view(self):
        print "Prueba: Eliminar tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/crear_tipo_item/fase/6/proyecto/3/')
        self.user = User.objects.get(pk=4)
        request.user = self.user
        response = crear_tipo_item_view(request, 3, 6)
        resp = eliminar_tipo_item_view(request, 2, 4, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        self.client.login(username='andres', password='andres')
        
        response = self.client.post('/desarrollo/fases/tipos_item/crear_tipo_item/fase/6/proyecto/3/', {'nombre': 'Tipo de item', 'descripcion':'Descripcion del tipo de item.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de tipo de item no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/tipos_item/fase/6/proyecto/3', "[POST] La direccion de la pagina de creacion de tipo de item retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/tipos_item/fase/6/proyecto/3"%response['Location'])
        
        tipo_item = TipoItem.objects.filter(pk=6)
        
        self.assertTrue(tipo_item, "No se ha encontrado el tipo de item recientemente creado.")
        
        print "Eliminacion de tipo de item sin errores\n"
        
    def test_tipos_atributo_tipo_item_view(self):
        print "Prueba: Tipos de atributo de tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/tipos_atributo/tipo_item/4/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = tipos_atributo_tipo_item_view(request, 2, 4, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de tipos de atributo de un tipo de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Tipos de atributo de tipo de item sin errores\n"
        
    def test_confirmacion_agregar_tipo_atributo_view(self):
        print "Prueba: Confirmacion de agregacion de tipo de atributo a tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/tipos_item/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = tipos_item_fase_view(request, 2, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de tipos de item de una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Confirmacion de agregacion de tipo de atributo a tipo de item sin errores\n"
    
    def test_quitar_tipo_atributo_view(self):
        print "Prueba: Quitar tipo de atributo de tipo de item"
        print ""
        request = self.factory.get('/desarrollo/fases/proyecto/2/')
        self.user = User.objects.get(pk=2)
        request.user = self.user
        response = fases_proyecto_view(request, 2)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de fases de proyecto retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Quitar tipo de atributo de tipo de item sin errores\n"
        
class ItemTestCase(TestCase):
    fixtures = ['proyectos_testdata.json'] + ['fases_testdata.json'] + ['lineas_base_testdata.json'] + ['items_testdata.json'] + ['versiones_item_testdata.json'] + ['valores_atributo_testdata.json'] + ['tipos_item_testdata.json'] + ['tipos_atributo_testdata.json'] + ['usuarios_testdata.json'] + ['roles_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()      

    def test_items_fase_view(self):
        print "Prueba: Items de fase"
        print ""
        request = self.factory.get('/desarrollo/fases/items/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = items_fase_view(request, 2, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de items de una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('items' in response.content, "[GET] No se ha encontrado el contenido items en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Items de fase sin errores\n"

    def test_crear_item_view(self):
        print "Prueba: Crear item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/crear_item/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = crear_item_view(request, 2, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='rodrigo', password='rodrigo')
        
        response = self.client.post('/desarrollo/fases/items/crear_item/fase/4/proyecto/2/', {'nombre': 'Item Nuevo', 'descripcion':'Descripcion del item.', 'complejidad':5, 'costo_monetario':150, 'costo_temporal':0, 'tipo_item':4})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de item no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/items/fase/4/proyecto/2', "[POST] La direccion de la pagina de creacion de fase retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/items/fase/4/proyecto/2"%response['Location'])
        
        item = Item.objects.filter(pk=18)
        
        self.assertTrue(item, "No se ha encontrado el item recientemente creado.")
        
        print "Creacion de item sin errores\n"

    def test_modificar_item_view(self):
        print "Prueba: Modificar item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/modificar_item/15/fase/5/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = modificar_item_view(request, 2, 5, 15)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de modificacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        
        self.client.login(username='rodrigo', password='rodrigo')
        
        response = self.client.post('/desarrollo/fases/items/modificar_item/15/fase/5/proyecto/2/', {'nombre': 'Item Nuevo 1', 'descripcion':'Descripcion del item.', 'complejidad':5, 'costo_monetario':150, 'costo_temporal':0, 'Usuario Creador':'Gustavo'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de modificacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/items/item/15/fase/5/proyecto/2', "[POST] La direccion de la pagina de modificacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/items/item/15/fase/5/proyecto/2"%response['Location'])
        
        nombre = Item.objects.get(pk=15).nombre
        
        self.assertEqual(nombre, 'Item Nuevo 1', "La modificacion del item no se ha concretado correctamente.")
        
        print "Modificacion de item sin errores\n"

    def test_eliminar_item_view(self):
        print "Prueba: Eliminar item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/eliminar_item/17/fase/5/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = eliminar_item_view(request, 2, 5, 17)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de eliminacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        
        self.client.login(username='rodrigo', password='rodrigo')
        
        response = self.client.post('/desarrollo/fases/items/eliminar_item/17/fase/5/proyecto/2/')
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de eliminacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/items/fase/5/proyecto/2', "[POST] La direccion de la pagina de eliminacion de proyecto retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/items/fase/5/proyecto/2"%response['Location'])
        
        item = Item.objects.filter(pk=17)
        
        self.assertFalse(item, "Se ha encontrado el item recientemente eliminado.")
        
        print "Eliminacion de item sin errores\n"
        
    def test_aprobar_item_view(self):
        print "Prueba: Aprobar item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/aprobar_item/15/fase/5/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = aprobar_item_view(request, 2, 5, 15)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de aprobacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        estado_aprobado = Item.objects.get(pk=15).estado
        
        self.assertEqual(estado_aprobado, 1, "El item no ha sido aprobado.")
        
        print "Aprobar item sin errores\n"
        
    def test_desaprobar_item_view(self):
        print "Prueba: Desaprobar item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/desaprobar_item/14/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = desaprobar_item_view(request, 2, 4, 14)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de desaprobacion de item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        estado_desaprobado = Item.objects.get(pk=14).estado
        
        self.assertEqual(estado_desaprobado, 0, "El item no ha sido desaprobado.")
        
        print "Desaprobar item sin errores\n"
        
    def test_calcular_impacto_view(self):
        print "Prueba: Calcular impacto de item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/calcular_impacto/12/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = calcular_impacto_view(request, 2, 4, 12)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de calculo de impacto de un item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Calcular impacto de item sin errores\n"
        
    def test_relaciones_item_view(self):
        print "Prueba: Relaciones de item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/relaciones/item/12/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = relaciones_item_view(request, 2, 4, 12)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de relaciones de un item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('padre' in response.content, "[GET] No se ha encontrado el contenido padre en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Relaciones de item sin errores\n"
        
    def test_versiones_item_view(self):
        print "Prueba: Versiones de item"
        print ""
        request = self.factory.get('/desarrollo/fases/items/versiones/item/12/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = versiones_item_view(request, 2, 4, 12)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de relaciones de un item retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Versiones de item sin errores\n"
        
class LineaBaseTestCase(TestCase):
    fixtures = ['proyectos_testdata.json'] + ['fases_testdata.json'] + ['lineas_base_testdata.json'] + ['items_testdata.json'] + ['versiones_item_testdata.json'] + ['valores_atributo_testdata.json'] + ['tipos_item_testdata.json'] + ['tipos_atributo_testdata.json'] + ['usuarios_testdata.json'] + ['roles_testdata.json'] + ['permisos_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()      

    def test_lineas_base_fase_view(self):
        print "Prueba: Lineas base de fase"
        print ""
        request = self.factory.get('/desarrollo/fases/lineas_base/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = lineas_base_fase_view(request, 2, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de lineas base de una fase retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        print "Lineas base de fase sin errores\n"

    def test_crear_linea_base_view(self):
        print "Prueba: Crear linea base"
        print ""
        request = self.factory.get('/desarrollo/fases/lineas_base/crear_linea_base/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = crear_linea_base_view(request, 2, 4)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de creacion de linea base retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('form' in response.content, "[GET] No se ha encontrado el contenido form en la pagina retornada.")
        
        self.client.login(username='rodrigo', password='rodrigo')
        
        response = self.client.post('/desarrollo/fases/lineas_base/crear_linea_base/fase/4/proyecto/2/', {'nombre': 'Linea base', 'descripcion':'Descripcion de la linea base.'})
        
        self.assertEqual(response.status_code, 302, "[POST] La pagina de creacion de linea base no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], 'http://testserver/desarrollo/fases/lineas_base/fase/4/proyecto/2', "[POST] La direccion de la pagina de creacion de linea base retornada no es correcta.\nDireccion de la pagina retornada: %s\nDireccion de la pagina esperada: http://testserver/desarrollo/fases/lineas_base/fase/4/proyecto/2"%response['Location'])
        
        lb = LineaBase.objects.filter(pk=7)
        
        self.assertTrue(lb, "No se ha encontrado la linea base recientemente creada.")
        
        print "Creacion de linea base sin errores\n"

    def test_cerrar_linea_base_view(self):
        print "Prueba: Cerrar linea base"
        print ""
        request = self.factory.get('/desarrollo/lineas_base/cerrar_linea_base/6/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = cerrar_linea_base_view(request, 2, 4, 6)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de cierre de linea base no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        estado = LineaBase.objects.get(pk=6).estado
        
        self.assertEqual(estado, 1, "El cierre de la linea base no se ha concretado correctamente.")
        
        print "Cerrar linea base sin errores\n"
        
    def test_linea_base_confirmacion_agregar_item_view(self):
        print "Prueba: Confirmacion de agregacion item a linea base"
        print ""
        request = self.factory.get('/desarrollo/lineas_base/confirmacion_agregar_item/14/linea_base/6/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = linea_base_confirmacion_agregar_item_view(request, 2, 4, 6, 14)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de agregacion de item a linea base retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        linea_base = LineaBase.objects.get(pk=6)
        item = linea_base.items.filter(pk=14)
        
        self.assertTrue(item, "No se ha encontrado el item recientemente agregado a la linea base.")
        
        print "Confirmacion de agregacion item a linea base sin errores\n"
    
    def test_linea_base_quitar_item_view(self):
        print "Prueba: Quitar item de linea base"
        print ""
        request = self.factory.get('/desarrollo/lineas_base/quitar_item/13/linea_base/6/fase/4/proyecto/2/')
        self.user = User.objects.get(pk=3)
        request.user = self.user
        response = linea_base_quitar_item_view(request, 2, 4, 13, 6)
        
        self.assertEqual(response.status_code, 200, "[GET] La pagina de confirmacion de quitado de item de la linea base retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 200"%response.status_code)
        self.assertTrue('fase' in response.content, "[GET] No se ha encontrado el contenido fase en la pagina retornada.")
        self.assertTrue('item' in response.content, "[GET] No se ha encontrado el contenido item en la pagina retornada.")
        self.assertTrue('proyecto' in response.content, "[GET] No se ha encontrado el contenido proyecto en la pagina retornada.")
        
        linea_base = LineaBase.objects.get(pk=6)
        item = linea_base.items.filter(pk=13)
        
        self.assertFalse(item, "Se ha encontrado el item recientemente quitado de la linea base.")
        
        print "Quitar item de linea base sin errores\n"