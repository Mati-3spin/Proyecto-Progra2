import logging
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
from conexion import Session
from modelo import Categoria, Equipo, Cliente, Arriendo, Estado
from factory import obtener_creador, TIPOS
import validacion as val

log = logging.getLogger(__name__)

# Auxiliares

def _mensaje_integridad(error):
    texto = str(error.orig)
    conocidos = {
        "categoria.nombre": "Ya existe una categoría con ese nombre.",
        "cliente.correo": "Ya existe un cliente con ese correo.",
    }
    for clave, mensaje in conocidos.items():
        if clave in texto:
            return False, mensaje
    if "FOREIGN KEY" in texto:
        return False, "La operación viola una relación con otros registros."
    if "CHECK" in texto:
        return False, "Los datos no cumplen las reglas de la base de datos."
    return False, "No se pudo guardar: los datos entran en conflicto con otros registros."


def _confirmar(session, mensaje):
    try:
        session.commit()
        return True, mensaje
    except IntegrityError as error:
        session.rollback()
        return _mensaje_integridad(error)
    except SQLAlchemyError:
        session.rollback()
        log.exception("Error de base de datos al confirmar")
        return False, "Error en la base de datos. No se realizaron cambios."

def _primer_error(*resultados):
    for ok, mensaje in resultados:
        if not ok:
            return False, mensaje
    return None

def _leer(sentencia, a_fila):
    with Session() as session:
        try:
            return [a_fila(objeto) for objeto in session.scalars(sentencia).all()]
        except SQLAlchemyError:
            log.exception("Error de lectura")
            return []

def _contar(session, modelo, condicion):
    return session.scalar(select(func.count()).select_from(modelo).where(condicion))


# Crear

def crear_categoria(nombre, descripcion):
    error = _primer_error(
        val.validar_texto(nombre, 100, campo="nombre"),
        val.validar_texto(descripcion, 150, campo="descripcion"),
    )
    if error:
        return error
    with Session() as session:
        session.add(Categoria(nombre=nombre.strip(), descripcion=descripcion.strip()))
        return _confirmar(session, "Categoría creada.")


def crear_equipo(nombre, categoria_id, precio_diario, stock_total, tipo="otro"):
    error = _primer_error(
        val.validar_texto(nombre, 100, campo="nombre"),
        val.validar_entero(categoria_id, campo="categoria id"),
        val.validar_precio_positivo(precio_diario),
        val.validar_stock_positivo(stock_total),
    )
    if error:
        return error
    creador = obtener_creador(tipo)
    if creador is None:
        return False, f"Tipo de equipo inválido. Opciones: {', '.join(TIPOS)}."
    with Session() as session:
        if session.get(Categoria, int(categoria_id)) is None:
            return False, "La categoría seleccionada no existe."
        session.add(creador.crear(
            nombre.strip(), int(categoria_id), int(precio_diario), int(stock_total)))
        return _confirmar(session, "Equipo creado.")


def crear_cliente(nombre, correo, telefono):
    error = _primer_error(
        val.validar_texto(nombre, 100, campo="nombre"),
        val.validar_texto(correo, 100, campo="correo"),
        val.validar_correo(correo),
        val.validar_telefono(telefono),
    )
    if error:
        return error
    with Session() as session:
        session.add(Cliente(nombre=nombre.strip(), correo=correo.strip(),
                            telefono=telefono.strip()))
        return _confirmar(session, "Cliente creado.")

# Leer

def consultar_categoria():
    sentencia = select(Categoria).order_by(Categoria.id)
    return _leer(sentencia, lambda c: (c.id, c.nombre, c.descripcion))


def _fila_equipo(e):
    return (e.id, e.nombre, e.categoria_id, e.categoria.nombre,
            e.precio_diario, e.stock_total, e.stock_disponible, e.tipo)


def consultar_equipo():
    sentencia = select(Equipo).options(joinedload(Equipo.categoria)).order_by(Equipo.id)
    return _leer(sentencia, _fila_equipo)


