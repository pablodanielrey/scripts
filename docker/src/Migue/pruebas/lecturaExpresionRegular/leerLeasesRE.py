import re

'''El codigo mas feo del universo no mirar'''

expresionComienzoLease=re.compile('^lease.')
expresionFinLease=re.compile('^}')
expresionMAC = re.compile('f4:f5:24:8d:8f:06')

def lectura():
    try:
        archivo=open('dhcpd.leases','r')
        ar=archivo.read()
    finally:
        archivo.close()
    return ar

def parseo(lineas):
    leases=[]
    
    return leases

if __name__ == "__main__":
    archivo=lectura()
    leases=parseo(archivo)
    print('La Cantidad de Leases es de: %d' %len(leases))
    for ocurrencia in leases:
        if expresionMAC.findall(str(ocurrencia)):
            print(ocurrencia[0])
