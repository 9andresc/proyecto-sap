from django.test import TestCase
from desarrollo.models import Item

class ItemTest(TestCase):
    def crear_item(self, nombre="Un item", descripcion="Descripcion de un item.", costo=15, complejidad=5):
        return Item.objects.create(nombre=nombre, descripcion=descripcion, costo=costo, complejidad=complejidad)
    
    def test_creacion_item(self):
        print "Prueba: Creacion de la clase Item"
        print ""
        i = self.crear_item()
        self.assertTrue(isinstance(i, Item), "La variable i no es instancia de la clase Item.")
        self.assertEqual(i.__unicode__(), i.nombre, "El campo nombre de la variable i no coincide con el valor retornado por la funcion __unicode__().")
        print "Creacion de la clase Item sin errores\n"