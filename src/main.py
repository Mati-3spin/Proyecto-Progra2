import logging

from crear_tabla import crear_tablas
from ui import Aplicacion


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    crear_tablas()
    app = Aplicacion()
    app.mainloop()


if __name__ == "__main__":
    main()
