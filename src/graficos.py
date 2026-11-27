import logging
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from conexion import Session
from modelo import Categoria, Equipo, Arriendo

log = logging.getLogger(__name__)


def arriendos_por_categoria():
    with Session() as session:
        try:
            sentencia = (
                select(Categoria.nombre, func.count(Arriendo.id))
                .join(Equipo, Equipo.categoria_id == Categoria.id)
                .join(Arriendo, Arriendo.equipo_id == Equipo.id)
                .group_by(Categoria.id)
                .order_by(func.count(Arriendo.id).desc())
            )
            return list(session.execute(sentencia).all())
        except SQLAlchemyError:
            log.exception("Error al consultar arriendos por categoría")
            return []


def equipos_mas_arrendados(limite=10):
    with Session() as session:
        try:
            sentencia = (
                select(Equipo.nombre, func.count(Arriendo.id))
                .join(Arriendo, Arriendo.equipo_id == Equipo.id)
                .group_by(Equipo.id)
                .order_by(func.count(Arriendo.id).desc())
                .limit(limite)
            )
            return list(session.execute(sentencia).all())
        except SQLAlchemyError:
            log.exception("Error al consultar equipos más arrendados")
            return []


def mostrar_graficos():
    import matplotlib.pyplot as plt

    datos_categorias = arriendos_por_categoria()
    datos_equipos = equipos_mas_arrendados()

    figura, ejes = plt.subplots(1, 2, figsize=(12, 5))
    figura.canvas.manager.set_window_title("Reportes de arriendos")

    ax1 = ejes[0]
    if datos_categorias:
        nombres = [fila[0] for fila in datos_categorias]
        totales = [fila[1] for fila in datos_categorias]
        ax1.bar(nombres, totales, color="#4c72b0")
        ax1.set_title("Cantidad de arriendos por categoría")
        ax1.set_xlabel("Categoría")
        ax1.set_ylabel("N° de arriendos")
        ax1.tick_params(axis="x", rotation=30)
    else:
        ax1.set_title("Cantidad de arriendos por categoría")
        ax1.text(0.5, 0.5, "Sin datos", ha="center", va="center", transform=ax1.transAxes)
        ax1.set_axis_off()

    ax2 = ejes[1]
    if datos_equipos:
        nombres = [fila[0] for fila in datos_equipos]
        totales = [fila[1] for fila in datos_equipos]
        ax2.barh(nombres[::-1], totales[::-1], color="#55a868")
        ax2.set_title("Equipos con mayor número de arriendos")
        ax2.set_xlabel("N° de arriendos")
        ax2.set_ylabel("Equipo")
    else:
        ax2.set_title("Equipos con mayor número de arriendos")
        ax2.text(0.5, 0.5, "Sin datos", ha="center", va="center", transform=ax2.transAxes)
        ax2.set_axis_off()

    figura.tight_layout()
    plt.show()
