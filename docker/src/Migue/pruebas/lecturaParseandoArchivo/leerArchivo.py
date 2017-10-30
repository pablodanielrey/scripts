import re
import sys
'''El codigo mas feo del universo no mirar'''

if len(sys.argv) <= 1:
    print("Falta pasar la mac")
    exit(1)


#expleaseejemplo = '(?P=<lease>lease ([0-9]+\.)+ \{.*starts(?<inicio>)hardware ethernet(?P=<mac>.*;?).*\})'
#Pagina de test de expresiones regulares https://pythex.org/

mac = sys.argv[1]
expComienzoLease=re.compile('^lease.')
expFinLease=re.compile('^}')
expStartsLease=re.compile('\s*^starts.')
expEndsLease=re.compile('\s*^ends.')
expHardwareLease=re.compile('\s*^hardware.')
expresionMAC = re.compile(mac)

def lectura():
    try:
        archivo=open('dhcpd.leases','r')
        ar=archivo.readlines()
    finally:
        archivo.close()
    return ar

def busqueda(lineas):
    leasesCoincidentes=[]
    lease={}
    procesandoLease=False
    for linea in lineas:
        if expComienzoLease.match(linea)!= None and not procesandoLease:
            procesandoLease=True
            lease={}
            lease['ip']=linea.split()[1]
        else:
            if expStartsLease.findall(linea.strip()) and procesandoLease:
                lease['starts']=linea.split()[2]+' '+linea.split()[3]
            if not 'never' in linea and expEndsLease.findall(linea.strip()) and procesandoLease:
                lease['ends']=linea.split()[2]+' '+linea.split()[3]
            if expHardwareLease.findall(linea.strip()) and procesandoLease:
                lease['hardware']=linea.split()[2]
            if expFinLease.findall(linea) and procesandoLease:
                if 'hardware' in lease and expresionMAC.findall(lease['hardware']):
                    leasesCoincidentes.append(lease)
                procesandoLease=False
    return leasesCoincidentes


def getIP(lease):
    return lease[0].split()[1]

if __name__ == "__main__":
    lineas=lectura()
    leases=busqueda(lineas)
    if len(leases) == 0:
        print('No esta')
    else:
        reciente=''
        ultimoLease=[]
        for coincidencia in leases:
            if coincidencia['starts']>reciente:
                reciente=coincidencia['starts']
                ultimoLease=coincidencia
        #print(getIP(ultimoLease))
        print('Ultima ip: '+coincidencia['ip'])
        print('Direcciones ip asignadas a ese dispositivo: ')
        for coincidencia in leases:
            print(coincidencia)
