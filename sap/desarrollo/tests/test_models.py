from django.test import TestCase
from desarrollo.models import Item, Fase, TipoItem

class FaseTest(TestCase):
    def crear_fase(self, nombre="Una fase", descripcion="Descripcion de una fase.", fecha_inicio="2014-12-19"):
        return Fase.objects.create(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio)
    
    def test_creacion_fase(self):
        print "Prueba: Creacion de la clase Fase"
        print ""
        f = self.crear_fase()
        self.assertTrue(isinstance(f, Fase), "La variable f no es instancia de la clase Fase.")
        self.assertEqual(f.__unicode__(), f.nombre, "El campo nombre de la variable f no coincide con el valor retornado por la funcion __unicode__().")
        print "Creacion de la clase Fase sin errores\n"
        
class TipoItemTest(TestCase):
    def crear_tipo_item(self, nombre="Un tipo de item", descripcion="Descripcion de un tipo de item."):
        return TipoItem.objects.create(nombre=nombre, descripcion=descripcion)
    
    def test_creacion_tipo_item(self):
        print "Prueba: Creacion de la clase TipoItem"
        print ""
        t = self.crear_tipo_item()
        self.assertTrue(isinstance(t, TipoItem), "La variable t no es instancia de la clase TipoItem.")
        self.assertEqual(t.__unicode__(), t.nombre, "El campo nombre de la variable t no coincide con el valor retornado por la funcion __unicode__().")
        print "Creacion de la clase TipoItem sin errores\n"

class ItemTest(TestCase):
    def crear_item(self, nombre="Un item", descripcion="Descripcion de un item.", costo_monetario=15, costo_temporal=0, complejidad=5):
        return Item.objects.create(nombre=nombre, descripcion=descripcion, costo_monetario=costo_monetario, costo_temporal=costo_temporal, complejidad=complejidad)
    
    def test_creacion_item(self):
        print "Prueba: Creacion de la clase Item"
        print ""
        i = self.crear_item()
        self.assertTrue(isinstance(i, Item), "La variable i no es instancia de la clase Item.")
        self.assertEqual(i.__unicode__(), i.nombre, "El campo nombre de la variable i no coincide con el valor retornado por la funcion __unicode__().")
        print "Creacion de la clase Item sin errores\n"