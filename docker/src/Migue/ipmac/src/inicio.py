from flask import Flask, render_template, jsonify
import re, datetime

#Crea instancia de aplicacion
app = Flask(__name__)
######################## Expresiones Regulares #######################
expresionMAC = re.compile('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$')
expresionLeaseCompleto = re.compile(r"lease (?P<ip>\d+\.\d+\.\d+\.\d+) {\s* starts 1 (?P<inicio>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});\s* ends 1 (?P<fin>[\d]{4}/[\d]{2}/[\d]{2}\s[\d]{2}:[\d]{2}:[\d]{2});\s*(?P<config>[\s\S]+?)\n}")
######################## Acceso a datos ##############################
def lectura():
    try:
        archivo=open('dhcpd.leases','r')
        ar=archivo.read()
    finally:
        archivo.close()
    return ar

def busqueda(iterador,mac):
    resultado = {}
    expresionMACBuscada= re.compile(mac)
    fechaUltimo=datetime.datetime(1970,1,1,0,0,0)
    for item in iterador:
        if expresionMACBuscada.search(item.group('config')):
            fechaActual=datetime.datetime.strptime(item.group('inicio'), "%Y/%m/%d %H:%M:%S")
            print(fechaActual)
            if fechaUltimo<fechaActual:
                fechaUltimo=fechaActual
                resultado['ip']=item.group('ip')
                resultado['inicio']=item.group('inicio')
                resultado['fin']=item.group('fin')
                resultado['datos']=item.group('config')
    return resultado
######################## Ruta por defecto / ####################################
@app.route("/")
def index():
    return render_template ('index.html')
################################################################################
######################## Manejador de Errores ##################################
def error(mensaje,code=None):
    response= jsonify({'mensaje': mensaje})
    if not code:
        response.status_code=400
    else:
        response.status_code=code
    return response
################################################################################
######################## API ###################################################
@app.route('/ipmac/api/v1.0/', methods=['GET'])
def ipreturn_vacio():
    return error('Debe especificar una direccion MAC')

@app.route('/ipmac/api/v1.0/<mac>', methods=['GET'])
def ipreturn(mac):
    if not expresionMAC.search(mac):
        return error('Direccion MAC Invalida')
    else:
        archivo=lectura()
        resultado=busqueda(expresionLeaseCompleto.finditer(archivo),mac)
        if not resultado:
            return error('No existe registro en el leases para esa direccion MAC')
        else:
            return jsonify({'ip':resultado['ip']})
################################################################################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)
