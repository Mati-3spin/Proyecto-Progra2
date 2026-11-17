from sqlalchemy import select
from Conexion import Session
from Modelo import Categoria, Equipo, Cliente, Arriendo

# Crear

def crear_categoria(nombre, descripcion):
    with Session.begin() as session:
        categoria= Categoria(
            nombre = nombre,
            descripcion = descripcion
        )
        session.add(categoria)

def crear_equipo(nombre, categoria_id, precio_diario, stock_total, stock_disponible):
    with Session.begin() as session:
        equipo= Equipo(
            nombre = nombre,
            categoria_id = categoria_id,
            precio_diario = precio_diario,
            stock_total = stock_total,
            stock_disponible = stock_disponible
        )
        session.add(equipo)

def crear_cliente(nombre, correo, telefono):
    with Session.begin() as session:
        cliente= Cliente(
            nombre = nombre,
            correo = correo,
            telefono = telefono
        )
        session.add(cliente)

def crear_arriendo(equipo_id, cliente_id, fecha_inicio, fecha_fin_prevista, estado):
    with Session.begin() as session:
        arriendo= Arriendo(
            equipo_id = equipo_id,
            cliente_id = cliente_id,
            fecha_inicio = fecha_inicio, 
            fecha_fin_prevista = fecha_fin_prevista,
            estado = estado
        )
        session.add(arriendo)

# Leer 

def consultar_categoria():
    with Session() as session:
        consulta = select(Categoria)
        categorias = session.scalars(consulta).all()
        if not categorias:
            return False, "La categoria no existe"
        lista_categorias = []
        for categoria in categorias:
            lista_categorias.append((
                categoria.id,
                categoria.nombre,
                categoria.descripcion
            ))
        return lista_categorias

def consultar_equipo():
    with Session() as session:
        consulta = select(Equipo)
        equipos = session.scalars(consulta).all()
        if not equipos:
            return False, "El equipo no existe"
        lista_equipos = []
        for equipo in equipos:
            lista_equipos.append((
                equipo.id,
                equipo.nombre,
                equipo.categoria_id,
                equipo.precio_diario,
                equipo.stock_total,
                equipo.stock_disponible
            ))
        return lista_equipos

def consultar_cliente():
    with Session() as session:
        consulta = select(Cliente)
        clientes = session.scalars(consulta).all()
        if not clientes:
            return False, "El cliente no existe"
        lista_clientes = []
        for cliente in clientes:
            lista_clientes.append((
                cliente.id,
                cliente.nombre,
                cliente.correo,
                cliente.telefono
            ))
        return lista_clientes

def consultar_arriendo():
    with Session() as session:
        consulta = select(Arriendo)
        arriendos = session.scalars(consulta).all()
        if not arriendos:
            return False, "El arriendo no existe"
        lista_arriendos = []
        for arriendo in arriendos:
            lista_arriendos.append((
                arriendo.id,
                arriendo.equipo_id,
                arriendo.cliente_id,
                arriendo.fecha_inicio,
                arriendo.fecha_fin_prevista,
                arriendo.cantidad,
                arriendo.estado
            ))
        return lista_arriendos

# Actualizar

def actualizar_categoria(in_id_categoria, in_nombre, in_descripcion):
    with Session.begin() as session:
        categoria = session.get(Categoria, in_id_categoria)
        if categoria is None:
            return False, "Categoria no encontrada"
        categoria.nombre = in_nombre
        categoria.descripcion = in_descripcion
    return True, "Categoria Actualizada"

def actualizar_equipo(in_id_equipo, in_nombre, in_categoria_id, in_precio_diario, in_stock_total, in_stock_disponible):
    with Session.begin() as session:
        equipo = session.get(Equipo, in_id_equipo)
        if equipo is None:
            return False, "Equipo no encontrado"
        equipo.nombre = in_nombre
        equipo.categoria_id = in_categoria_id
        equipo.precio_diario = in_precio_diario
        equipo.stock_total = in_stock_total
        equipo.stock_disponible=in_stock_disponible
    return True, "Equipo Actualizado"

def actualizar_cliente(in_id_cliente, in_nombre, in_correo, in_telefono):
    with Session.begin() as session:
        cliente = session.get(Cliente, in_id_cliente)
        if cliente is None:
            return False, "Cliente no encontrado"
        cliente.nombre = in_nombre
        cliente.correo = in_correo
        cliente.telefono = in_telefono
    return True, "Cliente Actualizado"

def actualizar_arriendo(in_id_arriendo, in_equipo_id, in_cliente_id, in_fecha_inicio, in_fecha_fin_prevista, in_estado):
    with Session.begin() as session:
        arriendo = session.get(Arriendo, in_id_arriendo)
        if arriendo is None:
            return False, "Arriendo no encontrado"
        arriendo.equipo_id = in_equipo_id
        arriendo.cliente_id = in_cliente_id
        arriendo.fecha_inicio = in_fecha_inicio
        arriendo.fecha_fin_prevista = in_fecha_fin_prevista
        arriendo.estado = in_estado
    return True, "Arriendo Actualizado"

# Eliminar

def eliminar_categoria(in_id_categoria):
    with Session.begin() as session:
        categoria = session.get(Categoria, in_id_categoria)
        if categoria is None:
            return False, "Categoria no encontrada"
        session.delete(categoria)
    return True, "Categoria eliminada"

def eliminar_equipo(in_id_equipo):
    with Session.begin() as session:
        equipo = session.get(Equipo, in_id_equipo)
        if equipo is None:
            return False, "Equipo no encontrado"
        session.delete(equipo)
    return True, "Equipo eliminado"

def eliminar_cliente(in_id_cliente):
    with Session.begin() as session:
        cliente = session.get(Cliente, in_id_cliente)
        if cliente is None:
            return False, "Cliente no encontrado"
        session.delete(cliente)
    return True, "Cliente eliminado"

def eliminar_arriendo(in_id_arriendo):
    with Session.begin() as session:
        arriendo = session.get(Arriendo, in_id_arriendo)
        if arriendo is None:
            return False, "Arriendo no encontrado"
        session.delete(arriendo)
    return True, "Arriendo eliminado"
