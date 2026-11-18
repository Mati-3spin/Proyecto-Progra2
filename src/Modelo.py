import enum
from datetime import datetime
from sqlalchemy import String, Integer, CheckConstraint, ForeignKey, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Categoria(Base):
    __tablename__ = 'categoria'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(150), nullable=False)
    categorias: Mapped[list["Equipo"]] = relationship(
        back_populates="categoria", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (f"Categoria (id={self.id}, nombre={self.nombre}, descripcion={self.descripcion})")


class Equipo(Base):
    __tablename__ = 'equipo'
    __table_args__= (
        CheckConstraint("precio_diario >=1", name="ck_precio_diario"),
        CheckConstraint("stock_total >=0", name="ck_stock_total"),
        CheckConstraint("stock_disponible >=0", name="ck_stock_disponible"),
        CheckConstraint("stock_total >= stock_disponible", name="ck_stock_valido")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True , nullable=False)
    categoria_id: Mapped[int] = mapped_column(Integer, ForeignKey('categoria.id'), nullable=False)   
    precio_diario: Mapped[int] = mapped_column(Integer, default=0, nullable=False)   
    stock_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False) 
    stock_disponible: Mapped[int] = mapped_column(Integer, default=0, nullable=False) 
    categoria: Mapped["Categoria"] = relationship(back_populates="categorias")
    equipos: Mapped[list["Arriendo"]] = relationship(
            back_populates="equipo", 
            cascade="all, delete-orphan"
        )

    def __repr__(self):
        return (f"Equipo (id={self.id}, nombre={self.nombre}), categoria_id={self.categoria_id}, precio_diario={self.precio_diario}, stock_total={self.stock_total}, stock_disponible={self.stock_disponible}")


class Cliente(Base):
    __tablename__ = 'cliente'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)   
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    clientes: Mapped[list["Arriendo"]] = relationship(
            back_populates="cliente", 
            cascade="all, delete-orphan"
        )   

    def __repr__(self):
        return (f"Cliente (id={self.id}, nombre={self.nombre}), correo={self.correo}, telefono={self.telefono}")

class Estado(str, enum.Enum):
    ACTIVO = "ACTIVO"
    DEVUELTO = "DEVUELTO"

class Arriendo(Base):
    __tablename__ = 'arriendo'
    __table_args__= (
        CheckConstraint("cantidad >=1", name="ck_cantidad"),
        CheckConstraint("fecha_fin_prevista >= fecha_inicio", name="ck_rango_arriendo_fechas")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_id: Mapped[int] = mapped_column(Integer, ForeignKey('equipo.id'), nullable=False)   
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('cliente.id'), nullable=False)   
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_fin_prevista: Mapped[datetime] = mapped_column(DateTime, nullable=False)   
    cantidad: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    equipo: Mapped[Equipo] = relationship(back_populates="equipos")
    cliente: Mapped[Cliente] = relationship(back_populates="clientes")
    estado: Mapped[Estado] = mapped_column(
        Enum(Estado, native_enum=True), default=Estado.ACTIVO, nullable=False)

    def __repr__(self):
        return (f"Arriendo (id={self.id}, equipo_id={self.equipo_id}, cliente_id={self.cliente_id}), fecha_inicio={self.fecha_inicio}, fecha_fin_prevista={self.fecha_fin_prevista}, cantidad={self.cantidad}, estado={self.estado}")