from dataclasses import dataclass

from app.models.tipo_movimiento import TipoMovimiento


@dataclass(slots=True)
class Categoria:
    id: int | None
    nombre: str
    tipo: TipoMovimiento
