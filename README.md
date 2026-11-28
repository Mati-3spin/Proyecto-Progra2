# Sistema de Gestión de Arriendo de Equipamiento Deportivo

Proyecto Final · Evaluación 3

* **Curso:** Programación 2 - ICINF1109
* **Docente:** Pedro Gaete Villegas
* **Integrantes:** Matias Espinoza, Annan John
* **Fecha de entrega:** 1 de diciembre de 2026

## Descripción

Aplicación de escritorio para una empresa de arriendo de implementos deportivos. Permite administrar categorías, equipos y clientes, registrar arriendos, controlar la disponibilidad de stock y procesar devoluciones. Los datos se guardan en una base SQLite mediante SQLAlchemy ORM, por lo que se conservan al cerrar y reabrir la aplicación.

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje principal |
| SQLAlchemy (ORM) | Modelo de datos y consultas |
| SQLite | Base de datos (arriendos.db) |
| Tkinter | Interfaz gráfica |
| Matplotlib | Gráficos a partir de datos reales |
| Factory Method | Creación de objetos de tipos de equipamiento |
| uv | Gestión de entorno y dependencias |

Tkinter viene incluido con Python. En algunas distribuciones de Linux hay que instalarlo aparte (por ejemplo, `sudo apt install python3-tk`).

## Instalación y ejecución

