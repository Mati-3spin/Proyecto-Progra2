from modelo import Equipo, Raqueta, PelotaFutbol, Casco


class CreadorEquipo:
    def fabricar(self, **datos):
        raise NotImplementedError

    def crear(self, nombre, categoria_id, precio_diario, stock_total):
        return self.fabricar(
            nombre=nombre,
            categoria_id=categoria_id,
            precio_diario=precio_diario,
            stock_total=stock_total,
            stock_disponible=stock_total,
        )


class CreadorRaqueta(CreadorEquipo):
    def fabricar(self, **datos):
        return Raqueta(**datos)


class CreadorPelota(CreadorEquipo):
    def fabricar(self, **datos):
        return PelotaFutbol(**datos)


class CreadorCasco(CreadorEquipo):
    def fabricar(self, **datos):
        return Casco(**datos)


class CreadorOtro(CreadorEquipo):
    def fabricar(self, **datos):
        return Equipo(**datos)

CREADORES = {
    "raqueta": CreadorRaqueta(),
    "pelota_futbol": CreadorPelota(),
    "casco": CreadorCasco(),
    "otro": CreadorOtro(),
}

TIPOS = list(CREADORES)


def obtener_creador(tipo):
    if not isinstance(tipo, str):
        return None
    return CREADORES.get(tipo.strip().lower())