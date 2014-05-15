from django.test import TestCase
from administracion.models import Permiso, Rol, TipoAtributo, Proyecto

class PermisoTest(TestCase):
    def crear_permiso(self, nombre="Un permiso"):
        return Permiso.objects.create(nombre=nombre)
    
    def test_creacion_permiso(self):
        print "Prueba: Creacion de la clase Permiso"
        print ""
        p = self.crear_permiso()
        self.assertTrue(isinstance(p, Permiso), "La variable p no es instancia de la clase Permiso.")
        self.assertEqual(p.__unicode__(), p.nombre, "El campo nombre de la variable p no coincide con el valor retornado por la funcion __unicode__().")
        print "Creacion de la clase Permiso sin errores\n"
        
class RolTest(TestCase):
    def crear_rol(self, nombre="Un rol", descripcion="Descripcion de un rol."):
        return Rol.objects.create(nombre=nombre, descripcion=descripcion)
    
    def test_creacion_rol(self):
        print "Prueba: Creacion de la clase Rol"
        print ""
        r = self.crear_rol()
        self.assertTrue(isinstance(r, Rol), "La variable r no es instancia de la clase Rol.")
        self.assertEqual(r.__unicode__(), r.nombre, "El campo nombre de la variable r no coincide con el valor retornado por la funcion __unicode__().")
        print "Creacion de la clase Rol sin errores\n"
        
class TipoAtributoTest(TestCase):
    def crear_tipo_atributo(self, nombre="Un tipo de atributo", descripcion="Descripcion de un tipo de atributo."):
        return TipoAtributo.objects.create(nombre=nombre, descripcion=descripcion)
    
    def test_creacion_tipo_atributo(self):
        print "Prueba: Creacion de la clase TipoAtributo"
        print ""
        t = self.crear_tipo_atributo()
        self.assertTrue(isinstance(t, TipoAtributo), "La variable t no es instancia de la clase TipoAtributo.")
        self.assertEqual(t.__unicode__(), t.nombre, "El campo nombre de la variable t no coincide con el valor retornado por la funcion __unicode__().")
        print "Prueba: Creacion de la clase TipoAtributo sin errores\n"
        
class ProyectoTest(TestCase):
    def crear_proyecto(self, nombre="Un proyecto", descripcion="Descripcion de un proyecto.", fecha_inicio="2014-12-19"):
        return Proyecto.objects.create(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio)
    
    def test_creacion_proyecto(self):
        print "Prueba: Creacion de la clase Proyecto"
        print ""
        p = self.crear_proyecto()
        self.assertTrue(isinstance(p, Proyecto), "La variable p no es instancia de la clase Proyecto.")
        self.assertEqual(p.__unicode__(), p.nombre, "El campo nombre de la variable p no coincide con el valor retornado por la funcion __unicode__().")
        print "Creacion de la clase Proyecto sin errores\n"