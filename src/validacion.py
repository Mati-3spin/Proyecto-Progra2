from datetime import datetime
import re

FORMATO_FECHA = "%Y-%m-%d %H:%M"


def validar_texto(cadena, largo_maximo=None, campo="El texto"):
    if not isinstance(cadena, str) or cadena.strip() == "":
        return False, f"{campo} no puede estar en blanco."
    if largo_maximo is not None and len(cadena.strip()) > largo_maximo:
        return False, f"{campo} no puede superar los {largo_maximo} caracteres."
    return True, ""

def validar_entero(valor, campo="El valor"):
    if isinstance(valor, bool) or not re.fullmatch(r"[+-]?[0-9]{1,9}", str(valor).strip()):
        return False, f"{campo} debe ser un número entero (máximo 9 dígitos)."
    return True, ""


def validar_stock_positivo(valor):
    ok, mensaje = validar_entero(valor)
    if not ok:
        return False, "El stock debe ser un número entero."
    if int(valor) < 0:
        return False, "El valor del stock no puede ser negativo."
    return True, ""


def validar_cantidad_positiva(valor):
    ok, mensaje = validar_entero(valor)
    if not ok:
        return False, "La cantidad debe ser un número entero."
    if int(valor) < 1:
        return False, "La cantidad debe ser mayor a 0."
    return True, ""


def validar_precio_positivo(valor):
    ok, mensaje = validar_entero(valor)
    if not ok:
        return False, "El precio debe ser un número entero."
    if int(valor) < 1:
        return False, "El precio debe ser mayor a 0."
    return True, ""


def validar_stocks(disponible, total):
    for valor in (disponible, total):
        ok, mensaje = validar_stock_positivo(valor)
        if not ok:
            return False, mensaje
    if int(disponible) > int(total):
        return False, "El stock disponible no puede ser mayor al stock total."
    return True, ""


def validar_cantidad_disponible(cantidad, stock_disponible):
    if int(cantidad) > int(stock_disponible):
        return False, (f"Stock insuficiente: solicitó {int(cantidad)} unidad(es) y hay {int(stock_disponible)} disponible(s).")
    return True, ""


def validar_telefono(numero):
    patron = r"(\+?56)?\s?9\d{8}"
    if not isinstance(numero, str) or not re.fullmatch(patron, numero.strip()):
        return False, "Número inválido para el estándar de Chile, ej: +56 912345678"
    return True, ""


def validar_correo(correo):
    patron = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    if not isinstance(correo, str) or not re.fullmatch(patron, correo.strip()):
        return False, "Ingrese un correo válido, como zramirez123@ejemplo.cl"
    return True, ""


def validar_fecha(fecha):
    if isinstance(fecha, datetime):
        return True, ""
    try:
        datetime.strptime(str(fecha).strip(), FORMATO_FECHA)
    except ValueError:
        return False, "Ingrese la fecha en formato AAAA-MM-DD HH:MM, ej: 2026-12-01 10:30."
    return True, ""


def convertir_fecha(fecha):
    if isinstance(fecha, datetime):
        return fecha
    return datetime.strptime(str(fecha).strip(), FORMATO_FECHA)


def validar_rango_fechas(fecha_inicio, fecha_fin_prevista):
    if fecha_fin_prevista < fecha_inicio:
        return False, "La fecha de fin prevista no puede ser antes de la fecha de inicio."
    return True, ""