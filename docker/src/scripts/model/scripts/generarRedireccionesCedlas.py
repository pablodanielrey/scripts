import sys
import csv
from pprint import pprint
from jinja2 import Environment, FileSystemLoader

def escribir_redirecciones(datos):
     env = Environment(loader=FileSystemLoader('templates'), trim_blocks=False)
     templ = env.get_template('redireccion.tmpl')
     outp = templ.render(redirecciones=datos)
     with open('/tmp/redirecciones.txt','w') as f:
         f.write(outp)

def obtener_redirecciones(archivo):
    redirecciones = []
    with open(archivo,'r') as f:
        reader = csv.reader(f, delimiter=',')
        for fila in reader:
            redirecciones.append((fila[0], fila[1]))
    return redirecciones

if __name__ == '__main__':

    archivo = sys.argv[1]
    r = obtener_redirecciones(archivo)
    pprint(r)
