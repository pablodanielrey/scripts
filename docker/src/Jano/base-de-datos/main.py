import sys
import logging
import os
import psycopg2
import psycopg2.extras
import uuid



if __name__ == '__main__':

    id=str(uuid.uuid4());
    # usuario={'id':id, 'Nombre': 'Emanuel','Apellido':'Pais', 'DNI':'30000000'}



    host = os.environ['HOST']
    user = os.environ['USER']
    passwd = os.environ['PASS']
    base = os.environ['BASE']
    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)
    try:
        curusuario = con.cursor()

        try:
            # sql = ("INSERT INTO correos (id, usuario_id, correo) VALUES ((%s), 'b44a70cb-19fa-4134-923b-fd4d39d13abd', 'paul@econo.unlp.edu.ar' )",(id, ))
            curusuario.execute('''INSERT INTO usuarios VALUES ('b44a70cb-19fa-4134-923b-fd4d39d13abd', 'Paul', 'California', 30000000)''');
            con.commit()
            # for row in curusuario:
            #     id = row[0]
            #     nombre = row[1]
            #     print(id + ' ' + nombre)
        except Exception as e:
            print (e)


            # curusuario.execute('SELECT * FROM usuarios;')
            # for row in curusuario:
            #     id = row[0]
            #     nombre = row[1]
            #     apellido = row[2]
            #     dni = row[3]
            #
            #     curcorreo = con.cursor()
            #     curcorreo.execute("SELECT correo FROM correos WHERE usuario_id = (%s);",(id,))
            #     correo = str(curcorreo.fetchone())
            #     curcorreo.close()
            #
            #     curclave = con.cursor()
            #     curclave.execute("SELECT clave FROM claves WHERE usuario_id = (%s);",(id,))
            #     clave= str(curclave.fetchone())
            #
            #     curclave.close()
            #
            #     print(id + ' | ' + nombre + ' | ' + apellido + ' | ' + dni + ' | ' + correo + ' | ' + clave)


        finally:
            curusuario.close()

    finally:
        con.close()
