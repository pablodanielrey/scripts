import sys
import logging
import os
import psycopg2
import psycopg2.extras
import pprint
import re

if __name__ == '__main__':

    usuariosEcono=[]
    usuarioEcono = {}

    hostEcono = os.environ['HOSTE']
    userEcono = os.environ['USERE']
    passwdEcono = os.environ['PASSE']
    baseEcono = os.environ['BASEE']
    con = psycopg2.connect(host=hostEcono, user=userEcono, password=passwdEcono, database=baseEcono)

    def consutarCorreoEcono(id):
        curcorreo.execute("SELECT correo FROM correos WHERE usuario_id = (%s);",(id,))
        correo = str(curcorreo.fetchone())
        direccion = re.findall(r'[\w\.-]+@[\w\.-]+', correo)
        return direccion

    def consutarClaveEcono(id):
        curclave.execute("SELECT clave FROM claves WHERE usuario_id = (%s);",(id,))
        clave = str(curclave.fetchone())
        contrasena = re.findall('\w+', clave, re.IGNORECASE)
        return contrasena

    def consultarUsuarioEcono(curcorreo, curclave):
        curusuario.execute('SELECT * FROM usuarios;')
        for row in curusuario:
            id = row[0]
            nombre = row[1]
            apellido = row[2]
            dni = row[3]

            curcorreo = con.cursor()
            try:
                direccion=consutarCorreoEcono(id)
            finally:
                curcorreo.close()

            curclave = con.cursor()
            try:
                contrasena=consutarClaveEcono(id)
            finally:
                curclave.close()

            usuarioEcono['ID']=row[0]
            usuarioEcono['NOMBRE']=row[1]
            usuarioEcono['APELLIDO']=row[2]
            usuarioEcono['DNI']=row[3]
            usuarioEcono['CORREO']=direccion[0]
            usuarioEcono['CLAVE']=contrasena[0]
            usuariosEcono.append(dict(usuarioEcono))

    hostGoogle = os.environ['HOSTG']
    userGoogle = os.environ['USERG']
    passwdGoogle = os.environ['PASSG']
    baseGoogle = os.environ['BASEG']
    conGoogle = psycopg2.connect(host=hostGoogle, user=userGoogle, password=passwdGoogle, database=baseGoogle)

    def consultarUsuarioGoogle(usuariosEcono):
        for usuario in usuariosEcono:
            print(usuario.items())
            print ('*************************')

    try:
        curcorreo = con.cursor()
        curclave = con.cursor()
        curusuario = con.cursor()

        try:
            consultarUsuarioEcono(curcorreo, curclave)
            consultarUsuarioGoogle(usuariosEcono)

        finally:
            curusuario.close()

    finally:
        con.close()
