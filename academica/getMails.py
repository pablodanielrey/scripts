
import pyoo
import logging
import psycopg2
import sys
import inject

from model.registry import Registry
from model.connection.connection import Connection

if __name__ == '__main__':

    inject.configure()
    registry = inject.instance(Registry)

    logging.getLogger().setLevel(logging.INFO)

    template = sys.argv[1]
    logging.info('abriendo : {}'.format(template))
    calc = pyoo.Desktop('localhost', 2002)
    doc = calc.open_spreadsheet(template)
    try:
        conn = Connection(registry.getRegistry('dcsys'))
        con = conn.get()
        try:
            cur = con.cursor()

            sheet = doc.sheets[0]
            for r in sheet:
                try:
                    dni = r[1].value
                    if dni == '':
                        break
                    dni = str(int(dni))
                    logging.info(dni)

                    cur.execute('select email from profile.mails pm, profile.users pu where pu.dni = %s and pu.id = pm.user_id', (dni,))
                    r[3].value = ''
                    for c in cur:
                        if 'econo.unlp' in c['email']:
                            r[3].value = r[3].value + c['email'] + ' '

                except ValueError as e:
                    pass

        finally:
            conn.put(con)

        doc.save('{}.xls'.format(template))
    finally:
        doc.close()
