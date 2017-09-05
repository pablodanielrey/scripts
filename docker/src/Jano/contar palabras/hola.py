# -*- coding: utf-8 -*-

import re
import string




#defino diccionario donde carga las palabras y la cantidad de veces
rep = {}
archivo = open('texto.txt', 'r')
try:
    texto = archivo.read()

    #patron de busqueda
    patron = re.finditer("\w*", texto)
    for palabrag in patron:
        palabra = palabrag.group()
        contar = rep.get(palabra,0)
        rep[palabra] = contar + 1

finally:
    archivo.close()

for palabras in rep:
    print (palabras, rep[palabras])
