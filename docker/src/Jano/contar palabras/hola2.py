# -*- coding: utf-8 -*-

import re
import string


def contar_palabras(nombre, repeticion):
    archivo = open(nombre, 'r')
    try:
        texto = archivo.read()

        #patron de busqueda
        patron = re.finditer("\w*", texto)
        for palabrag in patron:
            palabra = palabrag.group()
            contar = repeticion.get(palabra,0)
            repeticion[palabra] = contar + 1

    finally:
        archivo.close()


#defino diccionario donde carga las palabras y la cantidad de veces
repeticion = {}
contar_palabras(repeticion=repeticion, nombre='texto.txt')
for palabras in repeticion:
    print (palabras, rep[palabras])
