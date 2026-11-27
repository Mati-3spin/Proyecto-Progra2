import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import crud
import graficos
from factory import TIPOS
from validacion import FORMATO_FECHA


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arriendo de Equipamiento Deportivo")
        self.geometry("1000x600")
        self.minsize(900, 550)

        cuaderno = ttk.Notebook(self)
        cuaderno.pack(fill="both", expand=True, padx=8, pady=8)

        self.pestania_categorias = PestaniaCategorias(cuaderno)
        self.pestania_equipos = PestaniaEquipos(cuaderno)
        self.pestania_clientes = PestaniaClientes(cuaderno)
        self.pestania_arriendos = PestaniaArriendos(cuaderno)
        self.pestania_reportes = PestaniaReportes(cuaderno)

        cuaderno.add(self.pestania_categorias, text="Categorías")
        cuaderno.add(self.pestania_equipos, text="Equipos")
        cuaderno.add(self.pestania_clientes, text="Clientes")
        cuaderno.add(self.pestania_arriendos, text="Arriendos")
        cuaderno.add(self.pestania_reportes, text="Reportes")


def _mostrar_resultado(ok, mensaje):
    if ok:
        messagebox.showinfo("Operación exitosa", mensaje)
    else:
        messagebox.showerror("Operación rechazada", mensaje)


def _crear_tabla(contenedor, columnas, anchos=None):
    marco = ttk.Frame(contenedor)
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=12)
    for i, columna in enumerate(columnas):
        tabla.heading(columna, text=columna)
        ancho = anchos[i] if anchos and i < len(anchos) else 100
        tabla.column(columna, width=ancho, anchor="center")
    barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    return marco, tabla


def _llenar_tabla(tabla, filas):
    tabla.delete(*tabla.get_children())
    for fila in filas:
        tabla.insert("", "end", values=fila)


