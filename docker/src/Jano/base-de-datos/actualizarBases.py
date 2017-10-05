import sys
import logging
import os
import psycopg2
import psycopg2.extras
import pprint
import re
import uuid


def consultarCorreoEcono(id):
    curcorreoEcono = conEcono.cursor()
    try:
        curcorreoEcono.execute("SELECT correo FROM correos WHERE usuario_id = (%s);",(id,))
        correo = str(curcorreoEcono.fetchone())
        direccion = re.findall(r'[\w\.-]+@[\w\.-]+', correo)

        return direccion

    finally:
        curcorreoEcono.close()

def consultarClaveEcono(id):
    curclaveEcono = conEcono.cursor()
    try:
        curclaveEcono.execute("SELECT usuario_id, clave, modificado FROM claves WHERE usuario_id = (%s);",(id,))
        row = curclaveEcono.fetchone()
        usuario_id=row[0]
        clave = row[1]
        fechaModClave=row[2]

        claveEcono['USUARIO_ID']=usuario_id
        claveEcono['CLAVE']=clave
        claveEcono['MODIFICADO']=fechaModClave
        clavesEcono.append(dict(claveEcono))


        return clavesEcono
    finally:
        curclaveEcono.close()

def obtenerUsuariosEcono(conEcono):
    curusuarioEcono = conEcono.cursor()
    try:
       curusuarioEcono.execute('SELECT * FROM usuarios;')
       usuariosE = curusuarioEcono.fetchall()
       return usuariosE

    finally:
        curusuarioEcono.close()

def procesarUsuariosEcono(usuarios):
    for row in usuarios:
        id = row[0]
        nombre = row[1]
        apellido = row[2]
        dni = row[3]
        creado = row[4]
        modificado = row[5]
        eliminado = row[6]

        direccion=consultarCorreoEcono(id)
        contrasena=consultarClaveEcono(id)

        usuarioEcono['ID']=id
        usuarioEcono['NOMBRE']=nombre
        usuarioEcono['APELLIDO']=apellido
        usuarioEcono['DNI']=dni
        usuarioEcono['CREADO']=creado
        usuarioEcono['MODIFICADO']=modificado
        usuarioEcono['ELIMINADO']=eliminado
        usuarioEcono['CORREO']=direccion[0]
        usuarioEcono['CLAVE']=contrasena[-1]['CLAVE']
        usuariosEcono.append(dict(usuarioEcono))

    return usuariosEcono

def consultarClaveGoogle(id):
    curclaveGoogle = conGoogle.cursor()
    try:
        curclaveGoogle.execute("SELECT usuario_id, clave, modificado FROM claves WHERE usuario_id = (%s);",(id,))
        row = curclaveGoogle.fetchone()
        usuario_id=row[0]
        clave = row[1]
        fechaModClave=row[2]

        claveGoogle['USUARIO_ID']=usuario_id
        claveGoogle['CLAVE']=clave
        claveGoogle['MODIFICADO']=fechaModClave
        clavesGoogle.append(dict(claveGoogle))

        return clavesGoogle

    finally:
        curclaveGoogle.close()



def actualizarUsuariosGoogle(cur, usuariosEcono):

    cur.execute('SELECT id, modificado FROM usuarios;')
    usuariosGoogle = {}
    for e in [{'id':c[0],'modificado':c[1]} for c in cur]:
        usuariosGoogle[e['id']] = e['modificado']

    for u in usuariosEcono:
        econoId = u['ID']
        if u['MODIFICADO'] > usuariosGoogle[econoId]:
            cur.execute("UPDATE usuarios SET modificado=current_timestamp WHERE id = (%s);",(econoId,))
            print ('Actualizado recientemente en Google ---> ' + econoId)
        else:
            print ('Ya esta actualizado en Google ---> ' + econoId)




def insertarUsuarioGoogle(cur, usuariosEcono):

    cur.execute('SELECT id FROM usuarios;')
    idsGoogle = [c[0] for c in cur]

    for e in usuariosEcono:
        idEcono=e['ID']
        if idEcono not in idsGoogle:
            nombreEcono=e['NOMBRE']
            apellidoEcono=e['APELLIDO']
            dniEcono=e['DNI']
            creadoEcono=e['CREADO']
            modificadoEcono=e['MODIFICADO']
            eliminadoEcono=e['ELIMINADO']
            correoEcono=e['CORREO']
            claveEcono=e['CLAVE']

            idCorreoEcono=str(uuid.uuid4());
            idClaveEcono=str(uuid.uuid4());

            cur.execute("""
               INSERT INTO usuarios (id, nombre, apellido, dni, creado, modificado, eliminado)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,(idEcono, nombreEcono, apellidoEcono, dniEcono, creadoEcono, modificadoEcono, eliminadoEcono));

            cur.execute("""
               INSERT INTO correos (id, usuario_id, correo, creado, modificado, eliminado)
               VALUES (%s, %s, %s, %s, %s, %s)
            """,(idCorreoEcono, idEcono, correoEcono, creadoEcono, modificadoEcono, eliminadoEcono));

            cur.execute("""
               INSERT INTO claves (id, usuario_id, clave, creado, modificado, eliminado)
               VALUES (%s, %s, %s, %s, %s, %s)
            """,(idClaveEcono, idEcono, claveEcono, creadoEcono, modificadoEcono, eliminadoEcono));

            print ('Agregado recientemente a Google ---> ' + idEcono)


if __name__ == '__main__':

    claveEcono={}
    clavesEcono=[]
    usuarioEcono = {}
    usuariosEcono=[]

    claveGoogle={}
    clavesGoogle=[]


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
                usuariosE = obtenerUsuariosEcono(conEcono)
                usuariosEcono = procesarUsuariosEcono(usuariosE)

                insertarUsuarioGoogle(curusuarioGoogle, usuariosEcono)
                actualizarUsuariosGoogle(curusuarioGoogle, usuariosEcono)
                conGoogle.commit()


            finally:
                curusuarioGoogle.close()
        finally:
            conGoogle.close()

    finally:
        conEcono.close()
