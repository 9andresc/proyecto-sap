from django.test import TestCase
from desarrollo.models import Item, TipoItem
        
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