class PestaniaCategorias(ttk.Frame):
    COLUMNAS = ("ID", "Nombre", "Descripción")

    def __init__(self, maestro):
        super().__init__(maestro)
        formulario = ttk.LabelFrame(self, text="Datos de la categoría")
        formulario.pack(fill="x", padx=6, pady=6)

        ttk.Label(formulario, text="ID (actualizar/eliminar):").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.entrada_id = ttk.Entry(formulario, width=10)
        self.entrada_id.grid(row=0, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Nombre:").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.entrada_nombre = ttk.Entry(formulario, width=40)
        self.entrada_nombre.grid(row=1, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Descripción:").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        self.entrada_descripcion = ttk.Entry(formulario, width=60)
        self.entrada_descripcion.grid(row=2, column=1, sticky="w", padx=4, pady=3)

        botones = ttk.Frame(self)
        botones.pack(fill="x", padx=6)
        ttk.Button(botones, text="Crear", command=self.crear).pack(side="left", padx=3)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=3)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=3)
        ttk.Button(botones, text="Refrescar", command=self.refrescar).pack(side="left", padx=3)

        marco, self.tabla = _crear_tabla(self, self.COLUMNAS, anchos=(60, 180, 400))
        marco.pack(fill="both", expand=True, padx=6, pady=6)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)
        self.refrescar()

    def _al_seleccionar(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        self.entrada_id.delete(0, "end"); self.entrada_id.insert(0, valores[0])
        self.entrada_nombre.delete(0, "end"); self.entrada_nombre.insert(0, valores[1])
        self.entrada_descripcion.delete(0, "end"); self.entrada_descripcion.insert(0, valores[2])

    def crear(self):
        ok, mensaje = crud.crear_categoria(self.entrada_nombre.get(), self.entrada_descripcion.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def actualizar(self):
        ok, mensaje = crud.actualizar_categoria(self.entrada_id.get(), self.entrada_nombre.get(),
                                                self.entrada_descripcion.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def eliminar(self):
        ok, mensaje = crud.eliminar_categoria(self.entrada_id.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def refrescar(self):
        _llenar_tabla(self.tabla, crud.consultar_categoria())


class PestaniaEquipos(ttk.Frame):
    COLUMNAS = ("ID", "Nombre", "CatID", "Categoría", "Precio diario",
                "Stock total", "Stock disponible", "Tipo")

    def __init__(self, maestro):
        super().__init__(maestro)
        formulario = ttk.LabelFrame(self, text="Datos del equipo")
        formulario.pack(fill="x", padx=6, pady=6)

        ttk.Label(formulario, text="ID (actualizar/eliminar):").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.entrada_id = ttk.Entry(formulario, width=10)
        self.entrada_id.grid(row=0, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Nombre:").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.entrada_nombre = ttk.Entry(formulario, width=30)
        self.entrada_nombre.grid(row=1, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="ID categoría:").grid(row=1, column=2, sticky="w", padx=4, pady=3)
        self.entrada_categoria = ttk.Entry(formulario, width=10)
        self.entrada_categoria.grid(row=1, column=3, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Precio diario:").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        self.entrada_precio = ttk.Entry(formulario, width=15)
        self.entrada_precio.grid(row=2, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Stock total:").grid(row=2, column=2, sticky="w", padx=4, pady=3)
        self.entrada_stock = ttk.Entry(formulario, width=10)
        self.entrada_stock.grid(row=2, column=3, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Tipo:").grid(row=3, column=0, sticky="w", padx=4, pady=3)
        self.combo_tipo = ttk.Combobox(formulario, values=TIPOS, state="readonly", width=17)
        self.combo_tipo.set("otro")
        self.combo_tipo.grid(row=3, column=1, sticky="w", padx=4, pady=3)

        botones = ttk.Frame(self)
        botones.pack(fill="x", padx=6)
        ttk.Button(botones, text="Crear", command=self.crear).pack(side="left", padx=3)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=3)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=3)
        ttk.Button(botones, text="Refrescar", command=self.refrescar).pack(side="left", padx=3)
        ttk.Button(botones, text="Solo disponibles", command=self.mostrar_disponibles).pack(side="left", padx=3)
        ttk.Button(botones, text="Todos", command=self.refrescar).pack(side="left", padx=3)

        marco, self.tabla = _crear_tabla(self, self.COLUMNAS,
                                          anchos=(50, 180, 60, 150, 100, 90, 110, 90))
        marco.pack(fill="both", expand=True, padx=6, pady=6)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)
        self.refrescar()

    def _al_seleccionar(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        for entrada, indice in ((self.entrada_id, 0), (self.entrada_nombre, 1),
                                 (self.entrada_categoria, 2), (self.entrada_precio, 4),
                                 (self.entrada_stock, 5)):
            entrada.delete(0, "end"); entrada.insert(0, valores[indice])
        self.combo_tipo.set(valores[7])

    def crear(self):
        ok, mensaje = crud.crear_equipo(self.entrada_nombre.get(), self.entrada_categoria.get(),
                                         self.entrada_precio.get(), self.entrada_stock.get(),
                                         tipo=self.combo_tipo.get() or "otro")
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def actualizar(self):
        ok, mensaje = crud.actualizar_equipo(self.entrada_id.get(), self.entrada_nombre.get(),
                                              self.entrada_categoria.get(), self.entrada_precio.get(),
                                              self.entrada_stock.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def eliminar(self):
        ok, mensaje = crud.eliminar_equipo(self.entrada_id.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def refrescar(self):
        _llenar_tabla(self.tabla, crud.consultar_equipo())

    def mostrar_disponibles(self):
        _llenar_tabla(self.tabla, crud.consultar_equipos_disponibles())


class PestaniaClientes(ttk.Frame):
    COLUMNAS = ("ID", "Nombre", "Correo", "Teléfono")

    def __init__(self, maestro):
        super().__init__(maestro)
        formulario = ttk.LabelFrame(self, text="Datos del cliente")
        formulario.pack(fill="x", padx=6, pady=6)

        ttk.Label(formulario, text="ID (actualizar/eliminar):").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.entrada_id = ttk.Entry(formulario, width=10)
        self.entrada_id.grid(row=0, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Nombre:").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.entrada_nombre = ttk.Entry(formulario, width=40)
        self.entrada_nombre.grid(row=1, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Correo:").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        self.entrada_correo = ttk.Entry(formulario, width=40)
        self.entrada_correo.grid(row=2, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Teléfono:").grid(row=3, column=0, sticky="w", padx=4, pady=3)
        self.entrada_telefono = ttk.Entry(formulario, width=20)
        self.entrada_telefono.grid(row=3, column=1, sticky="w", padx=4, pady=3)

        botones = ttk.Frame(self)
        botones.pack(fill="x", padx=6)
        ttk.Button(botones, text="Crear", command=self.crear).pack(side="left", padx=3)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=3)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=3)
        ttk.Button(botones, text="Refrescar", command=self.refrescar).pack(side="left", padx=3)

        marco, self.tabla = _crear_tabla(self, self.COLUMNAS, anchos=(60, 220, 260, 140))
        marco.pack(fill="both", expand=True, padx=6, pady=6)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)
        self.refrescar()

    def _al_seleccionar(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        for entrada, indice in ((self.entrada_id, 0), (self.entrada_nombre, 1),
                                 (self.entrada_correo, 2), (self.entrada_telefono, 3)):
            entrada.delete(0, "end"); entrada.insert(0, valores[indice])

    def crear(self):
        ok, mensaje = crud.crear_cliente(self.entrada_nombre.get(), self.entrada_correo.get(),
                                          self.entrada_telefono.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def actualizar(self):
        ok, mensaje = crud.actualizar_cliente(self.entrada_id.get(), self.entrada_nombre.get(),
                                               self.entrada_correo.get(), self.entrada_telefono.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def eliminar(self):
        ok, mensaje = crud.eliminar_cliente(self.entrada_id.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def refrescar(self):
        _llenar_tabla(self.tabla, crud.consultar_cliente())


class PestaniaArriendos(ttk.Frame):
    COLUMNAS = ("ID", "Equipo", "Cliente", "Inicio", "Fin prevista",
                "Cantidad", "Estado", "Precio total")

    def __init__(self, maestro):
        super().__init__(maestro)
        formulario = ttk.LabelFrame(self, text="Registrar arriendo / devolución")
        formulario.pack(fill="x", padx=6, pady=6)

        ttk.Label(formulario, text="ID equipo:").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.entrada_equipo = ttk.Entry(formulario, width=10)
        self.entrada_equipo.grid(row=0, column=1, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="ID cliente:").grid(row=0, column=2, sticky="w", padx=4, pady=3)
        self.entrada_cliente = ttk.Entry(formulario, width=10)
        self.entrada_cliente.grid(row=0, column=3, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="Cantidad:").grid(row=0, column=4, sticky="w", padx=4, pady=3)
        self.entrada_cantidad = ttk.Entry(formulario, width=10)
        self.entrada_cantidad.grid(row=0, column=5, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text=f"Inicio ({FORMATO_FECHA}):").grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.entrada_inicio = ttk.Entry(formulario, width=20)
        self.entrada_inicio.insert(0, datetime.now().strftime(FORMATO_FECHA))
        self.entrada_inicio.grid(row=1, column=1, columnspan=2, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text=f"Fin prevista ({FORMATO_FECHA}):").grid(row=1, column=3, sticky="w", padx=4, pady=3)
        self.entrada_fin = ttk.Entry(formulario, width=20)
        self.entrada_fin.grid(row=1, column=4, columnspan=2, sticky="w", padx=4, pady=3)

        ttk.Label(formulario, text="ID arriendo (devolver):").grid(row=2, column=0, sticky="w", padx=4, pady=3)
        self.entrada_arriendo = ttk.Entry(formulario, width=10)
        self.entrada_arriendo.grid(row=2, column=1, sticky="w", padx=4, pady=3)

        botones = ttk.Frame(self)
        botones.pack(fill="x", padx=6)
        ttk.Button(botones, text="Registrar arriendo", command=self.crear).pack(side="left", padx=3)
        ttk.Button(botones, text="Registrar devolución", command=self.devolver).pack(side="left", padx=3)
        ttk.Button(botones, text="Solo activos", command=self.mostrar_activos).pack(side="left", padx=3)
        ttk.Button(botones, text="Historial completo", command=self.refrescar).pack(side="left", padx=3)

        marco, self.tabla = _crear_tabla(self, self.COLUMNAS,
                                          anchos=(50, 160, 160, 130, 130, 80, 90, 100))
        marco.pack(fill="both", expand=True, padx=6, pady=6)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)
        self.refrescar()

    def _al_seleccionar(self, _evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        self.entrada_arriendo.delete(0, "end")
        self.entrada_arriendo.insert(0, valores[0])

    def crear(self):
        ok, mensaje = crud.crear_arriendo(self.entrada_equipo.get(), self.entrada_cliente.get(),
                                           self.entrada_inicio.get(), self.entrada_fin.get(),
                                           self.entrada_cantidad.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def devolver(self):
        ok, mensaje = crud.devolver_arriendo(self.entrada_arriendo.get())
        _mostrar_resultado(ok, mensaje)
        if ok: self.refrescar()

    def refrescar(self):
        _llenar_tabla(self.tabla, crud.consultar_arriendo())

    def mostrar_activos(self):
        _llenar_tabla(self.tabla, crud.consultar_arriendos_activos())


class PestaniaReportes(ttk.Frame):
    def __init__(self, maestro):
        super().__init__(maestro)
        ttk.Label(self, text="Gráficos generados con Matplotlib a partir de los datos reales.",
                  padding=10).pack()
        ttk.Button(self, text="Mostrar gráficos",
                   command=self._mostrar).pack(pady=20)

    def _mostrar(self):
        try:
            graficos.mostrar_graficos()
        except Exception as error:
            messagebox.showerror("Error", f"No se pudieron generar los gráficos:\n{error}")
