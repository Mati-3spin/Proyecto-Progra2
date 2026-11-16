
def validar_texto(cadena):
    if cadena.strip() == "":
        return False, "El elemento debe existir"
    return True

def validar_cantidad(cantidad):
    if cantidad < 1:
        return False, "La cantidad debe ser mínimo 1."
    return True

def validar_stock(entero):
    if entero < 0:
        return False, "El stock o el precio no pueden ser negativos."
    return True

def validar_estado(estado):
    if not estado.lower() == "activo" or not estado.lower() == "devuelto":
        return False, "Estado no valido, debe ser activo o devuelto"
    return True
