from datetime import date
from sqlalchemy import String, Integer, CheckConstraint, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Categoria(Base):
    __tablename__ = 'categoria'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(150), nullable=False)

    def __repr__(self):
        return (f"Categoria (id={self.id}, nombre={self.nombre}, descripcion={self.descripcion})")


class Equipo(Base):
    __tablename__ = 'equipo'
    __table_args__= (
        CheckConstraint("precio_diario >=0", name="ck_precio_diario"),
        CheckConstraint("stock_total >=0", name="ck_stock_total"),
        CheckConstraint("stock_disponible >=0", name="ck_stock_disponible"),
        CheckConstraint("stock_total >= stock_disponible", name="ck_stock_valido")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True , nullable=False)
    categoria_id: Mapped[int] = mapped_column(Integer, ForeignKey('categoria.id'), nullable=False)   
    precio_diario: Mapped[str] = mapped_column(Integer, default=0, nullable=False)   
    stock_total: Mapped[str] = mapped_column(Integer, default=0, nullable=False) 
    stock_disponible: Mapped[str] = mapped_column(Integer, default=0, nullable=False) 

    categoria = relationship("Categoria")

    def __repr__(self):
        return (f"Equipo (id={self.id}, nombre={self.nombre}), categoria_id={self.categoria_id}, precio_diario={self.precio_diario}, stock_total={self.stock_total}, stock_disponible={self.stock_disponible}")


class Cliente(Base):
    __tablename__ = 'cliente'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)   
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)   

    def __repr__(self):
        return (f"Cliente (id={self.id}, nombre={self.nombre}), correo={self.correo}, telefono={self.telefono}")


class Arriendo(Base):
    __tablename__ = 'arriendo'
    __table_args__= (
        CheckConstraint("stock_disponible >0", name="ck_stock_disponible"),
        CheckConstraint("estado IN ('activo', 'devuelto')", name="ck_estado_valido"),
        CheckConstraint("fecha_fin_prevista >= fecha_inicio", name="ck_rango_arriendo_fechas")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_id: Mapped[int] = mapped_column(Integer, ForeignKey('equipo.id'), nullable=False)   
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('cliente.id'), nullable=False)   
    fecha_inicio: Mapped[date] = mapped_column(Date, unique=True , nullable=False)
    fecha_fin_prevista: Mapped[date] = mapped_column(Date, unique=True, nullable=False)   
    cantidad: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)

    equipo = relationship("Equipo")
    cliente = relationship("Cliente")

    def __repr__(self):
        return (f"Arriendo (id={self.id}, equipo_id={self.equipo_id}, cliente_id={self.cliente_id}), fecha_inicio={self.fecha_inicio}, fecha_fin_prevista={self.fecha_fin_prevista}, cantidad={self.cantidad}, estado={self.estado}")