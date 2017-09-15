
import sys
import logging
import os
import psycopg2
import psycopg2.extras

if __name__ == '__main__':

    host = os.environ['HOST']
    user = os.environ['USER']
    passwd = os.environ['PASS']
    base = os.environ['BASE']
    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)
    try:
        cur = con.cursor()
        try:
            for i in range(100):
                cur.execute('insert into p (id, nombre) values (%s,%s)', ('walter','puto'))

            cur.execute('select id, nombre from p')
            for row in cur:
                id = row[0]
                nombre = row[1]
                print(id + ' ' + nombre)

        finally:
            cur.close()

    finally:
        con.close()
