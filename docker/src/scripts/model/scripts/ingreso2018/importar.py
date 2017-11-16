import csv
import sys
import logging
import os
import uuid
import psycopg2
import psycopg2.extras

if __name__ == '__main__':

    arch = sys.argv[1]
    salida = '{}_proceso.csv'.format(arch.replace('.','_'))
    host = os.environ['HOST']
    user = os.environ['USER']
    passwd = os.environ['PASS']
    base = os.environ['BASE']

    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)
    try:
        cur = con.cursor()
        try:
            with open(arch, 'r') as f, open(salida,'w') as f2:
                ingreso = csv.reader(f, delimiter=';')
                for fila in ingreso:
                    apellido = fila[1].split(',')[0]
                    nombre = fila[1].split(',')[1]
                    dni = fila[2]
                    d = dni.lower().replace('pas','').replace('dni','').replace('ci','').replace('dnt','').strip()
                    if len(d) > 7:
                        d = d.upper()
                        n = nombre.strip()
                        a = apellido.strip()
                        uid = str(uuid.uuid4())

                        cur.execute('select 1 from profile.users where dni = %s', (d,))
                        if cur.rowcount > 0:
                            ss = '{};{};{};ya existe\n'.format(d, n, a)
                            f2.write(ss)
                            print(ss)
                            continue

                        cur.execute('insert into profile.users (id, dni, name, lastname) values (%s,%s,%s,%s)', (uid, d, n, a))

                        pid = str(uuid.uuid4())
                        pp = str(uuid.uuid4())
                        cur.execute('insert into credentials.user_password (id, user_id, username, password) values (%s,%s,%s,%s)', (pid, uid, d, pp))

                        con.commit()
                        ss = '{};{};{};creado\n'.format(d, n, a)
                        f2.write(ss)
                        print(ss)

        finally:
            cur.close()

    finally:
        con.close()
