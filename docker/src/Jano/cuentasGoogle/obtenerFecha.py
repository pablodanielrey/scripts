# -*- coding: utf-8 -*-
import re
import csv
import pprint

ultimoAcceso= set()
usuariosGoogle={}


def escribirCG(archivo, correo):
    archivo.write(correo)
    archivo.write('\n')
    return correo


archivoUA=open('ua.csv','r')
try:
    leerArchivoUA=csv.reader(archivoUA)
    archivoUsuarios=open('usuarios.csv','r')
    try:
        leerU=csv.reader(archivoUsuarios)
        cuentasGoogle = open("cuentasGoogle.txt", "w")
        try:
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
                        # cuentasGoogle.write(correo)
                        # cuentasGoogle.write('\n')

            for dni, correos in usuariosGoogle.items():
                for correo in correos:
                    escribirCG(cuentasGoogle, correo)
                    print (correo)


        finally:
            cuentasGoogle.close()

    finally:
        archivoUsuarios.close()

finally:
    archivoUA.close()





# sorted(usuariosGoogle.keys())
# pprint.pprint(usuariosGoogle)
# print(cantUsuarios)
