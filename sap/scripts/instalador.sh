#! /bin/bash


#adquirimos el nombre del usuario y definimos la ruta de instalacion en un directorio en ese usuario

usuario=$SUDO_USER
rutainstalacion="/home/$usuario"

#ruta actual del instalador
rutainstalador=`pwd`

#direcciones web de los paquetes que contienen el codigo fuente de cada iteracion y el codigo fuente del branch master

iteracion1="https://github.com/GustavoAndresCabral/proyecto-sap/archive/Iteracion_1.zip"
iteracion2="https://github.com/GustavoAndresCabral/proyecto-sap/archive/Iteracion_2.zip"
iteracion3="https://github.com/GustavoAndresCabral/proyecto-sap/archive/Iteracion_3.zip"
iteracion4="https://github.com/GustavoAndresCabral/proyecto-sap/archive/Iteracion_4.zip"
iteracion5="https://github.com/GustavoAndresCabral/proyecto-sap/archive/Iteracion_5.zip"
iteracion6="https://github.com/GustavoAndresCabral/proyecto-sap/archive/Iteracion_6.zip"
iteracion7="https://github.com/GustavoAndresCabral/proyecto-sap/archive/Iteracion_7.zip"

function opciones
{
echo ' 1 Iteracion1'
echo ' 2 Iteracion2'
echo ' 3 Iteracion3'
echo ' 4 Iteracion4'
echo ' 5 Iteracion5'
echo ' 6 Iteracion6'
echo ' 7 Iteracion7'
echo 'Seleccione el numero de la opción a instalar'
}

function entorno
{
echo ' 1 Pruebas'
echo ' 2 Produccion'
echo 'Seleccione el numero de la opción a utilizar'
}

function error
{
echo 'Opcion no valida, porfavor ingrese una opcion valida'
}

clear
continuar=true
while [ $continuar == true ]
do
opciones
read OPT
case $OPT in
1 )
fuente="$iteracion1"
echo 'Iteracion 1 seleccionada'
nombre_fichero='Iteracion_1'
continuar=false ;;
2 )
fuente="$iteracion2"
echo 'Iteracion 2 seleccionada'
nombre_fichero='Iteracion_2'
continuar=false ;;
3 )
fuente="$iteracion3"
echo 'Iteracion 3 seleccionada'
nombre_fichero='Iteracion_3'
continuar=false ;;
4 )
fuente="$iteracion4"
echo 'Iteracion 4 seleccionada'
nombre_fichero='Iteracion_4'
continuar=false ;;
5 )
fuente="$iteracion5"
echo 'Iteracion 5 seleccionada'
nombre_fichero='Iteracion_5'
continuar=false ;;
6 )
fuente="$iteracion6"
echo 'Iteracion 6 seleccionada'
nombre_fichero='Iteracion_6'
continuar=false ;;
7 )
fuente="$iteracion7"
echo 'Iteracion 7 Seleccionada'
nombre_fichero='Iteracion_7'
continuar=false ;;
? ) clear && error;;
esac
done

if [ ! -d "$rutainstalacion" ];
then
echo "###### LA RUTA DE INSTALACION NO EXISTE, SE CREARA EL DIRECTORIO EN LA RUTA ESPECIFICADA ######"
mkdir -p "$rutainstalacion"
fi


if [ ! -d "$rutainstalacion" ];
then
echo "LA RUTA SELECCIONADA NO EXISTE, SE CREARA EL DIRECTORIO AHORA"
mkdir -p "$rutainstalacion"
fi

echo "INICIANDO LA INSTALACION DEL SISTEMA SAP"


#proyecto
if [ -d "$rutainstalacion/sap" ];
then
echo "Eliminando proyecto existente"
rm -rf "$rutainstalacion/sap"
rm "$rutainstalacion/README.md"
fi
if [ ! -d proyecto ];
then
rm -rf proyecto
wget "$fuente" -P proyecto
fi
cd proyecto
unzip "$nombre_fichero".zip
cd proyecto-sap-"$nombre_fichero"
mv * "$rutainstalacion"
cd "$rutainstalacion"
chown "$usuario" sap README.md
chmod -R 777 sap
cd "$rutainstalador"
rm -rf proyecto

