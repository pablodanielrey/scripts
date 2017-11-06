# -*- coding: utf-8 -*-
import os


for filename in os.listdir('wpaper'):
    archivo = open('wpaper/' + filename, 'w', errors = 'ignore')
    try:
        texto = archivo.read()
        texto = texto.replace('http://cedlas.econo.unlp.edu.ar/archivos_upload/', 'http://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/')
        print(texto)

    finally:
        archivo.close()
