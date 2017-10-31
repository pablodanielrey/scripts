import re

#Hay que verificar que pasa cuando no existe hostname en un lease, no corta busqueda hasta que no encuentre el del siguiente lease que tenga hostname.
expresionLeaseCompleto=re.compile('^lease (?P<IP>[0-9\.]+) .*? starts 1 (?P<Inicio>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});.*? ends 1 (?P<Fin>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});.*?hardware ethernet (?P<MAC>([0-9A-Fa-f]{2}[:]){5}[0-9A-Fa-f]{2});.*?client-hostname "(?P<Hostname>[a-z0-9\-]+)";.*?}',re.I|re.S|re.M)

expresionMAC = re.compile('54:27:58:d7:27:73')

def lectura():
    try:
        archivo=open('dhcpd.leases','r')
        ar=archivo.read()
    finally:
        archivo.close()
    return ar

if __name__ == "__main__":
    archivo=lectura()
    iterador=expresionLeaseCompleto.finditer(archivo)
    for item in iterador:
        '''print('------------------------------------')
        print('IP:',item.group('IP'))
        print('Inicio:',item.group('Inicio'))
        print('Fin:',item.group('Fin'))
        print('MAC:',item.group('MAC'))
        print('HOSTNAME:',item.group('Hostname'))
        '''
        if expresionMAC.search(item.group('MAC')) == None:
            print('No es.')
        else:
            print('IP:',item.group('IP'))
            print('Inicio:',item.group('Inicio'))
            print('Fin:',item.group('Fin'))
            print('MAC:',item.group('MAC'))
            print('HOSTNAME',item.group('Hostname'))
            break
