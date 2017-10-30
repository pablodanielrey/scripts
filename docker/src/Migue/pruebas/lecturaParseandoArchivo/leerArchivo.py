import re

'''El codigo mas feo del universo no mirar'''

expresionComienzoLease=re.compile('^lease.')
expresionFinLease=re.compile('^}')
expresionMAC = re.compile('f4:f5:24:8d:8f:06')

def lectura():
    try:
        archivo=open('dhcpd.leases','r')
        ar=archivo.readlines()
    finally:
        archivo.close()
    return ar

def parseo(lineas):
    leases=[]
    lease=[]
    procesandoLease=False
    for linea in lineas:
        if expresionComienzoLease.match(linea)!= None and not procesandoLease:
            procesandoLease=True
            lease=[]
            lease.append(linea)
        else:
            if procesandoLease:
                lease.append(linea)
            if expresionFinLease.match(linea) and procesandoLease:
                procesandoLease=False
                leases.append(lease)
    return leases

if __name__ == "__main__":
    lineas=lectura()
    print ('La cantidad de lineas son: %d' %len(lineas))
    leases=parseo(lineas)
    print('La Cantidad de Leases es de: %d' %len(leases))
    for ocurrencia in leases:
        if expresionMAC.findall(str(ocurrencia)):
            print(ocurrencia[0])
