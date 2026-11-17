# Evaluación Final - Proyecto 3

* **Curso :** Programación 2 - ICINF1109
* **Integrantes :** Matias
* **Docente :** Pedro Gaete Villegas

## Problema Planteado 
>Una empresa de arriendo de implementos deportivos necesita una aplicación de escritorio que 
>permita administrar categorías, equipos y clientes, registrar arriendos, controlar la disponibilidad y 
>procesar devoluciones. Los datos deben mantenerse en una base SQLite mediante SQLAlchemy ORM. 

## Dependencias
**sqlalchemy**: 2.1.9 en adelante
**matplotlib**: 3.11.2
**sqlite3** 

## Arquitectura
```
ProyectoProgra2/
├── pyproject.toml
├── README.md
├── ui/        # ventanas/pestañas Tkinter
├── charts.py  # consultas y gráficos
└── src/proyectoprogra2/
        ├── Conexion.py
        ├── __init__.py
        ├── Modelo.py     
        ├── Factory.py # Factory Method
        ├── main.py     
        └── Servicios/     arrendar, devolver, CRUD, validaciones
            ├── Crud.py
            └── Validacion.py 
```
