# -*- coding: utf-8 -*-
import csv
import sys
import logging
import os
import psycopg2
import psycopg2.extras
import datetime
from pprint import pprint

if __name__ == '__main__':
    host = os.environ['HOST']
    user = os.environ['USER']
    passwd = os.environ['PASS']
    base = os.environ['BASE']

    dni = sys.argv[1]

    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)
    try:
        cur = con.cursor()
        try:
            cur.execute('select id, name, lastname, dni from profile.users where dni = %s', (dni, ))
            for u in cur.fetchall():
                print('Se encontró el usuario')
                pprint(u)
                uid = u[0]

                print('Compensatorios actuales')
                cur.execute('select * from assistance.justification_compensatory_stock where user_id = %s', (uid,))
                for c in cur:
                    pprint(c)

                print('Agregando 1 al stock de compensatorios')
                cur.execute('update assistance.justification_compensatory_stock set stock = stock + 1, updated = NOW() where user_id = %s', (uid,))
                if cur.rowcount <= 0:
                    print('No tenía stock, por lo tanto se crea un registro con 1 compensatorio')
                    cur.execute('insert into assistance.justification_compensatory_stock (user_id, stock, updated) values (%s,%s,%s)', (uid, 1, datetime.datetime.now()))

                print('Compensatorios después de la actualización')
                cur.execute('select * from assistance.justification_compensatory_stock where user_id = %s', (uid,))
                for c in cur:
                    pprint(c)

                con.commit()
        finally:
            cur.close()
    finally:
        con.close()
