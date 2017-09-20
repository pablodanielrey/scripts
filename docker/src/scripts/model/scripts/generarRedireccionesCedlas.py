import sys
import csv
from pprint import pprint
from jinja2 import Environment, FileSystemLoader

def escribir_redirecciones(datos, archivo):
     env = Environment(loader=FileSystemLoader('templates'), trim_blocks=False)
     templ = env.get_template('redireccion.tmpl')
     outp = templ.render(redirecciones=datos)
     with open(archivo, 'w') as f:
         f.write(outp)

def obtener_redirecciones(archivo):
    cedlas = []
    sedlac = []
    lablac = []
    with open(archivo,'r') as f:
        reader = csv.reader(f, delimiter=',')
        for fila in reader:
            hacia = fila[1].replace('http://www.cedlas.econo.unlp.edu.ar','')\
                            .replace('http://cedlas.econo.unlp.edu.ar','')\
                            .replace('http://sedlac.econo.unlp.edu.ar','')\
                            .replace('http://lablac.econo.unlp.edu.ar','')\

            de = fila[0]
            if 'cedlas.econo.unlp.edu.ar' in de:
                de = de.replace('http://www.cedlas.econo.unlp.edu.ar','').replace('http://cedlas.econo.unlp.edu.ar','')
                if de not in [d for d,h in cedlas]:
                    cedlas.append((de, hacia))

            if 'lablac.econo.unlp.edu.ar' in de:
                de = de.replace('http://lablac.econo.unlp.edu.ar','')
                if de not in [d for d,h in lablac]:
                    lablac.append((de, hacia))

            if 'sedlac.econo.unlp.edu.ar' in de:
                de = de.replace('http://sedlac.econo.unlp.edu.ar','')
                if de not in [d for d,h in sedlac]:
                    sedlac.append((de, hacia))

    return cedlas, sedlac, lablac


if __name__ == '__main__':

    if len(sys.argv) <= 2:
        print('Debe llamar al script con el parámetro del archvio a leer\nEj: python3 {} archivo.csv archivo2.txt'.format(sys.argv[0]))
        sys.exit(1)

    archivo = sys.argv[1]
    redir = sys.argv[2]
    cedlas, sedlac, lablac = obtener_redirecciones(archivo)
    escribir_redirecciones(cedlas, redir + 'c')
    escribir_redirecciones(sedlac, redir + 's')
    escribir_redirecciones(lablac, redir + 'l')
