# -*- coding: utf-8 -*-
import csv
import sys
import logging
import os
import psycopg2
import psycopg2.extras
import datetime
import json
from pprint import pprint

if __name__ == '__main__':
    host = os.environ['HOST']
    user = os.environ['USER']
    passwd = os.environ['PASS']
    base = os.environ['BASE']

    cadena = sys.argv[1]

    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)
    try:
        cur = con.cursor()
        try:
            cur.execute('select * from profile.users where dni ~* %s or name ~* %s or lastname ~* %s', (cadena, cadena, cadena))
            for u in cur:
                pprint(u)

        finally:
            cur.close()
    finally:
        con.close()
