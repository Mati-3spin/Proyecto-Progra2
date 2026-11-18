from datetime import datetime, timedelta
import re
def validar_texto(cadena):
    if cadena.strip() == "":
        return False, "El elemento debe existir."
    return True

def validar_stock_positivo(entero):
    if entero < 0:
        return False, "El stock o el precio no pueden ser negativos."
    return True

def validar_estado(estado):
    if not estado.upper() == "ACTIVO" and not estado.upper() == "DEVUELTO":
        return False, "Estado invalido, debe ser activo o devuelto."
    return True

def validar_telefono(numero):
    patron = r"^(\+?56)?(\s?)9\d{8}$"
    if not re.match(patron, numero):
        return False, "Número invalido para el estandar de Chile."
    return True

def validar_correo(correo):
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(patron, correo):
        return False, "Ingrese un correo valido, como zramirez123@ejemplo.cl"
    return True

def validar_fecha(fecha):
    if not datetime.strptime(fecha, "%Y-%m-%d %H:%M"):
        return False, "Ingrese su fecha en formato AAAA-MM-DD HH:MM"
    return True

# Regla de negocio: Los arriendos duran 90 minutos
def validar_tiempo_fechas(fecha_inicio: datetime, fecha_fin_prevista: datetime):
    diferencia = fecha_fin_prevista - fecha_inicio
    minimo = timedelta(minutes=90)
    if diferencia < minimo:
        return False, "La fecha inicial debe ser mayor por 90 minutos a la fecha final."
    return True

# Regla de negocio: La mínima cantidad es de 1
def validar_cantidad_precio(cantidad):
    if cantidad < 1:
        return False, "La cantidad debe ser como mínimo 1."
    return True

# Regla de negocio: El stock total debe ser mayor al disponible
def validar_stocks(disponible, total):
    if disponible > total:
        return False, "El stock total debe ser mayor al disponible."
    return True
