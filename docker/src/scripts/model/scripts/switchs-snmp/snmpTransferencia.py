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
                })

    cantidad = 0
    acumulado = 0.0
    tanterior = datetime.datetime.now()
    anterior = 0.0
    while True:
        tactual = datetime.datetime.now()
        if (tactual - tanterior) > datetime.timedelta(seconds=1):

            bytes_total = 0.0
            paquetes_total = 0.0

            for i in range(0,bocas):
                ''' bytes entrada '''
                errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                    cmdgen.CommunityData(comunity),
                    cmdgen.UdpTransportTarget((ip, 161)),
                    'iso.3.6.1.2.1.2.2.1.10.{}'.format(i+1)
                )
                for n, p in varBinds:
                    print(n, p)
                    v = (p / 1024 / 1024) * 8
                    if valores[i]['entrada']['anterior'] == 0:
                        valores[i]['entrada']['anterior'] = v
                        continue

                    valores[i]['entrada']['porsegundo'] = float(v - valores[i]['entrada']['anterior']) if (v - valores[i]['entrada']['anterior']) > 0 else 0
                    valores[i]['entrada']['anterior'] = v

                    valores[i]['entrada']['cantidad'] = valores[i]['entrada']['cantidad'] + 1
                    valores[i]['entrada']['acumulado'] = valores[i]['entrada']['acumulado'] + valores[i]['entrada']['porsegundo']
                    valores[i]['entrada']['promedio'] = float(valores[i]['entrada']['acumulado'] / valores[i]['entrada']['cantidad'])

                    bytes_total = bytes_total + valores[i]['entrada']['promedio']


                ''' bytes salida '''
                errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                    cmdgen.CommunityData(comunity),
                    cmdgen.UdpTransportTarget((ip, 161)),
                    'iso.3.6.1.2.1.2.2.1.16.{}'.format(i+1)
                )
                for n, p in varBinds:
                    print(n, p)

                    v = (p / 1024 / 1024) * 8
                    if valores[i]['salida']['anterior'] == 0:
                        valores[i]['salida']['anterior'] = v
                        continue

                    valores[i]['salida']['porsegundo'] = float(v - valores[i]['salida']['anterior']) if (v - valores[i]['salida']['anterior']) > 0 else 0
                    valores[i]['salida']['anterior'] = v

                    valores[i]['salida']['cantidad'] = valores[i]['salida']['cantidad'] + 1
                    valores[i]['salida']['acumulado'] = valores[i]['salida']['acumulado'] + valores[i]['salida']['porsegundo']
                    valores[i]['salida']['promedio'] = float(valores[i]['salida']['acumulado'] / valores[i]['salida']['cantidad'])

                    bytes_total = bytes_total + valores[i]['salida']['promedio']


                ''' paquetes entrada '''
                errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                    cmdgen.CommunityData(comunity),
                    cmdgen.UdpTransportTarget((ip, 161)),
                    'iso.3.6.1.2.1.2.2.1.11.{}'.format(i+1)
                )
                for n, p in varBinds:
                    v = p
                    if valores[i]['paquetes_entrada']['anterior'] == 0:
                        valores[i]['paquetes_entrada']['anterior'] = v
                        continue

                    valores[i]['paquetes_entrada']['porsegundo'] = float(v - valores[i]['paquetes_entrada']['anterior']) if (v - valores[i]['paquetes_entrada']['anterior']) > 0 else 0
                    valores[i]['paquetes_entrada']['anterior'] = v

                    valores[i]['paquetes_entrada']['cantidad'] = valores[i]['paquetes_entrada']['cantidad'] + 1
                    valores[i]['paquetes_entrada']['acumulado'] = valores[i]['paquetes_entrada']['acumulado'] + valores[i]['paquetes_entrada']['porsegundo']
                    valores[i]['paquetes_entrada']['promedio'] = float(valores[i]['paquetes_entrada']['acumulado'] / valores[i]['paquetes_entrada']['cantidad'])

                    paquetes_total = paquetes_total + valores[i]['paquetes_entrada']['promedio']

                ''' paquetes salida '''
                errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                    cmdgen.CommunityData(comunity),
                    cmdgen.UdpTransportTarget((ip, 161)),
                    'iso.3.6.1.2.1.2.2.1.17.{}'.format(i+1)
                )
                for n, p in varBinds:
                    v = p
                    if valores[i]['paquetes_salida']['anterior'] == 0:
                        valores[i]['paquetes_salida']['anterior'] = v
                        continue

                    valores[i]['paquetes_salida']['porsegundo'] = float(v - valores[i]['paquetes_salida']['anterior']) if (v - valores[i]['paquetes_salida']['anterior']) > 0 else 0
                    valores[i]['paquetes_salida']['anterior'] = v

                    valores[i]['paquetes_salida']['cantidad'] = valores[i]['paquetes_salida']['cantidad'] + 1
                    valores[i]['paquetes_salida']['acumulado'] = valores[i]['paquetes_salida']['acumulado'] + valores[i]['paquetes_salida']['porsegundo']
                    valores[i]['paquetes_salida']['promedio'] = float(valores[i]['paquetes_salida']['acumulado'] / valores[i]['paquetes_salida']['cantidad'])

                    paquetes_total = paquetes_total + valores[i]['paquetes_salida']['promedio']


            for tt in valores:
                for ttt in tt.values():
                    if type(ttt) == int:
                        if ttt < 0:
                            print(tt)
                            sys.exit(1)
                    elif type(ttt) == float:
                        if ttt < 0:
                            print(tt)
                            sys.exit(1)
                    else:
                        for tttt in ttt.values():
                            if type(tttt) != str and tttt < 0:
                                print(ttt)
                                print(tttt)
                                sys.exit(1);


            estadisticas['bytes_total'] = bytes_total
            estadisticas['paquetes_total'] = paquetes_total
            render_html(destino, estadisticas, valores)
