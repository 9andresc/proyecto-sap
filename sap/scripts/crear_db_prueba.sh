#!/bin/bash

#variables

#nombre del usuario propietario de la base de datos sap
usuario='admin'
#password del usuario propietario de la base de datos sap
password='admin'

echo 1- Se elimina cualquier base de datos llamada sap

sudo -u postgres dropdb sap

echo 2- Creacion del usuario admin propietario de la base de datos sap

sudo -u postgres dropuser admin

sudo -u postgres createuser --superuser admin

sudo -u postgres psql -c "ALTER USER "$usuario" WITH PASSWORD '"$password"';" postgres

echo 3- Creacion de la base de datos sap

sudo -u postgres createdb -O "$usuario" sap

echo 4- Se crean las tablas para la base de datos sap

python manage.py syncdb

echo 5- Se cargan los datos iniciales para el proyecto

python manage.py loaddata datos_iniciales_prueba.json
