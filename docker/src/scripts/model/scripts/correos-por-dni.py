import requests
import os
import sys
from pprint import pprint


if __name__ == '__main__':

    api = os.environ['USERS_API_URL']
    archivo = sys.argv[1]

    with open(archivo) as f, open('salida.txt','w') as f2:
        for dni in f:
            dni = dni.strip()
            if dni == '':
                continue
            print('--------------------')
            print(f'obteniendo {dni}')
            call = api + f'/usuarios/?dni={dni}'
            print(call)
            usuarios = requests.get(call).json()
            for usuario in usuarios:
                pprint(usuario)
                email = None
                for mail in usuario['mails']:
                    if mail['confirmado']:
                        if 'econo.unlp.edu.ar' in mail['email']:
                            email = mail['email']
                            break
                else:
                    for mail in usuario['mails']:
                        if mail['confirmado']:
                            email = mail['email']
                            break

                if not email:
                    email = 'No tiene'
                    
                pprint(email)
                f2.write('{};{};{};{}\n'.format(usuario['dni'], usuario['nombre'], usuario['apellido'], email))
            print('--------------------')
