import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_BD = os.environ.get("ARRIENDOS_DB", os.path.join(RAIZ, "arriendos.db"))

engine = create_engine(f"sqlite:///{RUTA_BD}", echo=False)


@event.listens_for(engine, "connect")
def activar_claves_foraneas(conexion):
        conexion.execute("PRAGMA foreign_keys=ON")

Session = sessionmaker(bind=engine, expire_on_commit=False)