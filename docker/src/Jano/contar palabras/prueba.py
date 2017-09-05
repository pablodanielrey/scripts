
def verificarCorreo(correo, correos):
    return correos.count(correo)
    correos.extend(["correo"])
    return correos



correos = "pepe la la la pe pepe"

ok = verificarCorreo("la", correos)
print(ok)
