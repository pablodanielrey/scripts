
import sys
import logging
import os
import psycopg2
import psycopg2.extras
import uuid


if __name__ == '__main__':

    id=str(uuid.uuid4());
    usuario={'id':id, 'Nombre': 'Emanuel','Apellido':'Pais', 'DNI':'30000000'}



    host = os.environ['HOST']
    user = os.environ['USER']
    passwd = os.environ['PASS']
    base = os.environ['BASE']
    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)
    try:
        cur = con.cursor()
        try:
            cur.execute('select nombre, apellido from usuarios')
            # for row in cur:
            #     id = row[0]
            #     nombre = row[1]
            #     print(id + ' ' + nombre)

        finally:
            cur.close()

    finally:
        con.close()
