#!/bin/bash
sudo apt-get install python-setuptools
sudo apt-get install graphviz libgraphviz-dev pkg-config
sudo easy_install pyparsing
cd herramientas/pydot-1.0.28/
sudo python setup.py install
