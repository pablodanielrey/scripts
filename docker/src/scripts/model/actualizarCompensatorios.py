import sys
import logging
logging.getLogger().setLevel(logging.INFO)
import os
import psycopg2
import psycopg2.extras
import csv

if __name__ == '__main__':

    fileName = sys.argv[1]
    
    host = os.environ['DB_HOST']
    dbname = os.environ['DB_NAME']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
        
          with open("./csv/{}".format(fileName)) as csvfile:
              spamreader = csv.reader(csvfile, delimiter=',')
              
              errors = []
              for row in spamreader:
                  nombre = row[0]
                  numero_documento = row[1]
                  stock = int(row[2])

                  cur.execute("SELECT id FROM profile.users WHERE dni = %s", (numero_documento,))
                  user = cur.fetchone()
                  
                  if not user:
                      errors.push("No existe el usuario {}".format(numero_documento))
                  
                  cur.execute("SELECT user_id, stock FROM assistance.justification_compensatory_stock WHERE user_id = %s;", (user["id"],))
                  compensatorio = cur.fetchone()
                

                  if not compensatorio:
                      logging.info("insertar stock de {}. Nuevo stock: {}".format(numero_documento, stock))
                      cur.execute("INSERT INTO assistance.justification_compensatory_stock (user_id, stock) VALUES (%s, %s)", (user["id"], stock))
                  else:
                      nuevo_stock = int(compensatorio["stock"]) + stock
                      logging.info("actualizar stock de {}. Stock anterior: {}. Nuevo stock: {}".format(numero_documento, compensatorio["stock"], nuevo_stock))
                      cur.execute("UPDATE assistance.justification_compensatory_stock SET stock = %s WHERE user_id = %s;", (nuevo_stock, user["id"]))
                  

                  conn.rollback()

        finally:
          cur.close()

    finally:
        conn.close()