Requisitos: [uv](https://docs.astral.sh/uv/) instalado.

```bash
git clone https://github.com/Mati-3spin/Proyecto-Progra2.git
cd Proyecto-Progra2
uv sync
```

`uv sync` crea el entorno virtual e instala las dependencias fijadas en `pyproject.toml` y `uv.lock`, por lo que no se usa `requirements.txt`.

Para crear la base de datos (si no existe) y ejecutar la aplicación:

```bash
uv run python src/crear_tabla.py
uv run python src/main.py
```

La base de datos `arriendos.db` se genera automáticamente en la raíz del proyecto. Para empezar desde cero basta con borrar ese archivo y volver a ejecutar `crear_tabla.py`.

## Estructura del proyecto

```
Proyecto-Progra2/
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
└── src/
    ├── conexion.py      # engine, sesión y activación de claves foráneas
    ├── modelo.py        # modelos ORM: Categoria, Equipo, Cliente, Arriendo
    ├── validacion.py    # validaciones reutilizables
    ├── crud.py          # CRUD, arriendos y devoluciones
    ├── crear_tabla.py   # creación de las tablas
    ├── main.py          # punto de entrada
    └── ui.py            # interfaz Tkinter
```

## Modelo de datos

| Entidad | Atributos | Restricciones |
|---|---|---|
| **Categoria** | id, nombre, descripcion | `nombre` único |
| **Equipo** | id, nombre, categoria_id, precio_diario, stock_total, stock_disponible | `precio_diario > 0`, `stock_total >= 0`, `stock_disponible >= 0`, `stock_disponible <= stock_total` |
| **Cliente** | id, nombre, correo, telefono | `correo` único |
| **Arriendo** | id, equipo_id, cliente_id, fecha_inicio, fecha_fin_prevista, cantidad,  precio_total, estado | `cantidad > 0`, `fecha_fin_prevista >= fecha_inicio`, estado `ACTIVO` o `DEVUELTO` |

Relaciones:

* Una categoría tiene muchos equipos (`Categoria.equipos`).
* Un equipo pertenece a una categoría y tiene muchos arriendos (`Equipo.categoria`, `Equipo.arriendos`).
* Un cliente puede tener muchos arriendos (`Cliente.arriendos`).
* Cada arriendo pertenece a un equipo y a un cliente.
* Las claves foráneas usan `ondelete="RESTRICT"` y no hay `cascade`, para no perder el historial.

Decisiones de diseño:

* El estado del arriendo es un `Enum` (`ACTIVO`, `DEVUELTO`).
* Las reglas de stock y fechas están en la base de datos (`CheckConstraint`) y también se validan en Python antes de guardar.
* SQLite no hace cumplir las claves foráneas por defecto, por lo que se activa `PRAGMA foreign_keys=ON` en cada conexión.
* Cada arriendo corresponde a un solo tipo de equipo (puede incluir varias unidades) y la devolución es completa.

## Reglas de negocio implementadas

* Un arriendo solo se registra si la cantidad es positiva y no supera el stock disponible.
* El stock se descuenta en la misma transacción que crea el arriendo.
* Solo se pueden registrar arriendos con equipo y cliente existentes.
* La fecha de término prevista no puede ser anterior a la de inicio (formato `AAAA-MM-DD HH:MM`).
* La devolución solo se permite para arriendos `ACTIVO`: cambia el estado a `DEVUELTO` y restituye exactamente las unidades arrendadas. No se puede devolver dos veces.
* No se puede eliminar una categoría con equipos, ni un equipo o cliente con arriendos. Se informa al usuario con un mensaje.
* Si el stock total de un equipo se edita, el disponible se recalcula y no puede quedar bajo las unidades que están arrendadas.
* Toda escritura se confirma en una transacción: si algo falla, se hace `rollback` y la base de datos queda como estaba.

## Pruebas de demostración

| Paso | Acción | Resultado esperado |
|---|---|---|
| 1 | Crear categoría y equipo con stock total 5 | Stock disponible 5 |
| 2 | Crear cliente y registrar arriendo de 2 unidades | Stock disponible 3; arriendo ACTIVO |
| 3 | Intentar arrendar 4 unidades adicionales | Operación rechazada; stock sigue en 3 |
| 4 | Devolver arriendo de 2 unidades | Stock disponible 5; estado DEVUELTO |
| 5 | Intentar devolver el mismo arriendo | Operación rechazada; stock sigue en 5 |
| 6 | Cerrar y reabrir la aplicación; mostrar gráficos | Datos persistentes y gráficos basados en la BD |

## Capturas

> Pendiente...

## Factory Method

**Problema que resuelve.** Cada tipo de equipamiento tiene su propia regla de precio. Sin un patrón, el CRUD tendría `if tipo == ...` repartidos por todo el código y habría que modificarlo cada vez que aparezca un tipo nuevo.

**Estructura (`src/factory.py`).**

| Rol | Clases |
|---|---|
| Creador base | `CreadorEquipo`, con el método fábrica `fabricar()` y la operación común `crear()` |
| Creadores concretos | `CreadorRaqueta`, `CreadorPelota`, `CreadorCasco`, `CreadorOtro` |
| Productos concretos | De clase padre `Equipo` proceden `Raqueta`, `PelotaFutbol`, `Casco` |

Cada creador concreto redefine `fabricar()` para decidir qué clase instanciar. `crear()` es común a todos: arma los datos del equipo y deja `stock_disponible` igual a `stock_total`. El diccionario `CREADORES` y la función `obtener_creador(tipo)` eligen el creador a partir del texto del tipo (`raqueta`, `pelota_futbol`, `casco` u `otro`).

**Reglas de precio por tipo** (`calcular_precio(dias)`):

| Tipo | Regla |
|---|---|
| Raqueta | 10% de descuento desde 3 días |
| Pelota de fútbol | 10% de descuento siempre |
| Casco | 10% de descuento desde 5 días |

Estas reglas son una decisión de diseño del equipo para mostrar el polimorfismo.

## Fuentes consultadas

* matplotlib.pyplot.bar - Matplotlib 3.11.2 documentation. (s. f.). [https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html)
* SQLAlchemy ORM - SQLAlchemy 2.0 Documentation. (s. f.). [https://docs.sqlalchemy.org/en/20/orm/](https://docs.sqlalchemy.org/en/20/orm/)
* tkinter.ttk - Tk themed widgets. (s. f.). Python Documentation. [https://docs.python.org/3/library/tkinter.ttk.html](https://docs.python.org/3/library/tkinter.ttk.html)
