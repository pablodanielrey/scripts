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

    host = os.environ['HOST']
    user = os.environ['USER']
    passwd = os.environ['PASS']
    base = os.environ['BASE']
    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)

    def consutarCorreoEcono(id):
        curcorreo.execute("SELECT correo FROM correos WHERE usuario_id = (%s);",(id,))
        correo = str(curcorreo.fetchone())
        patron = re.finditer(r"\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b", correo)
        return patron

    def consutarClaveEcono(id):
        curclave.execute("SELECT clave FROM claves WHERE usuario_id = (%s);",(id,))
        clave = str(curclave.fetchone())
        return clave

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
            usuarioEcono['CORREO']=direccion
            usuarioEcono['CLAVE']=contrasena
            usuariosEcono.append(dict(usuarioEcono))



    try:
        curcorreo = con.cursor()
        curclave = con.cursor()
        curusuario = con.cursor()

        try:
            consultarUsuarioEcono(curcorreo, curclave)

        finally:
            curusuario.close()

    finally:
        con.close()

print(usuariosEcono)
