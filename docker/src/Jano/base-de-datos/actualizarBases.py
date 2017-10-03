import sys
import logging
import os
import psycopg2
import psycopg2.extras
import pprint
import re
import uuid


def consutarCorreoEcono(id):
    curcorreoEcono = conEcono.cursor()
    try:
        curcorreoEcono.execute("SELECT correo FROM correos WHERE usuario_id = (%s);",(id,))
        correo = str(curcorreoEcono.fetchone())
        direccion = re.findall(r'[\w\.-]+@[\w\.-]+', correo)
        return direccion

    finally:
        curcorreoEcono.close()




def consutarClaveEcono(id):
    curclaveEcono = conEcono.cursor()
    try:
        curclaveEcono.execute("SELECT clave FROM claves WHERE usuario_id = (%s);",(id,))
        clave = str(curclaveEcono.fetchone())
        contrasena = re.findall('\w+', clave, re.IGNORECASE)
        return contrasena
    finally:
        curclaveEcono.close()

def obtenerUsuariosEcono(conEcono):
    curusuarioEcono = conEcono.cursor()
    try:
       curusuarioEcono.execute('SELECT * FROM usuarios;')
       usuarios = curusuarioEcono.fetchall()
       return usuarios

    finally:
        curusuarioEcono.close()

def procesarUsuariosEcono(usuarios):
    for row in usuarios:
        id = row[0]
        nombre = row[1]
        apellido = row[2]
        dni = row[3]

        direccion=consutarCorreoEcono(id)
        contrasena=consutarClaveEcono(id)

        usuarioEcono['ID']=row[0]
        usuarioEcono['NOMBRE']=row[1]
        usuarioEcono['APELLIDO']=row[2]
        usuarioEcono['DNI']=row[3]
        usuarioEcono['CORREO']=direccion[0]
        usuarioEcono['CLAVE']=contrasena[0]
        usuariosEcono.append(dict(usuarioEcono))

    return usuariosEcono




def consultarUsuarioGoogle(usuariosEcono):
    curusuarioGoogle.execute('SELECT * FROM usuarios;')

    # id = str(curusuarioGoogle.fetchone())
    id = re.findall('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', str(curusuarioGoogle.fetchall()), re.IGNORECASE)

    for e in usuariosEcono:
        idEcono=e['ID']
        print('salto')
        for i in range(len(id)):
            idGoogle=id[i]
            print (idEcono +' = '+ idGoogle)
            if idEcono == idGoogle:
                print (idGoogle + '                    Existe en Google')
                print ('\n')
            else:
                idEcono=e['ID']
                nombreEcono=e['NOMBRE']
                apellidoEcono=e['APELLIDO']
                dniEcono=e['DNI']
                print(idEcono + '                       No Existe en Google')
                print ('\n')


                # curusuarioGoogle.execute("INSERT INTO usuarios (id, nombre, apellido, dni) VALUES (%s, %s, %s, %s)",(idEcono, nombreEcono, apellidoEcono, dniEcono));
                # conGoogle.commit()


if __name__ == '__main__':

    usuariosEcono=[]
    usuarioEcono = {}

    hostEcono = os.environ['HOSTE']
    userEcono = os.environ['USERE']
    passwdEcono = os.environ['PASSE']
    baseEcono = os.environ['BASEE']

    hostGoogle = os.environ['HOSTG']
    userGoogle = os.environ['USERG']
    passwdGoogle = os.environ['PASSG']
    baseGoogle = os.environ['BASEG']


    conEcono = psycopg2.connect(host=hostEcono, user=userEcono, password=passwdEcono, database=baseEcono)

    try:
        conGoogle = psycopg2.connect(host=hostGoogle, user=userGoogle, password=passwdGoogle, database=baseGoogle)
        try:

            curusuarioGoogle = conGoogle.cursor()

            try:
                usuarios = obtenerUsuariosEcono(conEcono)
                usuariosEcono = procesarUsuariosEcono(usuarios)
                consultarUsuarioGoogle(usuariosEcono)

            finally:
                curusuarioGoogle.close()
        finally:
            conGoogle.close()

    finally:
        conEcono.close()
