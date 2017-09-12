
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
            cur.execute('select id, name, lastname from profile.users order by name, lastname limit 10')
            for row in cur:
                id = row[0]
                nombre = row[1]
                apellido = row[2]
                print(id + ' ' + nombre + ' ' + apellido)

        finally:
            cur.close()

    finally:
        con.close()
