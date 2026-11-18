from conexion import engine
from modelo import Base


def crear_tablas():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    crear_tablas()