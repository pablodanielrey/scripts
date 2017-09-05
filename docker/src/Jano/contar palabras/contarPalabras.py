# -*- coding: utf-8 -*-


"""Contar cuentas veces se repiten las palabras de un texto"""

#cargar el texto del archivo

#Identificar cada una de las palabras

#Guardar las palabras y si ya existe incrementar la cantidad de repeticiones

#Imprimir la lista de palabras con el valor de las repeticiones

palabras = {}

archivo = open('texto.txt', 'r')
texto = archivo.read()

def contarPalabras():
    palabra = texto.split(" ")

# for p in palabra:
#     contar = palabras[palabra,0]
#     palabras[palabra]= contar + 1

print (contarPalabras())
