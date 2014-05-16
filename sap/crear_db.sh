#!/bin/bash

echo 1- Se elimina cualquier tabla con el el nombre sap de la base de datos

sudo -u postgres dropdb sap

echo 2- Creacion de la base de datos sap

sudo -u postgres createdb sap

echo 3- Verificando si el usuario admin existe

if [ -z "$(getent passwd admin)" ]; then
    echo 3.1- El usuario admin no existe
    sudo adduser admin
	echo 3.2- El usuario admin fue creado exitosamente
    sudo passwd admin
	echo 3.3- El password del usuario admin fue actualizado exitosamente
else
	echo 3.1- El usuario admin ya existe
    sudo passwd admin
	echo 3.2- El password del usuario admin fue actualizado exitosamente
fi

echo 4- Cambiando el propietario de la base de datos sap

sudo -u postgres psql -c "alter database sap owner to admin;" sap

echo 5- Cambiando el propietario de las tablas de la base de datos sap

sudo -u postgres psql -tc "select 'alter table ' || tablename || ' owner to admin;' from pg_tables where schemaname not in ('pg_catalog', 'information_schema');" sap

echo 6- La base de datos sap fue alterada correctamente

echo 7- Se crean las tablas para la base de datos sap

python manage.py syncdb

echo 8- Se cargan los datos iniciales para el proyecto

python manage.py loaddata datos_iniciales.json
