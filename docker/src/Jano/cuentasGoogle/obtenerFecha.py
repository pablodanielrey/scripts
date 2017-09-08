# -*- coding: utf-8 -*-
import re
import csv
import pprint

ultimoAcceso= set()
usuariosGoogle={}

archivoUA=open('ua.csv','r')
leerArchivoUA=csv.reader(archivoUA)

archivoUsuarios=open('usuarios.csv','r')
leerU=csv.reader(archivoUsuarios)

cantUsuarios=0

for linea in leerArchivoUA:
    dni=linea[0].replace('@econo.unlp.edu.ar','')
    if int(linea[1]) > 20170600:
        ultimoAcceso.add(dni)

for linea in leerU:
    dni=linea[0]
    correo=linea[1]
    if dni in ultimoAcceso:
        direcciones=usuariosGoogle.get(dni, [])
        if 'econo.unlp.edu.ar' in correo:
            direcciones.append(correo)
            usuariosGoogle[dni]=direcciones
            cantUsuarios +=1


pprint.pprint(usuariosGoogle)
print(cantUsuarios)
