from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from inicio.views import login_view

class TestLogin(TestCase):
    fixtures = ['usuarios_testdata.json']
    
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_login(self):
        """
        Test para loguear un usuario.
        """
        request = self.factory.get('/login/')
        self.user = User.objects.get(pk=1)
        request.user = self.user
        response = login_view(request)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
    
    def test_login_usuario_no_existente(self):
        """ 
        Test para loguear a un usuario no registardo.
        """
        self.client.login(username='x', password='x')
        response = self.client.get('/administracion/gestion_usuarios/')
        
        self.assertEqual(response.status_code, 302)