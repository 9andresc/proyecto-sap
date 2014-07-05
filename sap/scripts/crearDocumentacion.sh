#!/bin/bash

#Creación de todos los .rst de todos los modulos del proyecto
#sphinx-apidoc -o doc/ .
cd ..
cd doc/
#Creación de los archivos html
make html
