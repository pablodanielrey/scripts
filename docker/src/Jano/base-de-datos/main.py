
import psycopg2
import os

if __name__ == '__main__':

    host = os.environ['HOST']
    user = os.environ['USER']
    passwd = os.environ['PASS']
    base = os.environ['BASE']
    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)
    try:
        cur = con.cursor()
        try:
            cur.execute('select name, lastname from profile.users limit 10')
            for nombre, apellido in cur:
                print(nombre + ' ' + apellido)

        finally:
            cur.close()

    finally:
        con.close()