#archivo sap.wsgi
ruta_sap_wsgi="$rutainstalacion/sap"
instalado=`ls "$ruta_sap_wsgi/apache_wsgi" | grep sap.wsgi`
if [ -n "$instalado" ];
then
echo "borrando el archivo sap.wsgi existente en el proyecto"
rm "$ruta_sap_wsgi/apache_wsgi/sap.wsgi"
fi
echo "creando el archivo sap.wsgi"
echo "import os" > sap.wsgi
echo "import sys" >> sap.wsgi
echo "sys.path = ['"$ruta_sap_wsgi"'] + sys.path" >> sap.wsgi
echo "os.environ['DJANGO_SETTINGS_MODULE'] = 'sap.settings'" >> sap.wsgi
echo "import django.core.handlers.wsgi" >> sap.wsgi
echo "application = django.core.handlers.wsgi.WSGIHandler()" >> sap.wsgi
echo "moviendo el archivo sap.wsgi al proyecto..."
mv sap.wsgi "$ruta_sap_wsgi/apache_wsgi"
chown $usuario "$ruta_sap_wsgi/apache_wsgi/sap.wsgi"
chmod +x "$ruta_sap_wsgi/apache_wsgi/sap.wsgi"
echo "archivo sap.wsgi movido"

#archivo sap.conf
ruta_sap_conf="/etc/apache2/sites-available"
instalado=`ls "$ruta_sap_conf" | grep sap.conf`
if [ -n "$instalado" ];
then
echo "borrando el archivo sap.conf existente en $ruta_sap_conf"
rm "$ruta_sap_conf/sap.conf"
fi
echo "creando el archivo sap.conf"
echo "<VirtualHost *:80>" > sap.conf
echo "WSGIScriptAlias / $ruta_sap_wsgi/apache_wsgi/sap.wsgi" >> sap.conf
echo "" >> sap.conf
echo "ServerName sap.com" >> sap.conf
echo "Alias /static $ruta_sap_wsgi/static/" >> sap.conf
echo "" >> sap.conf
echo "<Directory $ruta_sap_wsgi>" >> sap.conf
echo "Order allow,deny" >> sap.conf
echo "Allow from all" >> sap.conf
echo "</Directory>" >> sap.conf
echo "</VirtualHost>" >> sap.conf
echo "moviendo el archivo sap.conf en $ruta_sap_conf"
chmod 777 sap.conf
mv sap.conf "$ruta_sap_conf"
echo "archivo sap.conf movido"
echo "activando el servidor apache con django..."
cd /etc/apache2/sites-available/
a2ensite sap.conf
/etc/init.d/apache2 restart
cd "$rutainstalador"
echo "servidor apache activado"

if [ $nombre_fichero == "Iteracion_6" ] || [ $nombre_fichero == "master" ];
then


echo "Seleccione un entorno de base de datos para trabajar"

continuar=true
while [ $continuar == true ]
do
entorno
read OPT
case $OPT in
1 )
echo 'Entorno de Pruebas seleccionado'
cd "$rutainstalacion/sap"
cd scripts
./crear_db_prueba.sh
continuar=false ;;
2 )
echo 'Entorno de Produccion seleccionado'
cd "$rutainstalacion/sap"
cd scripts
./crear_db_produccion.sh
continuar=false ;;
? ) clear && error;;
esac
done

fi

#archivo hosts
instalado=`grep sap.com /etc/hosts`
if [ -n "$instalado" ];
then
echo "el link sap.com ya esta activado"
else
echo "activando el link sap.com..."
echo '' >> /etc/hosts
echo '127.0.1.1 sap.com' >> /etc/hosts
/etc/init.d/apache2 restart
echo "el link sap.com activado"
fi

echo "###### INSTALACION FINALIZADA, LANZANDO EL NAVEGADOR ######"
firefox -new-tab sap.com

#para lanzar el proyecto en google-chrome
#google-chrome -new-tab sap.com
