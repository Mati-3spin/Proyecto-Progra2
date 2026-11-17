# Evaluación Final - Proyecto 3

* **Curso :** Programación 2 - ICINF1109
* **Integrantes :** Matias Espinoza, Annan John
* **Docente :** Pedro Gaete Villegas

## Problema Planteado 
>Una empresa de arriendo de implementos deportivos necesita una aplicación de escritorio que 
>permita administrar categorías, equipos y clientes, registrar arriendos, controlar la disponibilidad y 
>procesar devoluciones. Los datos deben mantenerse en una base SQLite mediante SQLAlchemy ORM. 

## Dependencias
**sqlalchemy**: 2.1.9
**matplotlib**: 3.11.2
**sqlite3** 

## Arquitectura
```
ProyectoProgra2/
├── pyproject.toml
├── README.md
├── ui.py       # ventanas/pestañas Tkinter
├── .gitignore
└── src/
    ├── charts.py
    ├── Conexion.py
    ├── __init__.py
    ├── Modelo.py     
    ├── Factory.py
    ├── main.py         
    ├── Crud.py
    └── Validacion.py 
```
