from datetime import timezone
import re
def validar_texto(cadena):
    if cadena.strip() == "":
        return False, "El elemento debe existir"
    return True

def validar_cantidad(cantidad):
    if cantidad < 1:
        return False, "La cantidad debe ser como mínimo 1."
    return True

def validar_stock(entero):
    if entero < 0:
        return False, "El stock o el precio no pueden ser negativos."
    return True

def validar_estado(estado):
    if not estado.lower() == "activo" or not estado.lower() == "devuelto":
        return False, "Estado invalido, debe ser activo o devuelto"
    return True

def validar_telefono(numero):
    patron = r"^(\+?56)?(\s?)9\d{8}$"
    if not re.match(patron, numero):
        return False, "Número invalido para el estandar de Chile"
    return True

def validar_correo(correo):
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(patron, correo):
        return False, "Ingrese un correo valido, como zramirez123@ejemplo.cl"
    return True

def validar_fecha(fecha):
        return False, "Ingrese su fecha en formato AAAA:MM:DD"