def consultar_equipos_disponibles():
    sentencia = (select(Equipo).options(joinedload(Equipo.categoria))
                .where(Equipo.stock_disponible > 0).order_by(Equipo.id))
    return _leer(sentencia, _fila_equipo)


def consultar_cliente():
    sentencia = select(Cliente).order_by(Cliente.id)
    return _leer(sentencia, lambda c: (c.id, c.nombre, c.correo, c.telefono))


def _fila_arriendo(a):
    return (a.id, a.equipo.nombre, a.cliente.nombre,
            a.fecha_inicio.strftime(val.FORMATO_FECHA),
            a.fecha_fin_prevista.strftime(val.FORMATO_FECHA),
            a.cantidad, a.estado.value)


def _sentencia_arriendos():
    return (select(Arriendo)
            .options(joinedload(Arriendo.equipo), joinedload(Arriendo.cliente))
            .order_by(Arriendo.id.desc()))


def consultar_arriendo():
    return _leer(_sentencia_arriendos(), _fila_arriendo)


def consultar_arriendos_activos():
    sentencia = _sentencia_arriendos().where(Arriendo.estado == Estado.ACTIVO)
    return _leer(sentencia, _fila_arriendo)


# Actualizar

def actualizar_categoria(id_categoria, nombre, descripcion):
    error = _primer_error(
        val.validar_entero(id_categoria, campo="id categoria"),
        val.validar_texto(nombre, 100, campo="nombre"),
        val.validar_texto(descripcion, 150, descripcion="descripcion"),
    )
    if error:
        return error
    with Session() as session:
        categoria = session.get(Categoria, int(id_categoria))
        if categoria is None:
            return False, "Categoría no encontrada."
        categoria.nombre = nombre.strip()
        categoria.descripcion = descripcion.strip()
        return _confirmar(session, "Categoría actualizada.")


def actualizar_equipo(id_equipo, nombre, categoria_id, precio_diario, stock_total):
    error = _primer_error(
        val.validar_entero(id_equipo, campo="id equipo"),
        val.validar_texto(nombre, 100, campo="nombre"),
        val.validar_entero(categoria_id, campo="categoria id"),
        val.validar_precio_positivo(precio_diario),
        val.validar_stock_positivo(stock_total),
    )
    if error:
        return error
    with Session() as session:
        equipo = session.get(Equipo, int(id_equipo))
        if equipo is None:
            return False, "Equipo no encontrado."
        if session.get(Categoria, int(categoria_id)) is None:
            return False, "La categoría seleccionada no existe."
        en_uso = equipo.stock_total - equipo.stock_disponible
        if int(stock_total) < en_uso:
            return False, (f"No se puede reducir el stock total a {int(stock_total)}: hay {en_uso} unidad(es) arrendadas actualmente.")
        equipo.nombre = nombre.strip()
        equipo.categoria_id = int(categoria_id)
        equipo.precio_diario = int(precio_diario)
        equipo.stock_total = int(stock_total)
        equipo.stock_disponible = int(stock_total) - en_uso
        return _confirmar(session, "Equipo actualizado.")


def actualizar_cliente(id_cliente, nombre, correo, telefono):
    error = _primer_error(
        val.validar_entero(id_cliente, campo="id cliente"),
        val.validar_texto(nombre, 100, campo="nombre"),
        val.validar_texto(correo, 100, campo="correo"),
        val.validar_correo(correo),
        val.validar_telefono(telefono),
    )
    if error:
        return error
    with Session() as session:
        cliente = session.get(Cliente, int(id_cliente))
        if cliente is None:
            return False, "Cliente no encontrado."
        cliente.nombre = nombre.strip()
        cliente.correo = correo.strip()
        cliente.telefono = telefono.strip()
        return _confirmar(session, "Cliente actualizado.")


# Eliminar

