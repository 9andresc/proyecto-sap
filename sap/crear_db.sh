#!/bin/bash

echo 1- Se elimina cualquier tabla con el el nombre sap de la base de datos

sudo -u postgres dropdb sap

echo 2- Creacion de la base de datos sap

sudo -u postgres createdb sap

echo 3- La base de datos sap se ha creado con exito

echo 4- Se crean las tablas para la base de datos sap

python manage.py syncdb

echo 5- Se cargan los datos iniciales para el proyecto

python manage.py loaddata datos_iniciales.json
