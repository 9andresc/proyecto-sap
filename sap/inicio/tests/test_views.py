from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from inicio.views import login_view

class TestLogin(TestCase):
    fixtures = ['usuarios_testdata.json'] + ['permisos_testdata.json'] + ['roles_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_login(self):
        print "Prueba: Inicio de sesion"
        print ""
        request = self.factory.get('/login/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = login_view(request)
        
        self.assertEqual(response.status_code, 302, "[GET] La pagina de inicio de sesion retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        self.assertEqual(response['Location'], '/')
        print "Inicio de sesion sin errores\n"
    
    def test_login_usuario_no_existente(self):
        print "Prueba: Cierre de sesion"
        print ""
        self.client.login(username='x', password='x')
        response = self.client.get('/administracion/gestion_usuarios/')
        
        self.assertEqual(response.status_code, 302, "[GET] La pagina de cierre de sesion retornada no es correcta.\nCodigo de la pagina retornada: %s\nCodigo de la pagina esperada: 302"%response.status_code)
        print "Cierre de sesion sin errores\n"