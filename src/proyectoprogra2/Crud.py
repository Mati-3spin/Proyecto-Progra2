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
            print("No hay categorias registradas")
            return
        for categoria in categorias:
            return categoria.id, categoria.nombre, categoria.descripcion

def consultar_equipo():
    with Session() as session:
        consulta1 = select(Equipo)
        equipos = session.scalars(consulta1).all()

        if not equipos:
            print("No hay equipos registrados")
            return
        for equipo in equipos:
            return equipo.id, equipo.nombre, equipo.categoria_id, equipo.precio_diario, equipo.stock_total, equipo.stock_disponible



# Actualizar

def actualizar_categoria(in_id_categoria, in_nombre, in_descripcion):
    with Session.begin() as session:
        #Buscar producto con ID
        categoria = session.get(Categoria, in_id_categoria)

        if categoria is None:
            print("Categoria no encontrada")
            return

        categoria.in_nombre = in_nombre
        categoria.in_descripcion = in_descripcion
    print("Categoria actulizado")

def actualizar_equipo(in_id_equipo, in_nombre, in_categoria_id, in_precio_diario, in_stock_total, in_stock_disponible):
    with Session.begin() as session:
        #Buscar producto con ID
        equipo = session.get(Equipo, in_id_equipo)

        if equipo is None:
            print("Equipo no encontrado")
            return

        equipo.in_nombre = in_nombre
        equipo.in_categoria_id = in_categoria_id
        equipo.in_precio_diario = in_precio_diario
        equipo.in_stock_total = in_stock_total
        equipo.in_stock_disponible=in_stock_disponible
    print("Equipo actualizado")

def actualizar_cliente(in_id_cliente, in_nombre, in_correo, in_telefono):
    with Session.begin() as session:
        #Buscar producto con ID
        cliente = session.get(Cliente, in_id_cliente)

        if cliente is None:
            print("Cliente no encontrado")
            return

        cliente.in_nombre = in_nombre
        cliente.in_correo = in_correo
        cliente.in_telefono = in_telefono
    print("Cliente actulizado")

# Eliminar

def eliminar_categoria(in_id_categoria):
    with Session.begin() as session:
        categoria = session.get(Categoria, in_id_categoria)
        if categoria is None:
            return "Categoria no encontrada"
        session.delete(categoria)
    print("Categoria eliminada")

def eliminar_equipo(in_id_equipo):
    with Session.begin() as session:
        equipo = session.get(Equipo, in_id_equipo)
        if equipo is None:
            return "Equipo no encontrado"
        session.delete(equipo)
    print("Equipo eliminado")

def eliminar_cliente(in_id_cliente):
    with Session.begin() as session:
        cliente = session.get(Cliente, in_id_cliente)
        if cliente is None:
            return "Cliente no encontrado"
        session.delete(cliente)
    print("Cliente eliminado")

def eliminar_arriendo(in_id_arriendo):
    with Session.begin() as session:
        arriendo = session.get(Arriendo, in_id_arriendo)
        if arriendo is None:
            return "Arriendo no encontrado"
        session.delete(arriendo)
    print("Arriendo eliminado")