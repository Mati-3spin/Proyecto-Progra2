from sqlalchemy import String, Integer, CheckConstraint, ForeignKey
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
        CheckConstraint
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria_id: Mapped[int] = mapped_column(Integer, ForeignKey('categoria.id'), nullable=False)   
    precio_diario: Mapped[str] = mapped_column(Integer, default=0, nullable=False)   
    stock_total: Mapped[str] = mapped_column(Integer, default=0, nullable=False) 
    stock_disponible: Mapped[str] = mapped_column(Integer, default=0, nullable=False) 

    categoria = relationship("Categoria")

    def __repr__(self):
        return (f"Equipo (id={self.id}, nombre={self.nombre}),"
                f"categoria_id={self.categoria_id}, precio_diario={self.precio_diario}, stock_total={self.stock_total}, stock_disponible={self.stock_disponible}")
    


class Cliente(Base):
    __tablename__ = 'cliente'

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)   
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)   

    def __repr__(self):
        return (f"Cliente (id={self.id}, nombre={self.nombre}),"
                f"correo={self.correo}, telefono={self.telefono}")


class Arriendo(Base):
    __tablename__ = 'arriendo'
    __table_args__= (
        CheckConstraint()
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_id: Mapped[int] = mapped_column(Integer, ForeignKey('equipo.id'), nullable=False)   
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('cliente.id'), nullable=False)   
    fecha_inicio: Mapped[str] = mapped_column(String(10), nullable=False)
    fecha_fin_prevista: Mapped[str] = mapped_column(String(10), nullable=False)   
    cantidad: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estado: Mapped[str] = mapped_column(String(10), default="" , nullable=False)

    equipo = relationship("Equipo")
    cliente = relationship("Cliente")

    def __repr__(self):
        return (f"Arriendo (id={self.id}, equipo_id={self.equipo_id}, cliente_id={self.cliente_id}),"
                f"fecha_inicio={self.fecha_inicio}, fecha_fin_prevista={self.fecha_fin_prevista}, cantidad={self.cantidad}, estado={self.estado}")
