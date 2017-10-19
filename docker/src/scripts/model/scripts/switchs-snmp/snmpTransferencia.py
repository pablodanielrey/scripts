import time
import datetime
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
from jinja2 import Environment, FileSystemLoader


"""
    iso.3.6.1.2.1.2.2.1.10 ---> octetos de entrada
    iso.3.6.1.2.1.2.2.1.11 --> paquetes unicast entrada
    iso.3.6.1.2.1.2.2.1.16 ---> octetos de salida
    iso.3.6.1.2.1.2.2.1.17 ---> paquetes unicast de salida
"""

def render_html(destino, estadisticas, puertos):
     env = Environment(loader=FileSystemLoader('templates'), trim_blocks=False)
     templ = env.get_template('transferencia.tmpl')

     outp = templ.render(estadisticas=estadisticas, puertos=puertos)
     with open(destino,'w') as f:
         f.write(outp)


def consultar_y_cargar_pks(id, bocas, valores, indice, estadisticas):
    for i in range(0,bocas):
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(comunity),
            cmdgen.UdpTransportTarget((ip, 161)),
            '{}.{}'.format(id,i+1)
        )
        for n, p in varBinds:
            print(n, p)
            v = p
            if valores[i][indice]['anterior'] == 0:
                valores[i][indice]['anterior'] = v
                continue

            valores[i][indice]['porsegundo'] = float(v - valores[i][indice]['anterior']) if (v - valores[i][indice]['anterior']) > 0 else 0
            valores[i][indice]['anterior'] = v

            valores[i][indice]['cantidad'] = valores[i][indice]['cantidad'] + 1
            valores[i][indice]['acumulado'] = valores[i][indice]['acumulado'] + valores[i][indice]['porsegundo']
            valores[i][indice]['promedio'] = float(valores[i][indice]['acumulado'] / valores[i][indice]['cantidad'])

            estadisticas['paquetes_total'] = estadisticas['paquetes_total'] + valores[i][indice]['promedio']


def consultar_y_cargar(id, bocas, valores, indice, estadisticas):
    for i in range(0,bocas):
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(comunity),
            cmdgen.UdpTransportTarget((ip, 161)),
            '{}.{}'.format(id,i+1)
        )
        for n, p in varBinds:
            print(n, p)
            v = (p / 1024 / 1024) * 8
            if valores[i][indice]['anterior'] == 0:
                valores[i][indice]['anterior'] = v
                continue

            valores[i][indice]['porsegundo'] = float(v - valores[i][indice]['anterior']) if (v - valores[i][indice]['anterior']) > 0 else 0
            valores[i][indice]['anterior'] = v

            valores[i][indice]['cantidad'] = valores[i][indice]['cantidad'] + 1
            valores[i][indice]['acumulado'] = valores[i][indice]['acumulado'] + valores[i][indice]['porsegundo']
            valores[i][indice]['promedio'] = float(valores[i][indice]['acumulado'] / valores[i][indice]['cantidad'])

            estadisticas['bytes_total'] = estadisticas['bytes_total'] + valores[i][indice]['promedio']

cmdGen = cmdgen.CommandGenerator()

bocas = 16
valores = []
estadisticas = {
    'bytes_total': 0.0,
    'paquetes_total': 0.0
}


if __name__ == '__main__':
    comunity = sys.argv[1]
    ip = sys.argv[2]
    bocas = int(sys.argv[3])
    destino = sys.argv[4]


    for i in range(1,bocas+1):
        valores.append({
                'boca':i,
                'entrada':{
                    'cantidad':0,
                    'acumulado':0.0,
                    'anterior':0.0,
                    'porsegundo':0.0,
                    'promedio':0.0
                    },
                'salida':{
                    'cantidad':0,
                    'acumulado':0.0,
                    'anterior':0.0,
                    'porsegundo':0.0,
                    'promedio':0.0
                    },
                'paquetes_entrada': {
                    'cantidad':0,
                    'acumulado':0.0,
                    'anterior':0.0,
                    'porsegundo':0.0,
                    'promedio':0.0
                    },
                'paquetes_salida': {
                    'cantidad':0,
                    'acumulado':0.0,
                    'anterior':0.0,
                    'porsegundo':0.0,
                    'promedio':0.0
                    },
                'errores_entrada': {
                    'cantidad':0,
                    'acumulado':0.0,
                    'anterior':0.0,
                    'porsegundo':0.0,
                    'promedio':0.0
                    },
                })

    cantidad = 0
    acumulado = 0.0
    tanterior = datetime.datetime.now()
    anterior = 0.0
    while True:
        tactual = datetime.datetime.now()
        if (tactual - tanterior) > datetime.timedelta(seconds=1):
            print('.')
            consultar_y_cargar('iso.3.6.1.2.1.2.2.1.10',bocas, valores, 'entrada', estadisticas)
            consultar_y_cargar('iso.3.6.1.2.1.2.2.1.16',bocas, valores, 'salida', estadisticas)
            consultar_y_cargar_pks('iso.3.6.1.2.1.2.2.1.11',bocas, valores, 'paquetes_entrada', estadisticas)
            consultar_y_cargar_pks('iso.3.6.1.2.1.2.2.1.17',bocas, valores, 'paquetes_salida', estadisticas)

            render_html(destino, estadisticas, valores)
