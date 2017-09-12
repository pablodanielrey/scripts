# -*- coding: utf-8 -*-
import re
import csv
import pprint

ultimoAcceso= set() #para guardar los dni que accedieron a google en el ultimo tiempo
usuariosGoogle={} #para guardar dni + direcciones (incluye alias) de los que acceden a Google
# cantUsuarios=0

def escribirCG(archivo, correo): #escribe el archivo cuentasGoogle.txt final
    archivo.write(correo)
    archivo.write('\n')
    return correo

def leerArchivos(leerArchivoUA, leerU):
    cantDirecciones=0
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
                cantDirecciones +=1

    return cantDirecciones

archivoUA=open('ua.csv','r')
try:
    leerArchivoUA=csv.reader(archivoUA)
    archivoUsuarios=open('usuarios.csv','r')
    try:
        leerU=csv.reader(archivoUsuarios)
        cuentasGoogle = open("cuentasGoogle.txt", "w")
        try:
            cantDirecciones = leerArchivos(leerArchivoUA, leerU)

            for dni, correos in usuariosGoogle.items():
                for correo in correos:
                    escribirCG(cuentasGoogle, correo)
                    print (correo)

            print(cantDirecciones)

        finally:
            cuentasGoogle.close()

    finally:
        archivoUsuarios.close()

finally:
    archivoUA.close()
