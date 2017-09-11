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

cuentasGoogle = open("cuentasGoogle.txt", "w")

cantUsuarios=0

def escribirCG(correo):
    cuentasGoogle.write(correo)
    cuentasGoogle.write('\n')
    return correo


try:
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
                # cuentasGoogle.write(correo)
                # cuentasGoogle.write('\n')

    for dni, correos in usuariosGoogle.items():
        for correo in correos:
            escribirCG(str(correo))
            print (str(correo))


finally:
    archivoUA.close()
    archivoUsuarios.close()

# sorted(usuariosGoogle.keys())
# pprint.pprint(usuariosGoogle)
# print(cantUsuarios)
