import sys
import logging
logging.getLogger().setLevel(logging.INFO)
import os
import psycopg2
import psycopg2.extras
import csv

if __name__ == '__main__':


    
    
    host = os.environ['DB_HOST']
    dbname = os.environ['DB_NAME']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
        
          with open('./scripts/model/compensatorios.csv') as csvfile:
              spamreader = csv.reader(csvfile, delimiter=',')
              for row in spamreader:
                  nombre = row[0]
                  numero_documento = row[1]
                  compensatorios = row[2]

                  consulta = cur.execute("SELECT id FROM profile.users WHERE dni = %s", (numero_documento,))
                  user = cur.fetchone()


                                      
                  cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
        

            #return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()

