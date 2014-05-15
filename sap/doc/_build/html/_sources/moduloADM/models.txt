Models
=======

Import::

	from django.db import models
	from django.contrib.auth.models import User
   


.. automodule:: administracion.models
    :members:

class *django.contrib.auth.models.* **User** (args, kwargs)

::

	    Clase que describe la estructura de cada instancia de un usuario, 
	    extendimos la clase User de django y le agregamos los atributos 
	    adicionales que necesitabamos, los atributos que posee cada usuario son:

	    nombre de usuario: nickname del usuario.
	    email: direccion de correo electronico del usuario.
	    nombre/s: nombre real o nombres reales del usuario.
	    apellido/s: apellido/s del usuario.
	    estado: registra el estado del usuario.
	    direccion: ubicacion donde reside el usuario.
	    telefono: numero telefonico del usuario.
	    roles: roles que tiene asignado el usuario.

