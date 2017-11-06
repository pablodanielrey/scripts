import re, datetime,sys

#Hay que verificar que pasa cuando no existe hostname en un lease, no corta busqueda hasta que no encuentre el del siguiente lease que tenga hostname.
#expresionLeaseCompleto=re.compile('^lease (?P<IP>[0-9\.]+) .*? starts 1 (?P<Inicio>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});.*? ends 1 (?P<Fin>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});.*?hardware ethernet (?P<MAC>([0-9A-Fa-f]{2}[:]){5}[0-9A-Fa-f]{2});.*?client-hostname "(?P<Hostname>[a-z0-9\-]+)";.*?}',re.I|re.S|re.M)
#lease (?P<ip>\d+\.\d+\.\d+\.\d+) {\s* starts 1 (?P<inicio>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});\s* ends 1 (?P<fin>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});\s*(?P<config>[\s\S]+?)\n}
if len(sys.argv) <= 1:
    print("Falta pasar la mac")
    exit(1)

expresionLeaseCompleto=re.compile(r"lease (?P<ip>\d+\.\d+\.\d+\.\d+) {\s* starts 1 (?P<inicio>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});\s* ends 1 (?P<fin>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});\s*(?P<config>[\s\S]+?)\n}")

expresionMAC = re.compile(sys.argv[1])

def lectura():
    try:
        archivo=open('dhcpd.leases','r')
        ar=archivo.read()
    finally:
        archivo.close()
    return ar

def busqueda(iterador):
    #resultado={'ip':'0.0.0.0','inicio':'1970-01-01 00:00:00','fin':'1970-01-01 00:00:00','datos':'0'}
    resultado = {}
    fechaUltimo=datetime.datetime(1970,1,1,0,0,0)
    for item in iterador:
        if expresionMAC.search(item.group('config')):
            fechaActual=datetime.datetime.strptime(item.group('inicio'), "%Y/%m/%d %H:%M:%S")
            if fechaUltimo<fechaActual:
                fechaUltimo=fechaActual
                resultado['ip']=item.group('ip')
                resultado['inicio']=item.group('inicio')
                resultado['fin']=item.group('fin')
                resultado['datos']=item.group('config')
    return resultado

if __name__ == "__main__":
    archivo=lectura()
    iterador=expresionLeaseCompleto.finditer(archivo)
    resultado1=busqueda(iterador)
    if not resultado1:
        print('No se encuentra')
    else:
        print('IP:',resultado1['ip'])
        print('Inicio:',resultado1['inicio'])
        print('Fin:',resultado1['fin'])
        print('Datos:',resultado1['datos'])
