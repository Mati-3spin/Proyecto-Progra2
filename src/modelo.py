import enum
from datetime import datetime
from sqlalchemy import String, Integer, CheckConstraint, ForeignKey, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Estado(str, enum.Enum):
    ACTIVO = "ACTIVO"
    DEVUELTO = "DEVUELTO"

class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[str] = mapped_column(String(150), nullable=False)

    equipos: Mapped[list["Equipo"]] = relationship(back_populates="categoria")

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre={self.nombre!r}, descripcion={self.descripcion!r})"

class Equipo(Base):
    __tablename__ = "equipo"
    __table_args__ = (
        CheckConstraint("precio_diario > 0", name="ck_precio_diario"),
        CheckConstraint("stock_total >= 0", name="ck_stock_total"),
        CheckConstraint("stock_disponible >= 0", name="ck_stock_disponible"),
        CheckConstraint("stock_disponible <= stock_total", name="ck_stock_valido"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria_id: Mapped[int] = mapped_column(Integer, ForeignKey("categoria.id", ondelete="RESTRICT"), nullable=False)
    precio_diario: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stock_disponible: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    categoria: Mapped["Categoria"] = relationship(back_populates="equipos")
    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="equipo")

    __mapper_args__ = {"polymorphic_on": "tipo", "polymorphic_identity": "otro"}
    def calcular_precio(self, dias):
        return self.precio_diario * dias

    def __repr__(self):
        return (f"Equipo(id={self.id}, nombre={self.nombre!r}, categoria_id={self.categoria_id}, "
                f"precio_diario={self.precio_diario}, stock_total={self.stock_total}, "
                f"stock_disponible={self.stock_disponible})")

# Sub equipos 

class Raqueta(Equipo):
    __mapper_args__ = {"polymorphic_identity": "raqueta"}

    def calcular_precio(self, dias):
        total = self.precio_diario * dias
        if dias >= 3:
            total = total * 90 // 100
        return total


class PelotaFutbol(Equipo):
    __mapper_args__ = {"polymorphic_identity": "pelota_futbol"}

    def calcular_precio(self, dias):
        return self.precio_diario * dias * 90 // 100


class Casco(Equipo):
    __mapper_args__ = {"polymorphic_identity": "casco"}

    def calcular_precio(self, dias):
        total = self.precio_diario * dias
        if dias >= 5:
            total = total * 90 // 100
        return total 



class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)

    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="cliente")

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre={self.nombre!r}, correo={self.correo!r}, telefono={self.telefono!r})"


class Arriendo(Base):
    __tablename__ = "arriendo"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_cantidad"),
        CheckConstraint("fecha_fin_prevista >= fecha_inicio", name="ck_rango_arriendo_fechas"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("equipo.id", ondelete="RESTRICT"), nullable=False)
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cliente.id", ondelete="RESTRICT"), nullable=False)
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_fin_prevista: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estado: Mapped[Estado] = mapped_column(Enum(Estado), default=Estado.ACTIVO, nullable=False)

    equipo: Mapped["Equipo"] = relationship(back_populates="arriendos")
    cliente: Mapped["Cliente"] = relationship(back_populates="arriendos")

    def __repr__(self):
        return (f"Arriendo(id={self.id}, equipo_id={self.equipo_id}, cliente_id={self.cliente_id}, "
                f"fecha_inicio={self.fecha_inicio}, fecha_fin_prevista={self.fecha_fin_prevista}, "
                f"cantidad={self.cantidad}, estado={self.estado})")