def eliminar_categoria(id_categoria):
    ok, mensaje = val.validar_entero(id_categoria)
    if not ok:
        return False, mensaje
    with Session() as session:
        categoria = session.get(Categoria, int(id_categoria))
        if categoria is None:
            return False, "Categoría no encontrada."
        cantidad = _contar(session, Equipo, Equipo.categoria_id == categoria.id)
        if cantidad:
            return False, (f"No se puede eliminar: la categoría tiene {cantidad} equipo(s). Elimine o reasigne esos equipos primero.")
        session.delete(categoria)
        return _confirmar(session, "Categoría eliminada.")


def eliminar_equipo(id_equipo):
    ok, mensaje = val.validar_entero(id_equipo)
    if not ok:
        return False, mensaje
    with Session() as session:
        equipo = session.get(Equipo, int(id_equipo))
        if equipo is None:
            return False, "Equipo no encontrado."
        cantidad = _contar(session, Arriendo, Arriendo.equipo_id == equipo.id)
        if cantidad:
            return False, (f"No se puede eliminar: el equipo tiene {cantidad} arriendo(s) en su historial.")
        session.delete(equipo)
        return _confirmar(session, "Equipo eliminado.")


def eliminar_cliente(id_cliente):
    ok, mensaje = val.validar_entero(id_cliente)
    if not ok:
        return False, mensaje
    with Session() as session:
        cliente = session.get(Cliente, int(id_cliente))
        if cliente is None:
            return False, "Cliente no encontrado."
        cantidad = _contar(session, Arriendo, Arriendo.cliente_id == cliente.id)
        if cantidad:
            return False, (f"No se puede eliminar: el cliente tiene {cantidad} arriendo(s) en su historial.")
        session.delete(cliente)
        return _confirmar(session, "Cliente eliminado.")


# Arriendos y devoluciones

def crear_arriendo(equipo_id, cliente_id, fecha_inicio, fecha_fin_prevista, cantidad):
    error = _primer_error(
        val.validar_entero(equipo_id, campo="equipo id"),
        val.validar_entero(cliente_id, campo="cliente id"),
        val.validar_cantidad_positiva(cantidad),
        val.validar_fecha(fecha_inicio),
        val.validar_fecha(fecha_fin_prevista),
    )
    if error:
        return error
    inicio = val.convertir_fecha(fecha_inicio)
    fin = val.convertir_fecha(fecha_fin_prevista)
    ok, mensaje = val.validar_rango_fechas(inicio, fin)
    if not ok:
        return False, mensaje

    with Session() as session:
        equipo = session.get(Equipo, int(equipo_id))
        if equipo is None:
            return False, "El equipo no existe."
        cliente = session.get(Cliente, int(cliente_id))
        if cliente is None:
            return False, "El cliente no existe."
        ok, mensaje = val.validar_cantidad_disponible(cantidad, equipo.stock_disponible)
        if not ok:
            return False, mensaje

        equipo.stock_disponible -= int(cantidad)
        session.add(Arriendo(
            equipo_id=equipo.id, cliente_id=cliente.id,
            fecha_inicio=inicio, fecha_fin_prevista=fin,
            cantidad=int(cantidad), estado=Estado.ACTIVO,
        ))
        return _confirmar(
            session,
            f"Arriendo registrado: {int(cantidad)} unidad(es) de {equipo.nombre}. "
            f"Stock disponible: {equipo.stock_disponible}.",
        )


def devolver_arriendo(id_arriendo):
    ok, mensaje = val.validar_entero(id_arriendo, campo="id arriendo")
    if not ok:
        return False, mensaje
    with Session() as session:
        arriendo = session.get(Arriendo, int(id_arriendo))
        if arriendo is None:
            return False, "Arriendo no encontrado."
        if arriendo.estado != Estado.ACTIVO:
            return False, "Este arriendo ya fue devuelto."
        equipo = arriendo.equipo
        if equipo.stock_disponible + arriendo.cantidad > equipo.stock_total:
            return False, "Inconsistencia de stock: la devolución superaría el stock total."

        equipo.stock_disponible += arriendo.cantidad
        arriendo.estado = Estado.DEVUELTO
        return _confirmar(
            session,
            f"Devolución registrada. Stock disponible de {equipo.nombre}: "
            f"{equipo.stock_disponible}.",
        )