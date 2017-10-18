import time
import datetime
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
from jinja2 import Environment, FileSystemLoader

def render_html(destino, puertos):
     env = Environment(loader=FileSystemLoader('templates'), trim_blocks=False)
     templ = env.get_template('transferencia.tmpl')

     outp = templ.render(puertos=puertos)
     with open(destino,'w') as f:
         f.write(outp)


cmdGen = cmdgen.CommandGenerator()

bocas = 16
valores = []


if __name__ == '__main__':
    comunity = sys.argv[1]
    ip = sys.argv[2]
    bocas = int(sys.argv[3])
    destino = sys.argv[4]


    for i in range(1,bocas+1):
        valores.append({'boca':i, 'cantidad':0, 'acumulado':0.0, 'anterior':0.0, 'porsegundo':0.0, 'promedio':0.0})

    cantidad = 0
    acumulado = 0.0
    tanterior = datetime.datetime.now()
    anterior = 0.0
    while True:
        tactual = datetime.datetime.now()
        if (tactual - tanterior) > datetime.timedelta(seconds=1):

            for i in range(0,bocas):
                errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                    cmdgen.CommunityData(comunity),
                    cmdgen.UdpTransportTarget((ip, 161)),
                    'iso.3.6.1.2.1.2.2.1.10.{}'.format(i+1)
                )
                for n, p in varBinds:
                    v = (p / 1024 / 1024) * 8
                    if valores[i]['anterior'] == 0:
                        valores[i]['anterior'] = v
                        continue

                    valores[i]['porsegundo'] = float(v - valores[i]['anterior'])
                    valores[i]['anterior'] = v

                    valores[i]['cantidad'] = valores[i]['cantidad'] + 1
                    valores[i]['acumulado'] = valores[i]['acumulado'] + valores[i]['porsegundo']
                    valores[i]['promedio'] = float(valores[i]['acumulado'] / valores[i]['cantidad'])

            render_html(destino, valores)
