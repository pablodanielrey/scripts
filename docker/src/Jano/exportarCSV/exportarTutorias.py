# -*- coding: utf-8 -*-
import csv
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


    exportados=open('tutorias.csv', 'w')

    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)
    try:
        cur = con.cursor()
        try:
            cur.execute('''
            SELECT  alumno.lastname, alumno.name, alumno.dni, situation, tutor.name,tutor.lastname, tutor.dni, tutoring.tutorings.date
            	FROM tutoring.situations
            	INNER JOIN profile.users alumno ON (alumno.id = tutoring.situations.user_id)
            	INNER JOIN tutoring.tutorings on (tutoring.situations.tutoring_id = tutoring.tutorings.id)
            	INNER JOIN profile.users tutor ON (tutor.id = tutoring.tutorings.tutor_id)
                ORDER BY tutoring.tutorings.date, alumno.lastname, alumno.name;
            ''')
            a=csv.writer(exportados)

            a.writerow(['Nombre','Apellido', 'Dni', 'Situacion','Nombre Tutor','Apellido Tutor', 'Dni Tutor', 'Fecha'])


            for row in cur:
                a.writerow(row)
        finally:
            cur.close()

    finally:
        con.close()
