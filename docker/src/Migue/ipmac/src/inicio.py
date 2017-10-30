from flask import Flask, render_template, jsonify
import re

#Crea instancia de aplicacion
app = Flask(__name__)
expresionMAC = re.compile('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$')

######################## Prueba de almacenamiento ##############################
leases= [
    {
        'mac': 'ff:ff:ff:ff:ff:ff',
        'ip': '127.0.0.1'
    },
    {
        'mac': 'ab:ab:ab:ab:ab:ab',
        'ip': '192.168.0.1'
    }
]
######################## Ruta por defecto / ####################################
@app.route("/")
def index():
    return render_template ('index.html')
################################################################################
######################## Manejador de Errores ##################################
def error(mensaje):
    response= jsonify({'mensaje': mensaje})
    response.status_code=400
    return response
################################################################################
######################## API ###################################################
@app.route('/ipmac/api/v1.0/', methods=['GET'])
def ipreturn_vacio():
    return error('Debe especificar una direccion MAC')

@app.route('/ipmac/api/v1.0/<mac>', methods=['GET'])
def ipreturn(mac):
    if expresionMAC.search(mac)==None:
        return error('Direccion MAC Invalida')
    '''
    try:
        leases=open('/var/lib/dhcpd/dhcpd.leases','r')

    except:
        return error('Error de acceso al archivo leases')
    finally:
        leases.close()
    '''

    #Busqueda de asignaciones en variable leases ¡¡¡Falta Implementar busqeuda en leases!!!
    asignacion=[asignacion for asignacion in leases if asignacion['mac'].lower()==mac.lower()]
    #Pregunto si existe dato alguno adentro de asignacion
    if len(asignacion)==0:
        return error('No existe registro en el leases para esa direccion MAC')
    return jsonify({'asignacion':asignacion[0]})

################################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)
